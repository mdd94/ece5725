import data_to_send
import time

for i in range(10):
    pic = data_to_send.capture_photo()
    print(pic, flush=True)
    time.sleep(0.1)