import cv2
import webbrowser
from deepface import DeepFace
import emoji as emoj
from flask import Flask, render_template , request
language=""
Singer=""
Li=""
feeling=""
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('input.html')
@app.route('/display', methods=['POST'])
def display():
        language = request.form['language']
        Singer = request.form['Singer']
        print("FINE NOW LETS SEE YOUR MOOD TODAY ^_^ ")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
           print("Could not open webcam")
           exit()
        ret, frame = cap.read()
        cv2.namedWindow("<<<<<<PRESS ENTER KEY ONCE DONE>>>>>>", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("<<<<<<PRESS ENTER KEY ONCE DONE>>>>>>", 900,700)
        while True:
           ret, frame = cap.read()
           if ret:
             #cv2.setWindowProperty("<<<<<<PRESS ENTER KEY ONCE DONE>>>>>>", cv2.WND_PROP_TOPMOST, 1)
             cv2.imshow("<<<<<<PRESS ENTER KEY ONCE DONE>>>>>>", frame)
           if cv2.waitKey(1) == 13:
             break
        cap.release()
        cv2.destroyAllWindows()
        cv2.imwrite('Emotion_Pic.jpg', frame)
        cv2.imwrite(r'C:\Users\ARNAB MONDAL\PycharmProjects\1st SEMESTER Python\Static\images\Emotion_Pic1.jpg', frame)
        image = cv2.imread('Emotion_Pic.jpg')
        cap.release()
        cv2.destroyAllWindows()
        img = cv2.imread(r"Emotion_Pic.jpg")
        try:
          Emotional_Result = DeepFace.analyze(img, actions = ['emotion'])
        except ValueError:
          #print("Sorry your face *_* could not be detetcted ",emoj.emojize(":disappointed_face:"))
          return render_template('Error.html', show=emoj.emojize(":confused_face:") )
          webbrowser.open_new('http://127.0.0.1:5000')
        else :

           print(Emotional_Result)
           feeling = str(max(zip(Emotional_Result[0]['emotion'].values(),
					Emotional_Result[0]['emotion'].keys()))[1])
           Dict={"angry":(emoj.emojize(":angry_face:")),"fear":(emoj.emojize(":face_screaming_in_fear:")),"disgust":(emoj.emojize(":face_vomiting:")),"happy":(emoj.emojize(":smiling_face_with_smiling_eyes:")),"neutral":(emoj.emojize(":neutral_face:")),"sad":(emoj.emojize(":frowning_face:")),"surprize":(emoj.emojize(":astonished_face:"))}
           print(Dict)
           for j in Dict:
             if(j==feeling):
               print(f'Your mood is {feeling} {Dict[j]}')
               break
        Singer=Singer.strip()
        NSinger=Singer.replace(" ","+")
        print(NSinger)
        Li="https://www.youtube.com/results?search_query=+"+language+"+"+feeling+"+song+"+NSinger
        return render_template('display.html', Link=Li , feel=feeling , gra=Dict[j] , show=emoj.emojize(":smiling_face_with_open_hands:") )
if __name__ == '__main__':
  webbrowser.open_new('http://127.0.0.1:5000')
  app.run()
