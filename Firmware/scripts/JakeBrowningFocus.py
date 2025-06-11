import time
from picamera2 import Picamera2
from libcamera import controls

def print_af_state(request):
    md = request.get_metadata()
    print(("Idle", "Scanning", "Success", "Fail")[md['AfState']], md.get('LensPosition'))

picam2 = Picamera2()
#preview_config = picam2.create_preview_configuration(main={'format': 'RGB888', 'size': (1920*2, 1080*2)})
preview_config = picam2.create_preview_configuration(main={'format': 'RGB888', 'size': (4624, 3472)})

still_config = picam2.create_still_configuration(main={"size": (9000, 6000), "format": "RGB888"}, buffer_count=1)
picam2.configure(preview_config)
picam2.pre_callback = print_af_state
picam2.start()
print('Started')
picam2.set_controls({"AfMode":controls.AfModeEnum.Continuous})
start_time = time.time()
success = picam2.autofocus_cycle()
print(f'Autofocused: {success}, {time.time() - start_time}s')
picam2.switch_mode_and_capture_file(still_config, 'test.jpg')
picam2.stop()