# coding: UTF-8
from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import numpy as np
import requests
import urllib
import cv2
import dlib

# Create your views here

def response(request):
  url = request.GET.get("i", "")
  width = int(request.GET.get("w", 0))
  height = int(request.GET.get("h", 0))
  quarity = int(request.GET.get("quarity", 95))
  return Face().renderer(url, width, height, quarity)


class Face:
  def renderer(self, url, width, height, quarity):
    image = self.fetch_image(url)
    return self.make_response(self.process(image))

  def decode(self, img_array):
     img = cv2.imdecode(img_array,1)
     result, encimg = cv2.imencode(".jpeg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
     return cv2.imdecode(encimg, 1)

  def fetch_image(self, url):
    url = urllib.parse.unquote(url)
    res = requests.get(url)
    return res.content

  def make_response(self, image):
    response = HttpResponse(content_type="image/jpeg")
    image.save(response, "jpeg")
    return response

  def process(self, image):
    img_array = np.asarray(bytearray(image), dtype=np.uint8)
    img = self.decode(img_array)
    img = self.detect(img)
    img = self.cv_detect(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)
#dlib
  def detect(self, img):
    detector = dlib.get_frontal_face_detector()
    dets, scores, idx = detector.run(img, 0)
    for i, rect in enumerate(dets):
        cv2.rectangle(img, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0,0,255), thickness=5)
    return img
# OpenCV
  def cv_detect(self, img):
      cascade_fn = "/var/www/haarcascade/haarcascade_frontalface_alt.xml"
      cascade = cv2.CascadeClassifier(cascade_fn)
      facerect = cascade.detectMultiScale(img)
      for (x, y, w, h) in facerect:
          cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), thickness=5)
      return img
