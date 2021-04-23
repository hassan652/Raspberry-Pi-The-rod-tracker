import cv2
import time
import numpy as np
import imutils
import os, sys

class OpenCVController(object):

    def __init__(self):
        self.in_zone = False
        self.xb = xb
        self.yb = yb
        self.wb = wb
        self.hb = hb
        self.xr = xr
        self.yr = yr
        self.wr = wr
        self.hr = hr
        self.directory = os.path.join(os.path.dirname(__file__), 'test')
        print('Open CV Controller initiated')

    def get_frame(self, camera):
        print('Monitoring')
        frame_orig = camera.get_frame()
        jpg_as_np = np.fromstring(frame_orig, np.unit8)
        frame = cv2.imdecode(jpg_as_np, cv2.COLOR_BGR2RGB)

        #convert BGR to HSV
        hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #Masks

        #setting range for blue color and define mask
        blue_lower = np.array([100,150,0])
        blue_upper = np.array([140,255,255])
        blue_mask = cv2.inRange(hsvframe, blue_lower, blue_upper)

        #setting range for red color and define mask

        #lower red range(0 to 10)
        red_lower1 = np.array([0,50,50])
        red_upper1 = np.array([10,255,255])
        red_mask1 = cv2.inRange(hsvframe, red_lower1, red_upper1)

        #upper red range(170 to 180)
        red_lower2 = np.array([170,50,50])
        red_upper2 = np.array([180,255,255])
        red_mask2 = cv2.inRange(hsvframe, red_lower2, red_upper2)

        #defining red mask
        red_mask = red_mask1 + red_mask2

        #Contours
        #Contour for blue mask
        contour_blue = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_blue = imutils.grab_contours(contour_blue)
        contour_blue = sorted(contour_blue, key=cv2.contourArea, reverse=True)[0]

        #Contour for red mask
        contour_red = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_red = imutils.grab_contours(contour_red)
        contour_red = sorted(contour_red, key=cv2.contourArea, reverse=True)[0]

        #Finding perimeter and drawing polygon across the boundary of the required contour
        #for blue
        perimeter = cv2.arcLength(contour_blue, True)
        epsilon = 0.02 * perimeter
        approx = cv2.approxPolyDP(contour_blue, epsilon, True)
        #self.xb, self.yb, self.wb, self.hb = cv2.boundingRect(approx)
        xb, yb, wb, hb = cv2.boundingRect(approx)
        cv2.rectangle(frame, (self.xb, self.yb), (self.xb + self.wb, self.yb + self.hb), (0, 255, 0), 3)
        #for red
        perimeter = cv2.arcLength(contour_red, True)
        approx = cv2.approxPolyDP(contour_red, epsilon, True)
        xr, yr, wr, hr = cv2.boundingRect(approx)
        #self.xr, self.yr, self.wr, self.hr = cv2.boundingrect(approx)
        cv2.rectangle(frame, (self.xr, self.yr), (self.xr + self.wr, self.yr + self.hr), (0, 255, 0), 3)

        #encoding and saving the frame in the as 'temp' in an assigned folder
        frame_ret = cv2.imencode('.jpg', frame)
        st = self.directory + os.sep + 'temp.jpg'
        print(st)
        cv2.imwrite(st, frame)
        retval = open(os.path.join, 'rb').read()
        return retval

    def is_in_zone(self):
        left_bottom_corner = (self.xr>self.xb and self.xr<self.xb+self.wb and self.yr>self.yb and self.yr<self.yb+self.hb)
        right_bottom_corner = (self.xr+self.wr>self.xb and self.xr+self.wr<self.xb+self.wb and self.yr>self.yb and self.yr<self.yb+self.hb)
        if left_bottom_corner or right_bottom_corner:
            self.in_zone = True
        else:
            self.in_zone = False
        return self.in_zone




