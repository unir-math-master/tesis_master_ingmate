from csi_camera import CSI_Camera
import time
import cv2

camera = CSI_Camera()

camera.create_gstreamer_pipeline()

camera.open(camera.gstreamer_pipeline)

camera.start()

for i in range(10):
    _, frame = camera.read()
    cv2.imwrite(f"image{i}.jpeg", frame)
    time.sleep(2)

camera.stop()