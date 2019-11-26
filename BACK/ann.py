import face_recognition

def face():
    image = face_recognition.load_image_file("table.jpg")
    face_locations = face_recognition.face_locations(image)
    print (face_locations)

    return face_locations
