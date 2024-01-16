from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Request, FoundMessage
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flasgger import Swagger
import logging

app = Flask(__name__)
Swagger(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requestService.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/createRequest', methods=['GET', 'POST'])
def createRequest():
    if request.method == 'POST':
        blood_type = request.form['bloodtype']
        town = request.form['town']
        city = request.form['city']
        email = request.form['email']
        num_of_units = int(request.form['num_of_units'])
        duration_of_search = request.form['duration_of_search']
        reason = request.form['reason']

        new_request = Request(
            blood_type=blood_type,
            town=town,
            city=city,
            email=email,
            num_of_units=num_of_units,
            duration_of_search=duration_of_search,
            reason=reason
        )

        db.session.add(new_request)
        db.session.commit()
        
        return render_template('requestBlood.html', message="Request submitted successfully!")

    return render_template('requestBlood.html')


@app.route('/get_queue_data', methods=['GET'])
def get_queue_data():
    request_list = Request.query.all()
    
    result = []
    for request in request_list:
        data = {
            'id':request.id,
            'blood_type': request.blood_type,
            'town': request.town,
            'city': request.city,
            'num_of_units': request.num_of_units
        }
        result.append(data)
    
    return jsonify(result)

@app.route('/bloodFound', methods=['POST','GET'])
def bloodFound():
    if request.method == 'POST':
        data = request.get_json()
        app.logger.info(data)

        request_id = data.get('id')
        message = data.get('message')
        available_units = data.get('available_units')

        new_message = FoundMessage(request_id=request_id, message=message)
        db.session.add(new_message)
        db.session.commit()
        
        response_data = {
            'status': 'Success',
            'message': f'Received message for request id {request_id}: {message}'
        }

        app.logger.info(message)

        request_to_delete = Request.query.filter_by(id=request_id).first()
        if request_to_delete:
            if available_units < request_to_delete.num_of_units:
                # Num_of_units - available_units ile request'in kalan ihtiyacını güncelle
                request_to_delete.num_of_units -= available_units
                db.session.commit()
            else:
                db.session.delete(request_to_delete)
                db.session.commit()

    messages = FoundMessage.query.all()
    return render_template('messages.html', messages=messages)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(port=8686)