import numpy as np
import cv
import cv2
import serial
from picamera import PiCamera
from time import sleep
from matplotlib import pyplot as plt
import os

ser = serial.Serial('/dev/ttyACM0', 57600)

camera = PiCamera()

camera.resolution = (800,400)


def im_trim (img) : 
    x = 318; y = 199
    w = 222; h = 165
    img_trim = img[y:y+h, x:x+w]
    cv2.imwrite('/Auth/%04d.png' % nID, img_trim)
    return img_trim

#Local Binary Pattern Filter
def LBP_Img(img):
    """
    calculate LBP (Local Binary Pattern) image N8 neighborhood
    """
    sz = cv.GetSize(img)
    gr = cv.CreateImage(sz, 8, 1)
    lbp = cv.CreateImage(sz, 8, 1)
     
    #convert to grayscale
    cv.CvtColor(img, gr, cv.CV_BGR2GRAY)
 
    LBPMASK = [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,-1),(-1,0),(-1,1)]
     
    for y in xrange(1, sz[1]-2):
        for x in xrange(1, sz[0]-2):
            n = 0
            gv = gr[y,x]
            for i in xrange(len(LBPMASK)):
                m = LBPMASK[i]
                if gr[y+m[1], x+m[0]]>gv:
                    n += 1 << i
            lbp[y,x] = n
             
    return lbp
    
def TemplateMat():
    img1 = LBP_Result
    img2 = img1.copy()
    
    fname = '/home/pi/project/Auth/{0:04}.png' .format(nID)
    
    template = cv2.imread(fname)
    
    #Template img size
    w, h = template.shape[::-1]
    
    #Template Match Method
    method  = ['cv2.TM_CCORR']
    
    for meth in methods :
        img1 = img2.copy()
        method = eval(meth)
        
        try:
            res = cv2.matchTemplate(img1, template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        except:
            print('error', meth)
            continue
        top_left = max_loc
         
        bottom_right = (top_left[0]+w, top_left[1]+h)
        cv2.rectangle(img, top_left, bottom_right, 255, 2)
        if(cv2.rectangle) :
            Temp = 1
        else :
            Temp = 0
    return Temp

nProcess = 2
a = 2
nAc_Count = 0
nID = 1
nImages = 256
Temp = 0
nDelete_cashe = 0

while a == 0 :
    a = input()
    nProcess = a


if nProcess == 1:
    nAc_Count = 3
    
    while nAc_Count != 0 :
        if nID >= nImages or nID <= 0:
            print("Default")
            nAc_Count = nAc_Count - 1
        else :
            camera.capture('/home/pi/project/cache/cache.png')
            camera.resolution = (800,400)
            img = cv2.imread('/home/pi/project/cache/cache.png')
                       
            gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
            gray_img = im_trim(gray)
            LBP_Result = LBP_Img(gray_img)
            if img is not None :
                print("Can't find Image") 
                nAc_Count = nAc_Count -1
                if nAc_Count == 0 :
                    break
                    
            else :
                TemplateMat()
                if Temp == 1 : 
                    print('ACCESS')
                else :
                    print('Default')
                    nAc_Count = nAc_Count - 1
                if nAc_Count == 0 :
                    break

elif nProcess == 2 :
    if nID >= nImages or nID <= 0:
        print('Can not Enroll  ')
    else :
        camera.capture('/home/pi/project/cache/cache.png')
        camera.resolution = (800,400)
        img = ('/home/pi/project/cache/cache.png')

        gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

        gray_img = im_trim(gray)
        cv2.imshow('capture', gray_img)
        LBP_Result = LBP_Img(gray_img)
        cv2.imshow('LBP', LBP_Result)
        fname = '/home/pi/project/Auth/{0:04}.png' .format(nID)
        if img is not None :
            cv2.imwrite(fname, LBP_Result)
            print('Save Success    ')
        else :
            print('Image was exist ')
            

elif nProcess == 3 :
    for nDelete_cashe in range(1, nImages) :
        fname = '/home/pi/project/Auth/{0:04}.png' .format(nDelete_cashe)
        if os.path.isfile(fname) :
            os.remove(fname)
    print('Reset Complete!!')


else : 
    a = 0;
    
cv2.waitKey(10000)
cv2.destroyAllWindows()
