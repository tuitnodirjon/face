import json


import face_recognition

import os
from face_recognition import compare_faces
from django.http import JsonResponse
from django.shortcuts import render


def check_face(request):
    # print("check_face")
    return render(request, 'index.html')
def check_face_image(request):
    if request.method == 'POST':
        # print(json.loads(request.body))
        data = json.loads(request.body)
        img_data = data['image']
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
