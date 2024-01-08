from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requestService.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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
        
        return "Request submitted successfully!"

    return render_template('requestBlood.html')

if __name__ == '__main__':
    app.run(debug=True)

