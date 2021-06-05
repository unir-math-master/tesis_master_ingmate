import cv2

class TelescopeCamera:
    capture_width=1280
    capture_height=720
    display_width=1280
    display_height=720
    framerate=60
    flip_method=0
    gstreamer=""

    def gstreamer_pipeline(self):
        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                TelescopeCamera.capture_width,
                TelescopeCamera.capture_height,
                TelescopeCamera.framerate,
                TelescopeCamera.flip_method,
                TelescopeCamera.display_width,
                TelescopeCamera.display_height
            )
        )


    def __init__(self, camera_config):
        TelescopeCamera.capture_width=1280
        TelescopeCamera.capture_height=720
        TelescopeCamera.display_width=1280
        TelescopeCamera.display_height=720
        TelescopeCamera.framerate=60
        TelescopeCamera.flip_method=0
        TelescopeCamera.gstreamer=self.gstreamer_pipeline()
        print(TelescopeCamera.gstreamer)

    def show_camera(self):
        # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
        cap = cv2.VideoCapture(TelescopeCamera.gstreamer, cv2.CAP_GSTREAMER)
        if cap.isOpened():
            window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
            # Window
            while cv2.getWindowProperty("CSI Camera", 0) >= 0:
                ret_val, img = cap.read()
                cv2.imshow("CSI Camera", img)
                # This also acts as
                keyCode = cv2.waitKey(30) & 0xFF
                # Stop the program on the ESC key
                if keyCode == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()
        else:
            print("Unable to open camera")



