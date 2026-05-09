import cv2, face_recognition, pickle, pyttsx3

# Load DB
with open("faces_db.pkl", "rb") as f:
    known_encodings, known_names = pickle.load(f)

engine = pyttsx3.init()  # text-to-speech

def speak(text):
    engine.say(text)
    engine.runAndWait()

cap = cv2.VideoCapture(0)
greeted = set()  # avoid repeating greetings

while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    for enc, loc in zip(encodings, locations):
        matches = face_recognition.compare_faces(known_encodings, enc, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            name = known_names[matches.index(True)]
            if name not in greeted:
                speak(f"Hello {name}, welcome!")
                greeted.add(name)
        else:
            speak("Hello! I don't recognize you. What's your name?")
            # Optionally: capture input and enroll

        # Draw box + label
        top, right, bottom, left = loc
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 200, 100), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 100), 2)

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()