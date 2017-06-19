# coding: utf-8
# PYTHONIOENCODING=utf-8 python ocr_sample.py

import cv2
import numpy as np
import os
import pyocr
import re
import pyocr.builders
import codecs
from PIL import Image
from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed

DATA_DIR = "./data"

def prepare_dir(root):
    # FIXME: 'original' use as magic word, but if root dir include 'original', it will happen bug.
    dir = root.replace("original", "custom")
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir

def resize_to_xx_times(file, dir, range=xrange(5)):
    for time in range:
        im = cv2.imread(DATA_DIR + "/original/" + file)
        gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        _, threshold_im = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        height, width = threshold_im.shape[:2]
        # add padding : tesseract needs enough spaceas for recognition.
        padding_im = cv2.resize(np.zeros((1, 1), np.uint8), (width+20, height+20))
        # backgroaund change white
        padding_im[:] = 255
        padding_im[10:height+10, 10:width+10] = threshold_im
        resized_im = cv2.resize(padding_im, None, fx = time + 1, fy = time + 1)            
        cv2.imwrite(dir + "/" + str(time + 1) + ".jpg", resized_im)

def extract_ocr(dir):
    for file in os.listdir(dir):
        yield pyocr_tool().image_to_string(
            Image.open(dir + "/" + file),
            lang="jpn+eng",
            builder=pyocr.builders.TextBuilder()
        )

def pyocr_tool():
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR found")
        exit
    return tools[0]

def _inference(text):
    conference = [(u"三" in text), (u"京" in text), (u"U" in text)]
    if np.count_nonzero(conference) >= 2:
        return "green"

    if np.count_nonzero(conference) == 1:
        return "yellow"
    
    return None

def _output(dir, file, text, answer):
    # WARNING: catch exception
    output_file = file.split(".")[0] + ".csv"
    with codecs.open(dir + "/" + output_file, "w", "utf-8") as f:
        f.write(answer + ", " + text)

if __name__ == '__main__':
    for root, dirs, files in os.walk(DATA_DIR + "/original"):
        current_dir = prepare_dir(root)
        for file in files:
            answer, text = None, None
            resize_to_xx_times(file, current_dir)
            for t in extract_ocr(current_dir):
                current_answer = _inference(t)
                if current_answer == "green":
                    text = t
                    answer = "green"
                    break

                if current_answer == "yellow" and answer == None:
                    answer = "yellow"
                    text = t
                    continue
                
                if current_answer == None and answer == None:
                    text = t
                    continue

            _output(current_dir, file, text, answer)
