from flask import Flask, url_for, render_template, request, redirect, url_for, session, flash, jsonify
import joblib
from request_to_arduino_sender import send_request_to_arduino
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/controll', methods=['GET', 'POST'])
def upload_voice_text():    
    data = request.get_json()
    try:
        speech = list()
        speech.append(data['speech'])

        # Load vectorizer và mô hình
        loaded_vectorizer = joblib.load('text_vectorizer.joblib')
        loaded_model = joblib.load('action_classification.joblib')

        # Vector hóa dữ liệu mới
        new_text_vectorized = loaded_vectorizer.transform(speech)

        # Dự đoán với mô hình đã load
        predictions = loaded_model.predict(new_text_vectorized)
        predict_value = predictions[0]
        print(predictions, predict_value)
        
        switcher = {
            1: "forward",
            2: "left",
            3: "right",
            4: "backward",
            5: "rotate",
            6: "stop",
        }

        controll_require = switcher.get(predict_value, "Unknown command")
        send_request_to_arduino(controll_require)

        return jsonify({"controll_require": controll_require})
    except:
        print("Exception")
        return "Invalid request data", 400

@app.route('/upload-image', methods=['GET'])
def upload_image():    
    # Chuyển đổi dữ liệu hình ảnh từ base64 sang numpy array
    # image_data = request.get_json().get('image')
    # image_data = base64.b64decode(image_data.split(',')[1])
    # image = Image.open(BytesIO(image_data))
    # image = np.array(image)

    # Xử lý nhận diện khuôn mặt ở đây

    return jsonify({'message': 'Khuôn mặt được nhận diện'})

if __name__ == "__main__":
    app.run(debug=True)