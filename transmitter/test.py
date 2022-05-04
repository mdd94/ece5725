
import data_to_send

# test the functions
for i in range(10):
    data_to_send.calibration_light()
    data_cam = data_to_send.camera_scanner()
    print(data_cam)
    data_dht11 = data_to_send.temp_and_hum_capture()
    print(data_dht11)
