import cv2 as cv
import numpy as np

def Liquify(img, x, y):
    shape = img.shape[:2]
    width = shape[0] if shape[0] <= shape[1] else shape[1]
    x_center = x
    y_center =y
    radius = np.floor(width*1/3)
    img = np.asarray(img)
    img2 = np.zeros_like(img)
    img2 = np.asarray(img2)
    for x in range(-np.rint(width / 2).astype(int), np.rint(width / 2).astype(int)):
        for y in range(-np.rint(width / 2).astype(int), np.rint(width / 2).astype(int)):
            if x * x + y * y <= radius * radius:
                r = np.sqrt(x * x + y * y)
                theta = np.arctan2(y, x)
                if theta < 0:
                    theta += np.pi * 2
                interpolation_factor = np.minimum(1,r / radius)
                #r_map = 1.5*r * interpolation_factor + (1 - interpolation_factor)  *0.2* np.power(radius,0.2)
                r_map= 1*r*interpolation_factor - (1-interpolation_factor)*0.4* np.power(r,0.5)
                if x_center + (r_map * np.cos(theta)).astype(int)>=shape[0] or x_center + (r_map * np.cos(theta)).astype(int)<0 or (y_center + r_map * np.sin(theta)).astype(int)>=shape[1] or (y_center + r_map * np.sin(theta)).astype(int)<0:
                    continue
                if (x_center + x).astype(int) >= shape[0] or (x_center + x).astype(int)<0 or (y_center + y).astype(int)>shape[1] or (y_center + y).astype(int)<0:
                    continue
                if x <= 0:
                    #r_map = 1*r *1.5
                    img2[(x_center + x).astype(int), (y_center + y).astype(int)] = img[x_center + (r_map * np.cos(theta)).astype(int), (y_center + r_map * np.sin(theta)).astype(int)]
                    #img[(x_center + r_map * np.cos(theta)).astype(int), (y_center + r_map * np.sin(theta)).astype(int)] = img[(x_center + x).astype(int), (y_center + y).astype(int)]
                    #img[(x_center + x).astype(int), (y_center + y).astype(int)] = r
                    pass
                if x>0:       
                    #r_map = 1*r*interpolation_factor + (1-interpolation_factor)*r*2
                    #print(r,r_map,x_center + (r_map * np.cos(theta)).astype(int) )
                    img2[(x_center + x).astype(int), (y_center + y).astype(int)] = img[x_center + (r_map * np.cos(theta)).astype(int), (y_center + r_map * np.sin(theta)).astype(int)]
                    #print((x_center + r_map * np.cos(theta)).astype(int), (y_center + r_map * np.sin(theta)).astype(int))
                    pass

    x,y,_ =np.nonzero(img2)
    img[x,y]=img2[x,y]
    return img