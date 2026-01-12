from picamera2 import Picamera2, Preview
from time import sleep
picam0 = Picamera2(0)
picam1 = Picamera2(1)

capture_main = {"size": (3840, 2160),"format": "RGB888"}
capture_config = picam0.create_still_configuration(main=capture_main)
capture_config1 = picam1.create_still_configuration(main=capture_main)


#picam0.start_preview(Preview.QTGL)
#picam1.start_preview(Preview.QTGL)
picam0.configure(capture_config)
picam1.configure(capture_config1)


picam0.start()
picam1.start()
sleep(10)
picam0.capture_file("cam0.jpg")
picam1.capture_file("cam1.jpg")
picam0.stop()
picam1.stop()
picam0.stop_preview()
picam1.stop_preview()
