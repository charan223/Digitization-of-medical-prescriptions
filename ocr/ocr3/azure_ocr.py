
# azure_ocr.py
# Python 3.5

"""
Python script to analyze and read text from image URLs using Micorost Azure Cognitive services OCR API
"""

#from IGNORE import azure_secrets  # To fetch API endpoint and key
from __future__ import print_function
from base64 import b64encode
from os import makedirs, remove
from os.path import join, basename
from sys import argv
import json
import requests
import glob
from unidecode import unidecode
import http.client
'''
headers = {
    # Request headers.
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": azure_secrets.api["key1"],
}

headers = {
    # Request headers
    'Content-Type': 'application/json'
}
'''
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'XXXXXXX', 
} 
def make_image_data_list(image_filenames):
    """
    image_filenames is a list of filename strings
    Returns a list of dicts formatted as the Vision API
        needs them to be
    """
    img_requests = []
    with open(image_filenames, 'rb') as f:
        ctxt = b64encode(f.read()).decode()
        img_requests.append({
                'image': {'content': ctxt},
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': 1
                }]
        })
    return img_requests

def make_image_data(image_filenames):
    """Returns the image data lists as bytes"""
    imgdict = make_image_data_list(image_filenames)
    return json.dumps({"requests": imgdict }).encode()


def detect_text_from_image_url(img_filename):
    """
    Given an image url, detect the text
    """
    '''
    # Query parameters to analyze image
    params = {
    # Request parameters. The language setting "unk" means automatically detect the language.
    'language': 'unk',
    'detectOrientation ': 'true',
    }

    # https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/ocr"
    resp = requests.post("https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/ocr", data=make_image_data(img_filename), params = params, headers=headers)
    '''
 
    body = open('check.jpg', "rb").read()
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/ocr?%s" % body, headers)
    resp = conn.getresponse()
    data = resp.read() 
    print(data)
    conn.close()
    resp.raise_for_status()
    # print(resp.url)

    parsed = json.loads(resp.text)

    # Text description of the image
    # print (json.dumps(parsed, sort_keys=True, indent=2))
    
    result = list()

    for region in parsed["regions"]:
        for line in region["lines"]:
            for word in line["words"]:
                result.extend([word["text"]])

    return " ".join(result)


if __name__ == "__main__":
        # detect text from url
        print (detect_text_from_image_url('check.jpg'))

'''

########### Python 2.7 #############
import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '{subscription key}',
}

params = urllib.urlencode({
    # Request parameters
    'handwriting': 'true',
})

with open('check.jpg', 'rb') as f:
    	img_data = f.read()

conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
conn.request("POST", "/vision/v1.0/recognizeText?%s" % params, "{body}", headers, data=img_data)
response = conn.getresponse()
data = response.read()
print(data)
conn.close()


####################################
'''
