import numpy as np
import cv2
import serial
import picamera import PiCamera
from time import sleep

ser = serial.Serial('/dev/ttyACM0', 57600)

camera = PiCamera()

camera.resolution = (800,400)

#이미지 부분추출
def im_trim (img) : 
    x = 318; y = 199
    w = 222; h = 165
    img_trim = img[y:y+h, x:x+w] #잘라낸 결과를 img에 저장
    cv2.imwrite('/Auth/%04d.png' % nID, img_trim)
    return img_trim

#Local Binary Pattern Filter
def LBP_Img(img):
    size2, size1 = img.shape
    numbers = []
    dx = 8
    dy = 8
    cell_x = 16
    cell_y = 16
    x = 0
    y = 0
    
    hist_list = []
    while  y + cell_y  <= size2:
        for i in range(y, y + cell_y):
            for j in range(x, x + cell_x):
                
                hood = np.zeros((3,3), dtype = int)
                
                if j == 0 and i == 0:
                    hood[1:3, 1:3] = img[i:i+2, j:j+2]
                    
                elif i == 0 and j == size1 - 1:
                    hood[1:3, 0:2] = img[i:i+2, j-1:j+1]
                       
                elif j == 0 and i == size2 - 1:
                    hood[0:2, 1:3] = img[i-1:i+1, j:j+2]
                            
                elif i == size2 - 1 and j == size1 - 1:
                                hood[0:2, 0:2] = img[i-1 : i+1, j-1:j+1]
                                
                elif i == 0:
                    hood[1:3,0:3] = img[i:i+2, j-1:j+2]
                                    
                elif j == 0:
                    hood[0:3, 1:3] = img[i-1:i+2, j:j+2]

                elif i == size2 - 1:
                    hood[0:2, 0:3] = img[i-1 : i+1, j-1:j+2]      

                elif j == size1 - 1:
                    hood[0:3, 0:2] = img[i-1 : i+2, j-1:j+1]
                                                
                else:
                    hood = img[i-1 : i+2, j-1:j+2]
                                                    
                ordered_hood = np.concatenate((hood[0], [hood[1,2], hood[2,2], hood[2,1], hood[2,0], hood[1,0]]))
                                                    
                for k in range(len(ordered_hood)):
                    if ordered_hood[k] < hood [1,1]:
                        ordered_hood[k] = 0
                    else:
                        ordered_hood[k] = 1
                                                                
                    binary = ""
                    for digit in ordered_hood:
                        binary += str(digit)
                    integer = int(binary, 2)
                    numbers.append(integer)

        hist = np.zeros(256)
        for l in numbers:
            hist[l] += 1
            hist_list = np.concatenate((hist_list, hist))

        if x + dx + cell_x > size1:
            x = 0
            y = y + dy
        else:
            x = x + dx
    return hist_list
    
def TemplateMat():
    img1 = Pic
    img2 = img1.copy()
    
    template = LBP_Result(gray)
    
    #Template img size
    w, h = template.shape[::-1]
    
    #Template Match Method
    method  = ['cv2.TM_CCORR']
    
    for meth in methods :
        img1 = img2.copy()
        method = eval(meth)
        
        try:
            res = cv2matchTemplate(img1, template, method)
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

nProcess = 0
a = 0
nAc_Count = 0
nID = 0
nImages = 256
Temp = 0
nDelete_cashe = 0

while a == 0 :
    a = input()
    nProcess = a

#인증절차
if nProcess == 1:
    nAc_Count = 3
    #nID = 아두이노에서 입력받은 ID
    while nAc_Count != 0 :
        if nID >= nImages or nID <= 0:
            print("Default")
            nAc_Count = nAc_Count - 1
        else :
            #카메라에서 이미지 촬영 후 dir cache에 저장
            camera.capture('/home/pi/project/cache.png')
            img = cv2.imread('/home/pi/project/cache.png')
            
            #카메라이미지불러오기
            gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            gray = im_trim(gray)
            LBP_Result = LBP_Img(gray)
            if(img.empty()) :
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
#등록절차
elif nProcess == 2 :
    if nID >= nImages or nID <= 0:
        print('Can not Enroll  ')
    else :
        #카메라에서 이미지 가져오는걸로 수정해야함
        camera.capture('/home/pi/project/cache.png')
        img = cv2.imread('/home/pi/project/cache.png'
            
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        gray = im_trim(gray)
        LBP_Result = LBP_Img(gray)

        fname = '/Auth/%4d.png' %(nID)
        if img.empty() : 
            cv2.imwrite(fname, LBP_Result)
            print('Save Success    ')
        else :
            print('Image was exist ')
            

#초기화절차
elif Process == 3 :
    for nDelete_cashe in range(1, nImages) :
        fname = '/Auth/%4d.png' %(nDelete_cashe)
        if os.path.isfile(fname) :
            os.remove(fname)
    print('Reset Complete!!')


else : 
    a = 0;
    
cv2.waitKey(1000)
cv2.destroyAllWindows()
