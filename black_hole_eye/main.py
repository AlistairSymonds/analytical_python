import cv2
import argparse
import os
import pathlib

ap = argparse.ArgumentParser()
ap.add_argument("--image", "-i", help="path to image to analysed, will try to open webcam if not set")
args = ap.parse_args()

fn = pathlib.Path(__file__).parent
print(fn)

# Load the Haar cascades
face_path = fn / "haarcascade_frontalface_default.xml"
eye_path = fn / "haarcascade_eye.xml"
face_cascade = cv2.CascadeClassifier(str(face_path))
eyes_cascade = cv2.CascadeClassifier(str(eye_path))
eye_replacement = cv2.imread('m87.png', cv2.IMREAD_UNCHANGED)


# Define function that will do detection

# the facial recognition code is ehavily based around this excellent example:
# https://blog.goodaudience.com/real-time-face-and-eyes-detection-with-opencv-54d9ccfee6a8

def detect(gray, frame):
    """ Input = greyscale image or frame from video stream
        Output = Image with rectangle box in the face
    """
    # Now get the tuples that detect the faces using above cascade
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # faces are the tuples of 4 numbers
    # x,y => upperleft corner coordinates of face
    # width(w) of rectangle in the face
    # height(h) of rectangle in the face
    # grey means the input image to the detector
    # 1.3 is the kernel size or size of image reduced when applying the detection
    # 5 is the number of neighbors after which we accept that is a face

    # Now iterate over the faces and detect eyes
    for (x, y, w, h) in faces:
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Arguements => image, top-left coordinates, bottomright coordinates, color, rectangle border thickness

        # we now need two region of interests(ROI) grey and color for eyes one to detect and another to draw rectangle
        roi_gray = gray[y:y + h, x:x + w]
        # Detect eyes now
        eyes = eyes_cascade.detectMultiScale(roi_gray, 1.1, 3)
        # Now draw rectangle over the eyes

        for (ex, ey, ew, eh) in eyes:
            orig_y, orig_x, _ = eye_replacement.shape
            x_scale = ew / orig_x
            y_scale = eh / orig_y
            resized_replacement = cv2.resize(eye_replacement, None, fx=x_scale, fy=y_scale)

            new_x, new_y, _ = resized_replacement.shape
            for c in range(0, 3):
                alpha = resized_replacement[:, :, 3] / 255.0
                color = resized_replacement[:, :, c] * (alpha)
                beta = frame[y + ey:y + ey + new_y, x + ex:x + ex + new_x, c] * (1 - alpha)
                frame[y + ey:y + ey + new_y, x + ex:x + ex + new_x, c] = color + beta
    return frame



if args.image is None:
    # Capture video from webcam
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # Run the infinite loop

    while True:
        # Read each frame
        _, frame = video_capture.read()

        # Convert frame to grey because cascading only works with greyscale image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bgra = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        # Call the detect function with grey image and colored frame
        canvas = detect(gray, frame_bgra)
        # Show the image in the screen
        cv2.imshow("Video", canvas)
        # Put the condition which triggers the end of program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()

else:

    print(args.image)
    img = cv2.imread(args.image, cv2.IMREAD_UNCHANGED)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    frame_bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # Call the detect function with grey image and colored frame
    canvas = detect(gray, frame_bgra)

    img_name, img_ext = os.path.splitext(args.image)
    cv2.imwrite(img_name+"_bh_eye.jpg",canvas)
