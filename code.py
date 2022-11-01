import cv2
import time
from matplotlib.pyplot import axis
import numpy as np
import Image

bg = Image('bg_img.jpg')

fourcc      = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi' , fourcc , 20.0 , (640  ,480))
cap  =cv2.VideoCapture(0)

for i in range(60):
    frame , image = cap.read()
    bg = np.flip(bg , axis = 1)

    frame = cv2.resize(frame , (640 , 480))
    image = cv2.resize(frame , (640 , 480))

    u_black = np.array([104 , 153 , 70])
    l_black = np.array([30 ,30 ,0])

    mask = cv2.inRange(frame , l_black , u_black)
    res = cv2.bitwise_and(frame , frame , mask = mask)
    f   = frame-res
    f   = np.where(f == 0 , image = f)

    mask_1 = cv2.morphologyEx(mask , cv2.MORPH_OPEN , np.ones((3,3) , np.uint8))
    mask_1 = cv2.morphologyEx(mask , cv2.MORPH_DILATE , np.ones((3,3) , np.uint8))

    mask_2 = cv2.bitwise_not(mask_1)
    res_1 = cv2.bitwise_and(image , image , mask=mask_2)
    res_2 = cv2.bitwise_and(bg , bg , mask = mask_1)

    final_output = cv2.addWeighted(res_1 , 1 , res_2 , 1 , 0)
    output_file.write(final_output)
    cv2.imshow('magic' , final_output)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


