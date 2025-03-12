from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__)
model = load_model("mymodel.h5")
predicted_sign = "Waiting..."

def process_frame(frame):
    """ Process frame to detect hand and predict sign language. """
    global predicted_sign
    resized_frame = cv2.resize(frame, (64, 64)) / 255.0
    prediction = model.predict(np.expand_dims(resized_frame, axis=0))
    predicted_class = np.argmax(prediction)
    predicted_sign = str(predicted_class)  # Replace with actual label mapping if available
    return predicted_class

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        process_frame(frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_sign')
def get_sign():
    return jsonify(predicted_sign)

if __name__ == "__main__":
    app.run(debug=True)
