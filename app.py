from flask import Flask, Response, render_template, jsonify
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load the trained model
model = load_model("mymodel.h5")

# Load the camera
camera = cv2.VideoCapture(0)  # Ensure this is the correct index for your camera

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_sign')
def get_sign():
    success, frame = camera.read()
    if not success:
        return "No Camera Input"

    # Preprocess the frame (Modify based on your model’s input format)
    resized_frame = cv2.resize(frame, (64, 64))  # Adjust size as needed
    normalized_frame = resized_frame / 255.0
    reshaped_frame = np.expand_dims(normalized_frame, axis=0)  # Add batch dimension

    # Make a prediction
    predictions = model.predict(reshaped_frame)
    sign_index = np.argmax(predictions)
    sign_labels = ["Hello", "Yes", "No"]  # Update with your actual labels
    detected_sign = sign_labels[sign_index]

    return jsonify(detected_sign)

if __name__ == "__main__":
    app.run(debug=True)


