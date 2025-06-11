import time
from picamera2 import Picamera2, Preview

picam2 = Picamera2()
#picam2.start_preview(Preview.QTGL)
#preview_config = picam2.create_preview_configuration({"format": "YUV420"})
capture_config = picam2.create_still_configuration({"format": "YUV420"})
picam2.configure(capture_config)
picam2.start()
time.sleep(2)

array = picam2.switch_mode_and_capture_array(capture_config)
