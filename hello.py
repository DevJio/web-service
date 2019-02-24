from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, send_file
from sklearn.externals import joblib
import numpy as np
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os

#import requests

app = Flask(__name__)
knn = joblib.load('knn.pkl')

@app.route('/')
def hello_world():
    print("go! go! go!")
    return "<h1>Hello, zettt fffff</h1>" + "simple example" + " рыба съедена!"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    username =int(username) * int(username)
    return 'User %s' % str(username)
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers),1)


@app.route('/avg/<nums>')
def avg(nums):
    nums = list(map(int,nums.split(',')))
    #nums = [float(num) for num in nums]
    nums_mean = mean(nums)
    print(nums)
    return "<h1>" +str(nums_mean) + "</h1>"

@app.route('/iris/<params>')
def iris(params):
    params = list(map(int,params.split(',')))
    print(params)
    params = np.array(params).reshape(1,-1)
    predict =knn.predict(params)
    return str(predict)

@app.route('/show_image')
def show_image():
    #return '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Iris_versicolor_3.jpg/1920px-Iris_versicolor_3.jpg" alt="versicolor">'
    return '<img src="/static/Iris_virginica.jpg" alt="not loaded">'

@app.route('/badrequest400')
def bad_request():
    return abort(400)


@app.route('/iris_post', methods=['POST'])
def add_message():
    
    try:
        content = request.get_json()
        print(content)
        params = content['flower'].split(',')
        print(params)
        params = np.array(params).reshape(1,-1)
        predict =knn.predict(params)
        # print(content) # Do your processing
        predict = {'class': str(predict[0])}
    except:
        return redirect(url_for('bad_request'))
    return jsonify(predict)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        print(form.name)
        
        f = form.file.data
        filename = form.name.data + '.txt'
        #f.save(os.path.join(filename))
        df = pd.read_csv(f, header=None)
        predict =knn.predict(df)

        result = pd.DataFrame(predict)
        result.to_csv(filename, index=False, header=False)


        return send_file(filename, mimetype='text/csv', attachment_filename=filename, as_attachment=True)
    return render_template('submit.html', form=form)
