import cv2
import webbrowser
from deepface import DeepFace
import emoji
from flask import Flask, render_template, request

# Flask App Initialization
app = Flask(__name__)

# Function to Capture Image from Webcam
def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None, "Could not open webcam"

    while True:
        ret, frame = cap.read()
        if not ret:
            return None, "Failed to capture image"

        cv2.imshow("Press ENTER to capture", frame)
        if cv2.waitKey(1) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save captured image
    image_path = 'static/images/Emotion_Pic1.jpg'
    cv2.imwrite(image_path, frame)

    return image_path, None

# Function to Analyze Emotion
def analyze_emotion(image_path):
    try:
        emotions = DeepFace.analyze(image_path, actions=['emotion'])
        return max(emotions[0]['emotion'], key=emotions[0]['emotion'].get)
    except:
        return None

# Flask Routes
@app.route('/')
def index():
    return render_template('input.html')

@app.route('/display', methods=['POST'])
def display():
    language = request.form.get('language', '').strip()
    singer = request.form.get('Singer', '').strip()

    image_path, error = capture_image()
    if error:
        return render_template('error.html', show=emoji.emojize(":confused_face:"))

    emotion = analyze_emotion(image_path)
    if not emotion:
        return render_template('error.html', show=emoji.emojize(":disappointed_face:"))

    emoji_dict = {
        "angry": emoji.emojize(":angry_face:"),
        "fear": emoji.emojize(":face_screaming_in_fear:"),
        "disgust": emoji.emojize(":face_vomiting:"),
        "happy": emoji.emojize(":smiling_face_with_smiling_eyes:"),
        "neutral": emoji.emojize(":neutral_face:"),
        "sad": emoji.emojize(":frowning_face:"),
        "surprise": emoji.emojize(":astonished_face:")
    }

    emotion_emoji = emoji_dict.get(emotion, "")
    search_query = f"https://www.youtube.com/results?search_query={language}+{emotion}+song+{singer.replace(' ', '+')}"

    return render_template('display.html', Link=search_query, feel=emotion, gra=emotion_emoji, show=emoji.emojize(":smiling_face_with_open_hands:"))

# Run Flask App
if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5000')
    app.run(debug=True)

