from os import name
from flask import request, render_template, jsonify
from app import app
from utils import *
from models import Pests
from app import db

from flask_restful import marshal_with, fields


PestFields = {
    'id': fields.Integer,
    'name': fields.String,
    'image': fields.String
}

@app.route('/')
def home():
    print('Downloading Models..')
    download_models()
    
    return render_template("index.html")

@app.route('/submit', methods = ['POST'])
def submit():
    if request.method == 'POST':
        barangay = request.form['barangay']
        stage = request.form['stage']
        category = request.form['category']
        image = request.files['image']
        
        # check if image is human
        is_human = face_detector(image)

        # check if correct category -> image
        is_category_correct = predict_category(image, category)

        # clear temp folder
        clear_temp()

        if is_human: 
            return {'prediction': 'human'}
        elif not is_category_correct:
            return {'prediction': 'categorical'}
        else: 
            # Save image
            image_filename = save_image(image, category)

            # Prediction (Pests and Diseases)
            if category == 'Pest' or category == 'Disease':
                prediction = predict_image(category, image_filename)
            # Delta-E (Nutrients)
            else:
                prediction = delta_e(image_filename)

            return {
                'barangay': barangay,
                'stage': stage,
                'category': category,
                'image_filename': image_filename, 
                'prediction': prediction
                }

@app.route('/submit-api', methods = ['POST'])
def submit_api():
    if request.method == 'POST':
        barangay = request.form['barangay']
        stage = request.form['stage']
        category = request.form['category']
        image = request.files['image']
        
        # check if image is human
        is_human = face_detector(image)

        # check if correct category -> image
        is_category_correct = predict_category(image, category)

        # clear temp folder
        clear_temp()

        if is_human: 
            return {'prediction': 'human'}
        elif not is_category_correct:
            return {'prediction': 'categorical'}
        else: 
            # Save image
            image_filename = save_image(image, category)

            # Prediction (Pests and Diseases)
            if category == 'Pest' or category == 'Disease':
                prediction = predict_image(category, image_filename)
            # Delta-E (Nutrients)
            else:
                prediction = delta_e(image_filename)

            # clear images folders
            clear_images()
            
            return {
                'barangay': barangay,
                'stage': stage,
                'category': category,
                'image_filename': image_filename, 
                'prediction': prediction
                }

@app.route('/p/<image_filename>/<stage>/<category>/<prediction>/<barangay>', methods=['GET'])
def p(image_filename, stage, category, prediction, barangay):
    data = {
        'image_filename': image_filename,
        'stage': stage,
        'category': category,
        'prediction': prediction,
        'barangay': barangay
    }

    if category == "Pest": 
        return render_template('pest.html', data=data)
    elif category == 'Disease':
        return render_template('disease.html', data=data)
    elif category == 'Nutrient':
        return render_template('nutrient.html', data=data)


@app.route('/submit-sample', methods=['GET', 'POST'])
def submit_sample():
    return {
        'it worked!': 'haha!'
    }
