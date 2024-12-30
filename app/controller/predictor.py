import tensorflow as tf
import numpy as np
import os
from werkzeug.utils import secure_filename
from app.model.catbreedinfo import CatBreedInfo
from app import db 

# Muat model
model = tf.keras.models.load_model(r"C:\Users\HP\Documents\Kuliah\Umpo\Semester 5\Komputasi Pararel\Tugas Ke-2\Web Prediksi Ras Kucing\app\resource\CatBreed_ClassificationV4.h5")

# Label kelas yang sesuai dengan model
class_labels = {
    0: 'Bengal',
    1: 'Birman',
    2: 'British_shorthair',
    3: 'Persia',
    4: 'Ragdoll'
}

# Threshold berdasarkan F1-score
class_thresholds = {
    'Bengal': 0.80,  # F1-score 0.80
    'Birman': 0.78,  # F1-score 0.78
    'British_shorthair': 0.67,  # F1-score 0.67
    'Persia': 0.62,  # F1-score 0.62
    'Ragdoll': 0.45  # F1-score 0.50
}

# Tentukan folder untuk menyimpan gambar sementara
UPLOAD_FOLDER = "app/static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Fungsi prediksi
def predict_cat_breed(file):
    # Menyimpan file gambar sementara di server
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Memuat gambar dari file yang disimpan
    img = tf.keras.utils.load_img(file_path, target_size=(120, 120))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0 

    # Prediksi
    predictions = model.predict(img_array)
    max_confidence = np.max(predictions)  # Probabilitas tertinggi
    predicted_class_idx = np.argmax(predictions, axis=1)
    
    # Mendapatkan nama ras berdasarkan prediksi
    predicted_class = class_labels[predicted_class_idx[0]]

    # Cek apakah probabilitas tertinggi cukup tinggi berdasarkan F1-score threshold untuk kelas ini
    if max_confidence < class_thresholds[predicted_class]:
        return 'uploads/' + filename, "Unknown", "The uploaded image is not recognized as a cat breed. Please try another image."
    
    # Ambil deskripsi ras kucing dari database
    breed_info = CatBreedInfo.query.filter_by(breed_name=predicted_class).first()
    
    # Jika tidak ditemukan di database, kembalikan None untuk deskripsi
    if breed_info:
        description = breed_info.description
    else:
        description = "Description not available"
    
    return 'uploads/' + filename, predicted_class, description