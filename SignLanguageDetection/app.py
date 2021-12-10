from flask import Flask, render_template, Response, request, redirect, url_for
from camera import Video
import mediapipe as mp
import cv2
import sys

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html', url = "video")

it =1

def gen(camera, clear):
    sequence = []
    sentence = []
    mp_holistic = mp.solutions.holistic
    i = 0
    global it
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
            frame = camera.get_frame(sequence, sentence, holistic, clear, it)               
            
            print(clear)
            # print(it)
            if clear and i==100:
                it = it + 1
                clear = False
                # break
            
            if i<100:
                i=i+1
                print(i)
            # clear = False
            yield(b'--frame\r\n'
            b'Content-Type:  image/jpeg\r\n\r\n' + frame +
            b'\r\n\r\n')
        cv2.destroyAllWindows()

clear = False
@app.route('/video')
def video():
    clear = True
    return Response(gen(Video(), clear),
    mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/clear')
# def clearText():
#     print("ohohohohohohohghuivuivgiugweufdgbwikefvkgiewgfv")
#     return Response(gen(Video(), clear=True),
#     mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/background_process_test', methods=['GET','POST'])
# def background_process_test():
#     return redirect(url_for('index', url="clear"))



app.run(debug=True)