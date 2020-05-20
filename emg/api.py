from flask import Blueprint, request, json, jsonify, make_response
from flask_login import login_required, current_user
from . import db
from .facial_recognition import FaceRecognition
import PIL.Image
import numpy as np
import base64

api = Blueprint('api', __name__)
PRETRAINED_68 = "/home/jordy/EMG/emg/pretrained_model/shape_predictor_68_face_landmarks.dat"
REGOGNITION_MODEL = "/home/jordy/EMG/emg/pretrained_model/dlib_face_recognition_resnet_model_v1.dat"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
facial = FaceRecognition(PRETRAINED_68, REGOGNITION_MODEL)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/api/recognition', methods=['POST'])
def recognition():
    new_img = base64.b64decode(request.form['img'])
    # print(new_img.fi)
    # if 'img' not in request.files:
    #     return make_response(jsonify({'message':'aucune image envoyée'}), 400)

    # _file = request.files['img']

    # if _file.filename == '':
    #    return make_response(jsonify({'message':'aucune image envoyée'}), 400)
    
    # if _file and allowed_file(_file.filename):
    personne_info, faces_found = facial.face_reco(new_img)
    r = {'faces': faces_found, 'known_faces': personne_info }
    # r['faces'] = "{}".format(faces_found)
    # r['known_faces'] = "{}".format(personne_info)

    print(r)

    return r