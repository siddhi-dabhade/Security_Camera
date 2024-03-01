import cv2      # used to open camera
import winsound

cam = cv2.VideoCapture(0)       # cam captures the video

while cam.isOpened():       
    ret, frame1 = cam.read()     # used for detection of the env
    ret, frame2 = cam.read()     # used for detection of the moving objects in relation to the env
    diff = cv2.absdiff(frame1, frame2)      # shows colored changes when object moves
    gray = cv2.cvtColor(diff , cv2.COLOR_RGB2GRAY)      # we change RGB to GRAY color when detecting motion since gray color gives an accurate detection than the RGB 
    blur = cv2.GaussianBlur(gray, (5, 5), 0)        # blur version of the gray color motion detectoqr
    _ , thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)        # to make the motion detector sharper and brighter to get rid of noises 
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)        # to get boundary around the objects 

    #cv2.drawContours(frame1, contours, -1 , (0, 255, 0), 2)
    for c in contours:
        if cv2.contourArea(c) < 5000:       # to draw contours around the big things
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        winsound.Beep(500, 200)
        #winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

    if cv2.waitKey(10) == ord('q'):     # turns off the camera after pressing q
        break
    cv2.imshow('Security Cam', frame1)      # shows the video being captured on the frame named Security camera
