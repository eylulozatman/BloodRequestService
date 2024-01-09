from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Request
from queue import Queue
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requestService.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

my_queue = Queue() 

@app.route('/', methods=['GET', 'POST'])
def homepage():
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
            'blood_type': request.blood_type,
            'town': request.town,
            'city': request.city,
            'num_of_units': request.num_of_units
        }
        result.append(data)
    
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=8686)

