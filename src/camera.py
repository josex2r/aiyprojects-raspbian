from time import sleep
from picamera import PiCamera
import picamera

# camera = PiCamera()
# camera.resolution = (1024, 768)
# camera.start_preview()
# Camera warm-up time
# sleep(2)
# camera.capture('../image.jpg')


# camera = PiCamera()
# camera.start_preview()
# sleep(2)
# for filename in camera.capture_continuous('../tmp/img{counter:03d}.jpg'):
#     print('Captured %s' % filename)
#     sleep(2) # wait 5 seconds


camera = picamera.PiCamera()
camera.resolution = (1024, 768)
camera.start_recording('../tmp/my_video.h264')
camera.wait_recording(5)
camera.stop_recording()
