import cv2
import dlib
import PIL.Image
import face_recognition
import numpy as np
from imutils import face_utils
#import argparse
from pathlib import Path
import os
import ntpath
from . import db
from .models import Personne

class FaceRecognition(object):

    def __init__(self, PRETRAINED_68, REGOGNITION_MODEL):
        self.pose_predictor_68_point = dlib.shape_predictor(PRETRAINED_68)
        self.face_encoder = dlib.face_recognition_model_v1(REGOGNITION_MODEL)
        self.face_detector = dlib.get_frontal_face_detector()


    def transform(self, image, face_locations):
        coord_faces = []
        for face in face_locations:
            rect = face.top(), face.right(), face.bottom(), face.left()
            coord_face = max(rect[0], 0), min(rect[1], image.shape[1]), min(rect[2], image.shape[0]), max(rect[3], 0)
            coord_faces.append(coord_face)

        return coord_faces

    def get_all_faces(self):
        personnes = Personne.query.filter(Personne.img_path != None).all()

        return personnes

    def known_faces_encode(self):
        known_face_encodings = []
        known_face_encodings_ids = []
        for personne in self.get_all_faces():
            image = PIL.Image.open(personne.img_path)
            image = np.array(image)
            face_encoded = self.encode_face(image)[0][0]
            known_face_encodings.append(face_encoded)
            known_face_encodings_ids.append(personne.id)

        return known_face_encodings, known_face_encodings_ids

    def encode_face(self, image):
        face_locations = self.face_detector(image, 1)
        face_encodings_list = []
        landmarks_list = []
        for face_location in face_locations:
            # DETECT FACES
            shape = self.pose_predictor_68_point(image, face_location)
            face_encodings_list.append(np.array(self.face_encoder.compute_face_descriptor(image, shape, num_jitters=1)))
            # GET LANDMARKS
            shape = face_utils.shape_to_np(shape)
            landmarks_list.append(shape)
        face_locations = self.transform(image, face_locations)

        return face_encodings_list, face_locations, landmarks_list

    def face_reco(self, image):
        # nparr = np.fromstring(image.read(), np.uint8)
        nparr = np.fromstring(image, np.uint8)
        rgb_small_frame = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        known_face_encodings, known_face_encodings_ids = self.known_faces_encode()
        # ENCODING FACE
        face_encodings_list, face_locations_list, landmarks_list = self.encode_face(rgb_small_frame)
        faces_found = 0
        personne_info = []
        for face_encoding in face_encodings_list:
            if len(face_encoding) == 0:
                return np.empty((0))
            # CHECK DISTANCE BETWEEN KNOWN FACES AND FACES DETECTED
            vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
            tolerance = 0.45
            result = []
            for vector in vectors:
                print(vector)
                if vector <= tolerance:
                    result.append(True)
                else:
                    result.append(False)
            if True in result:
                first_match_index = result.index(True)
                id = known_face_encodings_ids[first_match_index]
                p = getPersonne(id)
                personne_info.append({'id':p.id, 'name': p.name, 'firstname': p.first_name})
                faces_found = faces_found + 1
            else:
                u_name = "Unknown"
                faces_found = faces_found + 1

        return personne_info, faces_found

def getPersonne(id):
    personne = Personne.query.filter_by(id=id).first()
    return personne
