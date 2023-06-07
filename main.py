from flask import Flask, request, jsonify
import cv2
import dlib
import math
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET'])
def MainAccess():
    response_data = {"message": "Test"}
    return jsonify(response_data)

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Load the dlib shape predictor for facial landmark detection
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

@app.route('/process_image', methods=['GET', 'POST'])
def process_image():
    # Read the image data from the request
    image = request.files['image'].read()

    # Convert the image data to a NumPy array
    nparr = np.frombuffer(image, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Detect the face in the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Initialize boolean variables
    left_defect = False
    right_defect = False
    no_defect = False

    # If a face is detected, detect the facial landmarks and measure the distances
    for (x, y, w, h) in faces:
        # Crop the face region from the frame
        face = frame[y:y+h, x:x+w]

        # Detect the facial landmarks using the dlib shape predictor
        shape = predictor(gray, dlib.rectangle(x, y, x+w, y+h))

        # Extract the x and y coordinates of the left and right eyebrows and the nose tip
        left_eyebrow_x = shape.part(20).x
        left_eyebrow_y = shape.part(20).y
        right_eyebrow_x = shape.part(25).x
        right_eyebrow_y = shape.part(25).y
        nose_tip_x = shape.part(34).x
        nose_tip_y = shape.part(34).y

        # Calculate the distances between the left and right eyebrows and the nose tip
        distance_left_eyebrow_nose_tip = math.sqrt((left_eyebrow_x - nose_tip_x) ** 2 + (left_eyebrow_y - nose_tip_y) ** 2)
        distance_right_eyebrow_nose_tip = math.sqrt((right_eyebrow_x - nose_tip_x) ** 2 + (right_eyebrow_y - nose_tip_y) ** 2)

        # Update boolean variables based on the distances
        if distance_left_eyebrow_nose_tip + 8 < distance_right_eyebrow_nose_tip:
            left_defect = True
        elif distance_right_eyebrow_nose_tip + 8 < distance_left_eyebrow_nose_tip:
            right_defect = True
        elif abs(distance_right_eyebrow_nose_tip - distance_left_eyebrow_nose_tip) <= 8:
            no_defect = True

    # Create a dictionary with the boolean results
    response_data = {
        "left_defect": left_defect,
        "right_defect": right_defect,
        "no_defect": no_defect
    }

    # Return the boolean results as a JSON response
    return jsonify(response_data)

if __name__ == '__main__':
    app.run()
