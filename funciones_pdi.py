import cv2
import numpy as np
from scipy import ndimage

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

def more_ligther(yiq):
    result = np.zeros(yiq.shape)
    result[:,:,0] = np.sqrt(yiq[:,:,0])
    result[:,:,1] = yiq[:,:,1]
    result[:,:,2] = yiq[:,:,2]
    return result

def more_darker(yiq):
    result = np.zeros(yiq.shape)
    result[:,:,0] = yiq[:,:,0] * yiq[:,:,0]
    result[:,:,1] = yiq[:,:,1]
    result[:,:,2] = yiq[:,:,2]
    return result

def histogram_lineal(yiq,a,b):
    result = np.zeros(yiq.shape)
    for x in range(yiq[:,:,0].shape[0]):
        for y in range(yiq[:,:,0].shape[1]):
            result[x,y,0] = lineal_trozos(yiq[:,:,0][x,y],a,b)
    result[:,:,1] = yiq[:,:,1]
    result[:,:,2] = yiq[:,:,2]
    return result

def convolution(image, kernel = np.ones((1,1)), option = 'sum'):
    convolved = np.zeros((np.array(image.shape)-np.array(kernel.shape)+1))
    if option == 'sum':
        for x in range(convolved.shape[0]):
            for y in range(convolved.shape[1]):
                convolved[x,y] = (image[x:x+kernel.shape[0],y:y+kernel.shape[1]]*kernel).sum()
    if option == 'max':
        for x in range(convolved.shape[0]):
            for y in range(convolved.shape[1]):
                convolved[x,y] = (image[x:x+kernel.shape[0],y:y+kernel.shape[1]]*kernel).max()      
    if option == 'min':
        for x in range(convolved.shape[0]):
            for y in range(convolved.shape[1]):
                convolved[x,y] = (image[x:x+kernel.shape[0],y:y+kernel.shape[1]]*kernel).min()               
    return convolved

def lineal_trozos(x,a,b):
    m = (1/(b-a))
    if x < a :
        return 0
    elif x > b:
        return 1
    else:
        return m*(x-a)

def kernel_barlet(size):
    row=np.zeros(size)
    half = int(size/2 + 0.5)
    for x in range(size):
        if(x<half):
            row[x] = (x+1)
        else:
            row[x] = row[x-1]-1
    matrix = complete_matrix(row,size)
    return matrix, matrix/matrix.sum()

def kernel_gaussiano(size):
    row = triangulo_pascal(size-1)
    matrix = complete_matrix(row,size)
    return matrix, matrix/matrix.sum()

def kernel_laplaciano(version):
    if version == 4:
        return np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    if version == 8:
        return np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])

def kernel_mejora(version):
    # return np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    k_laplaciano = kernel_laplaciano(version)
    i = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    sum_kernels = i+k_laplaciano*0.2
    return sum_kernels


def factorial(num):
    if num > 0:
        return int(num*factorial(num-1))
    else:
        return 1

def combinatoria(num1, num2):
    return int(factorial(num1) / (factorial(num2)*factorial(num1-num2)))

def triangulo_pascal(size):
    row = np.zeros(size+1)
    for x in range(size+1):
        row[x] = combinatoria(size,x)
    return row

def complete_matrix(row,size):
    m=np.zeros((size,size))
    m[0,:] = row
    m[:,0] = np.transpose(row)
    for x in range(size-1):
        for y in range(size-1):
            m[x+1,y+1] = m[x+1,0] * m[0,y+1]
    return m

def _morph_multiband(im, se, op):
    result = np.zeros(im.shape)
    offset = (np.array(se.shape)-1)//2
    im = np.pad(im,[(offset[0],offset[0]),(offset[1],offset[1]),(0,0)],'edge')
    for y, x in np.ndindex(result.shape[:2]):
        pixels = im[y:y+se.shape[0], x:x+se.shape[1]][se]
        result[y, x] = pixels[op(pixels[:,0])]
    return result

def _morph_color(im, se, op):
    im2 = (RGB_to_YIQ(im)[:, :, 0])[:, :, np.newaxis]
    im2 = np.concatenate((im2, im),axis=2)
    result = _morph_multiband(im2, se, op)[:, :, 1:]
    return result

def im_dilate(im, se):
    if im.ndim == 3:
        return _morph_color(im, se, np.argmax)
    else:
        return ndimage.grey_dilation(im, footprint = se)
    
def im_erode(im, se):
    if im.ndim == 3:
        return _morph_color(im, se, np.argmin)
    else:
        return ndimage.grey_erosion(im, footprint = se)

def im_border_ext(im, se):
    return im_dilate(im, se) - im

def im_border_int(im, se):
    return im - im_erode(im, se)

def im_gradient(im, se):
    return im_dilate(im,se) - im_erode(im,se)

def im_open(im, se):
    return im_dilate(im_erode(im, se), se)

def im_close(im, se):
    return im_erode(im_dilate(im, se), se)

def mediana(im,kernel):
    img_formated = np.array(255*im, dtype = 'uint8')
    return cv2.medianBlur(img_formated,kernel)