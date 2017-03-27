"""
    SECRONE GOOGLE CLOUD VISION API
    IMAGE CAPTURE AND PROCESS SCRIPT 
"""
import argparse
import base64
import picamera
import json
import datetime

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def initCamera():
    camera = picamera.PiCamera()
    camera.exposure_mode ='sports'
    print('Camera initialized..')
    return camera

def caprureImage(camera):
    imageName = 'img-' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.jpg'
    camera.capture(imageName)
    print('"' + imageName + '" - Captured!')
    return imageName

def visionRequest(reqImageName):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials = credentials)
    with open(reqImageName, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body = {
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [
                    {
                        'type': 'LABEL_DETECTION'
                    },
                    {
                        'type': 'LOGO_DETECTION'
                    },
                    {
                        'type': 'TEXT_DETECTION'
                    },
                    {
                        'type': 'FACE_DETECTION'
                    }
                ]
            }]
        })
        print('Executing request..')
        response = service_request.execute()
        print('Done!')
        return response

def main():
    camera = initCamera()
    print('\n')

    cnt = 1
    while cnt > 0:
        response = visionRequest(caprureImage(camera))
        print json.dumps(response, indent=4, sort_keys=True)
        print('###############################################')
        print('\n')

if __name__ == '__main__':

    main()
