import cv2
import numpy as np

def cross_dissolve(img1, img2, alpha):
    return (1 - alpha) * img1 + alpha * img2

def laplacian_blend(img1, img2, levels=4):
    gp1 = [img1.copy()]
    gp2 = [img2.copy()]

    for _ in range(levels):
        gp1.append(cv2.pyrDown(gp1[-1]))
        gp2.append(cv2.pyrDown(gp2[-1]))

    lp1 = [gp1[-1]]
    lp2 = [gp2[-1]]

    for i in range(levels-1, -1, -1):
        size = (gp1[i].shape[1], gp1[i].shape[0])
        lap1 = gp1[i] - cv2.pyrUp(gp1[i+1], dstsize=size)
        lap2 = gp2[i] - cv2.pyrUp(gp2[i+1], dstsize=size)
        lp1.append(lap1)
        lp2.append(lap2)

    LS = []
    for l1, l2 in zip(lp1, lp2):
        LS.append((l1 + l2) / 2)

    result = LS[0]
    for i in range(1, len(LS)):
        result = cv2.pyrUp(result)
        result += LS[i]

    return result
