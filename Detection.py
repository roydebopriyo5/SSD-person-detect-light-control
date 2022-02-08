import numpy as np
import cv2
import schedule, time
import Operate

while True:

    video = cv2.VideoCapture(0)

    if (video.isOpened() == False):
        print("Error reading video file")

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    size = (frame_width, frame_height)

    result = cv2.VideoWriter('obj.avi',
                            cv2.VideoWriter_fourcc(*'XVID'),
                            10, size)

    capture_duration = 60
    start_time = time.time()

    while True:
        print(int(start_time),int(time.time()))
        ret, frame = video.read()
        frame = cv2.flip(frame, 1)

        if ret == True:
            result.write(frame)
            cv2.imshow('Frame', frame)
            if int(time.time() - start_time) >= capture_duration:
                break
        else:
            break

    video.release()
    result.release()
    cv2.destroyAllWindows()

    PROTOTXT = "MobileNetSSD_deploy.prototxt"
    MODEL = "MobileNetSSD_deploy.caffemodel"
    INP_VIDEO_PATH = 'obj.avi'
    OUT_VIDEO_PATH = 'obj_detection.avi'
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
                "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)

    cap = cv2.VideoCapture(INP_VIDEO_PATH)
    while True:
        ret, frame = cap.read()

        if not ret:
            break
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                idx = int(detections[0, 0, i, 1])

                switch = 0
                if CLASSES[idx] == "person":
                    switch += 1
                    print("Detected!!!")
                    Operate.led(switch)
                else:
                    print ("Not Detected!!!")
                    Operate.led(switch)

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)

                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cv2.destroyAllWindows()
