import os
from flask import render_template, request, redirect, url_for
from app import app
from app.controller.predictor import predict_cat_breed

@app.route('/')
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            predicted_class = predict_cat_breed(file_path)
            return render_template('index.html', predicted_class=predicted_class)
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return redirect(request.url)
    
    file = request.files['image']
    
    if file:
        # Panggil fungsi prediksi dengan file yang diunggah
        image_path, breed_name, breed_description = predict_cat_breed(file)
        
        # Kirim hasil prediksi dan gambar ke halaman result.html
        return render_template('result.html', breed_name=breed_name, description=breed_description, image_url=image_path)
    
    return redirect(url_for('index'))