from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, send_file
from flask import json
from flask_cors import CORS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

from sklearn.externals import joblib
import numpy as np
import random
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

knn = joblib.load('knn.pkl')
lr = joblib.load('lr.pkl')
count_vect = joblib.load('count_vect.pkl')
#pipeln = joblib.load('pipeln.pkl')

@app.route('/')
def hello_world():
    print("go! go! go!")
    return "<h1>test post service by json on ds_post {id:[ids], text: [texts]</h1>" 

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


@app.route('/ds_post', methods=['POST'])
def add_message():
    #try:
    content = request.get_json()
    data = pd.DataFrame(content)

    #print(data.head())

    
    X = count_vect.transform(data['text'])
    #print(X.shape)
    #data.loc[:,'class'] = [random.randint(1, 10) for x in range(data.shape[0])]
    data['class'] = lr.predict(X)
    data['probability'] = np.around(np.max(lr.predict_proba(X), axis=1), decimals=3)
    #print(data['probability'])
    #params = np.array(params).reshape(1,-1)
    #predict = {'class': str(predict[0])}
    
    response = app.response_class(response='{"id":'+str(list(data.id.values))+ ',"class":' + str(list(data['class'].values))+ \
        ',"probability":'+ str(list(data['probability'].values))+'}', 
    status=200, 
    mimetype='application/json')
    #print(response)
    #except:
        #return redirect(url_for('bad_request'))
    return response




app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))
