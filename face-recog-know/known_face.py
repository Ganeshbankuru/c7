import face_recognition, os, pickle

known_encodings = []
known_names = []

for img_file in os.listdir("known_faces/"):
    img = face_recognition.load_image_file(f"known_faces/{img_file}")
    enc = face_recognition.face_encodings(img)
    if enc:
        known_encodings.append(enc[0])
        known_names.append(os.path.splitext(img_file)[0])  # filename = person's name

# Save for reuse
with open("faces_db.pkl", "wb") as f:
    pickle.dump((known_encodings, known_names), f)