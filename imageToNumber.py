#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:58:53 2020
@author: duypham
@url: https://github.com/a11to1n3/IntelIDReg
"""

import cv2
import re
import cv2
import os
import pytesseract
from pytesseract import Output
import numpy as np
import argparse

class processing_image():
  def __init__(self,folder,filename):
    img = cv2.imread(os.path.join(folder,filename))
    self.img = img

  def pre_process(self, thresh, thresh_filter):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges_foreground = cv2.bilateralFilter(gray, 9, thresh_filter, thresh_filter)
    (_, blackAndWhiteImage) = cv2.threshold(edges_foreground, thresh, 200, cv2.THRESH_BINARY)
    return blackAndWhiteImage

  def fix_match(self, match):
    match_new = []
    for ch in match:
      if ch == '@' or ch == 'Q':
        match_new.append('0')
      elif ch == '?':
        match_new.append('2')
      else:
        match_new.append(ch)
    match_new = ''.join(match_new)
    print(f"The ID is: {match_new}")
    return match_new

  def recognize_numbers(self):
    match=""
    thresh = 139
    isDilation = [False,True]
    while match == "" and thresh < 180:
      thresh+=1
      # print(thresh)
      thresh_filter = 0
      while match == "" and thresh_filter < 30:
        thresh_filter += 1
        # print(thresh_filter)
        for D in isDilation:
          if match != "":
            break
          blackAndWhiteImage = self.pre_process(thresh, thresh_filter)
          if D:
            kernel = np.ones((2,2),np.uint8)
            blackAndWhiteImage = cv2.dilate(blackAndWhiteImage,kernel,iterations=1)

          d = pytesseract.image_to_data(blackAndWhiteImage, output_type=Output.DICT)
          keys = list(d.keys())

          num_pattern = re.compile("^[\W\w\d]{5}$")

          n_boxes = len(d['text'])
          for i in range(n_boxes):
            if int(d['conf'][i]) > 70 and len(d['text'][i])==5:
              match=d['text'][i]
              if re.match(num_pattern, d['text'][i]):
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                # print(x, y, w, h)
                self.img = cv2.rectangle(self.img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # cv2.imshow(img)
    match_new = self.fix_match(match)
    return match, match_new

if __name__ == '__main__':
  #Construct the argument parser
  ap = argparse.ArgumentParser()
  # Add the arguments to the parser
  ap.add_argument("-folder", "--folder", required=True,
   help="folder name")
  ap.add_argument("-filename", "--filename", required=True,
   help="file name")
  args = vars(ap.parse_args())
  image = processing_image(args['folder'],args['filename'])
  match, match_new = image.recognize_numbers()
