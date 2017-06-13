import cv2
import numpy as np
import os

DATA_DIR = "./data"

def prepare_dir(file):
    basename, _ = os.path.splitext( os.path.basename(file) )
    dir = DATA_DIR + "/" + basename
    if not os.path.exists(dir):
        os.makedirs(dir)

    return dir

def resize_to(file, dir, range=xrange(5)):
    for time in range:
        im = cv2.imread(DATA_DIR + "/original/" + file)
        gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        _, threshold_im = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)        
        resized_im = cv2.resize(gray, None, fx = time + 1, fy = time + 1)            
        cv2.imwrite(dir + "/" + str(time + 1) + ".jpg", resized_im)

    
if __name__ == '__main__':
    for file in os.listdir(DATA_DIR + "/original"):
        current_dir = prepare_dir(file)
        resize_to(file, current_dir)
        print current_dir

