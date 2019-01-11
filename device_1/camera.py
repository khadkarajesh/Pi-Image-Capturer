from picamera import PiCamera
import time

class Camera:

    def __init__(self):
        self.camera_state = False
        self.camera = PiCamera()
        print('cammera instantiated')

    def start_preview(self):
        print("preview started")
        self.camera_state = True
        self.camera.start_preview()

    def capture(self, path):
        file_name = '{}.jpg'.format(str(uuid.uuid4()))
        path =  path + file_name
        self.camera.capture(path)
        

    def stop_preview(self):
        self.camera_state = False
        self.camera.stop_preview()
        self.camera.close()
        print('preview stopped')

    def close_camera():
        print("camera closed")
        self.camera.close()
