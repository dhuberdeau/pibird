from picamera2 import Picamera2, Preview
import time
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(buffer_count=2)
picam2.configure(camera_config)
picam2.start_preview(Preview.NULL)
picam2.start()
time.sleep(2)
picam2.capture_file("test.jpg")
picam2.stop()
