import numpy as np

def YIQ_to_RGB(yiq):
    rgb = np.zeros(yiq.shape)
    rgb[:,:,0] = yiq[:,:,0] + 0.9663*yiq[:,:,1] + 0.6210*yiq[:,:,2] #BandaR
    rgb[:,:,1] = yiq[:,:,0] - 0.2721*yiq[:,:,1] - 0.6474*yiq[:,:,2] #BandaG
    rgb[:,:,2] = yiq[:,:,0] - 1.1070*yiq[:,:,1] + 1.7046*yiq[:,:,2] #BandaB
    return rgb

def RGB_to_YIQ(rgb):
    yiq = np.zeros(rgb.shape)
    yiq[:,:,0] = 0.229*rgb[:,:,0] + 0.587*rgb[:,:,1] + 0.114*rgb[:,:,2]
    yiq[:,:,1] = 0.595716*rgb[:,:,0] - 0.274453*rgb[:,:,1] - 0.321263*rgb[:,:,2]
    yiq[:,:,2] = 0.211456*rgb[:,:,0] - 0.522591*rgb[:,:,1] + 0.311135*rgb[:,:,2]
    return yiq

def suma_clampeada_RGB(rgb1,rgb2):
    suma = np.zeros(rgb1.shape)
    suma[:,:,0] = np.clip(rgb1[:,:,0] + rgb2[:,:,0],0,1)
    suma[:,:,1] = np.clip(rgb1[:,:,1] + rgb2[:,:,0],0,1)
    suma[:,:,2] = np.clip(rgb1[:,:,2] + rgb2[:,:,0],0,1)
    return suma

# def suma_clampeada_RGB(rgb1,rgb2):
#     suma = np.zeros(rgb1.shape)
#     suma[:,:,0] = np.clip(rgb1[:,:,0] + rgb2[:,:,0],0,255)
#     suma[:,:,1] = np.clip(rgb1[:,:,1] + rgb2[:,:,0],0,255)
#     suma[:,:,2] = np.clip(rgb1[:,:,2] + rgb2[:,:,0],0,255)
#     return suma

def suma_lineal_RGB(rgb1,rgb2):
    suma = np.zeros(rgb1.shape)
    suma[:,:,0] = np.clip((rgb1[:,:,0] + rgb2[:,:,0])/2,0,1)
    suma[:,:,1] = np.clip((rgb1[:,:,1] + rgb2[:,:,0])/2,0,1)
    suma[:,:,2] = np.clip((rgb1[:,:,2] + rgb2[:,:,0])/2,0,1)
    return suma

def suma_clampeada_YIQ(yiq1, yiq2):
    suma = np.zeros(yiq1.shape)
    suma[:,:,0] = np.clip(yiq1[:,:,0] + yiq2[:,:,0],0,1)
    suma[:,:,1] = np.clip((yiq1[:,:,0] * yiq1[:,:,1])+(yiq2[:,:,0] * yiq2[:,:,1])/(yiq1[:,:,0] + yiq2[:,:,0]),0,1)
    suma[:,:,2] = np.clip((yiq1[:,:,0] * yiq1[:,:,2])+(yiq2[:,:,0] * yiq2[:,:,2])/(yiq1[:,:,0] + yiq2[:,:,0]),0,1)
    return suma

def suma_promediada_YIQ(yiq1, yiq2):
    suma = np.zeros(yiq1.shape)
    suma[:,:,0] = np.clip((yiq1[:,:,0] + yiq2[:,:,0])/2,0,1)
    suma[:,:,1] = np.clip(((yiq1[:,:,0] * yiq1[:,:,1])+(yiq2[:,:,0] * yiq2[:,:,1])/(yiq1[:,:,0] + yiq2[:,:,0]))/2,0,1)
    suma[:,:,2] = np.clip(((yiq1[:,:,0] * yiq1[:,:,2])+(yiq2[:,:,0] * yiq2[:,:,2])/(yiq1[:,:,0] + yiq2[:,:,0]))/2,0,1)
    return suma

def if_ligther(yiq1,yiq2):
    ligther = np.zeros(yiq1.shape)
    ligther[:,:,0] = np.maximum(yiq1[:,:,0],yiq2[:,:,0])
    ligther[:,:,1] = np.maximum(yiq1[:,:,1],yiq2[:,:,1])
    ligther[:,:,2] = np.maximum(yiq1[:,:,2],yiq2[:,:,2])
    return ligther

def if_darker(yiq1,yiq2):
    darker = np.zeros(yiq1.shape)
    darker[:,:,0] = np.minimum(yiq1[:,:,0],yiq2[:,:,0])
    darker[:,:,1] = np.minimum(yiq1[:,:,1],yiq2[:,:,1])
    darker[:,:,2] = np.minimum(yiq1[:,:,2],yiq2[:,:,2])
    return darker

def convolution1(image, kernel = np.ones((1,1))):
    print(image.shape)
    print(kernel.shape)
    convolved = np.zeros((np.array(image.shape)-np.array(kernel.shape)+1))
    print(convolved.shape)
    for x in range(convolved.shape[0]):
        for y in range(convolved.shape[1]):
            convolved[x,y] = (image[x:x+kernel.shape[0],y:y+kernel.shape[1]]*kernel).sum()
    return convolved

def convolution2(image, kernel = np.ones((1,1))):
    convolved = np.zeros((np.array(image.shape)-np.array(kernel.shape)+1))
    for x, y in np.ndindex(convolved.shape):
        convolved[x,y] = (image[x:x+kernel.shape[0],y:y+kernel.shape[1]]*kernel).sum()
    return convolved