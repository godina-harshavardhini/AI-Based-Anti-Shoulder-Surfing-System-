import face_recognition
import os
import pickle

known_faces_dir = "known_faces"
encodings = []

for filename in os.listdir(known_faces_dir):
    path = os.path.join(known_faces_dir, filename)
    image = face_recognition.load_image_file(path)
    face_enc = face_recognition.face_encodings(image)

    if face_enc:
        encodings.append((filename, face_enc[0]))

# Save encodings
with open("known_faces_encodings.pkl", "wb") as f:
    pickle.dump(encodings, f)

print(f"Saved {len(encodings)} trusted face encodings.")
