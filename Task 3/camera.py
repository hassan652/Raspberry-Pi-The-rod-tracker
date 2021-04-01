#fake camera created to check whether the code is okay for the realtime video which will be obtained from a camera attached to Raspberry Pi.
#Yields one of the four images in the folder test
#Only for testing purposes

import time
import os, sys

class Camera(object):

    def __init__(self):
        directory = os.path.join(os.path.dirname(__file__), 'test')
        self.test_frame_name = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']
        self.frames = [open(os.path.join(directory, f), 'rb').read() for f in self.test_frame_name]

    def get_frame(self):
        random_index = int(time()) % 4    #gives a random value to be picked from 4 frames available in the test folder
        print (f'frame {self.test_frame_name[random_index]}')
        return self.frames[random_index]