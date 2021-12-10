import cv2
import mediapipe as mp
import numpy as np
from tensorflow import keras
import sys
import time

model = keras.models.load_model('action.h5')

class Video(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def __del__(self):
        self.video.release()

    def extract_keypoints(self, results):
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
        return np.concatenate([pose, face, lh, rh])

    def mediapipe_detection(self, image, model):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
        image.flags.writeable = False                  # Image is no longer writeable
        results = model.process(image)                 # Make prediction
        image.flags.writeable = True                   # Image is now writeable 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
        return image, results


    def get_frame(self, sequence, sentence, holistic, clear, it):
        actions = np.array(['hello', 'thanks', 'iloveyou'])
        threshold = 0.7
        ret,frame=self.video.read()
        imageOrg, results = self.mediapipe_detection(frame, holistic)
        image = imageOrg.copy()
        keypoints = self.extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:]
        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            #print(actions[np.argmax(res)])

            if res[np.argmax(res)] > threshold: 
                if len(sentence) > 0: 
                    #chceck if new action is different than last to not double translation
                    if actions[np.argmax(res)] != sentence[-1]:
                        sentence.append(actions[np.argmax(res)])
                else:
                    sentence.append(actions[np.argmax(res)])
            # sentence.append(text[i])
            if len(sentence) > 5: 
                sentence = sentence[-5:]            
      
        
        cv2.rectangle(image, (0,0), (640, 40), (24, 159, 121), -1)
        
        if clear and it==2:
            sentence = []
            cv2.rectangle(image, (0,0), (640, 40), (24, 159, 121), -1)
        else:
            cv2.putText(image, ' '.join(sentence), (3,30),cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)


        ret, jpg=cv2.imencode('.jpg', image)

        return jpg.tobytes()
    
