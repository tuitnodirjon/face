import json


import face_recognition

import os
from face_recognition import compare_faces
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
@api_view(['POST'])
def check_image(request):
    if request.method == 'POST':
        data = request.data
        face_img_data = data['face_image']
        base_img_data = data['base_image']
        import base64
        import random
        face_image_name = f"image_{random.randint(1, 10000)}"
        base_image_name = f"image_{random.randint(10001, 100000)}"
        face_decodeit = open(f'{face_image_name}.jpg', 'wb')
        face_decodeit.write(base64.b64decode(face_img_data.split(',')[-1]))
        face_decodeit.close()
        base_decodeit = open(f'{base_image_name}.jpg', 'wb')
        base_decodeit.write(base64.b64decode(base_img_data.split(',')[-1]))
        base_decodeit.close()
        face_image = face_recognition.load_image_file(f'{face_image_name}.jpg')
        base_image = face_recognition.load_image_file(f'{base_image_name}.jpg')
        try:
            face_encoding = face_recognition.face_encodings(face_image)[0]
            base_encoding = face_recognition.face_encodings(base_image)[0]
            results = compare_faces([base_encoding], face_encoding)
        except:
            return Response({'result': False})
        if True in results:
            return Response(json.dumps({'result': True}))
        return Response(json.dumps({'result': False}))


def check_face(request):
    # print("check_face")
    return render(request, 'index.html')
def check_face_image(request):
    if request.method == 'POST':
        # print(json.loads(request.body))
        data = json.loads(request.body)
        img_data = data['image']
        # pinfl = data['pinfl']
        # profile =
        import base64
        import random
        image_name = f"image_{random.randint(1, 100000)}"
        decodeit = open(f'{image_name}.jpg', 'wb')
        decodeit.write(base64.b64decode(img_data.split(',')[-1]))
        decodeit.close()
        image2_test = face_recognition.load_image_file(f'{image_name}.jpg')
        image2_face_encoding = face_recognition.face_encodings(image2_test)[0]
        images = os.listdir('imagesBasic')
        known_face_encodings = []
        known_face_names = []
        for i in images:
            image = face_recognition.load_image_file("imagesBasic/" + i)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(i.split('.')[0])
        results = compare_faces(known_face_encodings, image2_face_encoding)
        print(results)
        if True in results:
            first_match_index = results.index(True)
            name = known_face_names[first_match_index]
            print(name)
        else:
            name = "Unknown"
        return JsonResponse({'name': name})
