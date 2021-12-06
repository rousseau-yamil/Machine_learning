import cv2
import winsound

cam = cv2.VideoCapture(0) #numero de la camara puede ser 1 o 2 si hay otras
address = "https:/192.168.43.200:8080/video"
cam.open(address)
while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2) #creamos una diferencia entre estado 0 y movimiento
    gris = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gris, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2) contorno de cada micromovimiento en camara
    for c in contours:
        if cv2.contourArea(c) < 5000: # la capacidad de movimiento filtrada
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+w), (0, 255, 0), 2) # el tamaño del rectangulo
        winsound.Beep(500, 200)#default beep
       # winsound.PlaySound('filename.wav', winsound.SND_ASYNCJ)

    if cv2.waitKey(10) == ord('q'):#exitfunction la q
        break
    cv2.imshow('A cam', frame1) #solo mostramos cuando la diferencia osea lo que se mueve
