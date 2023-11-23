from tkinter import Tk,Label,Button,Entry, Frame,filedialog,messagebox, Scale
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import imageio
import numpy as np
from libs.tkSliderWidget import Slider

import funciones_pdi as nf

class FrMain(Frame):

    FILTERS = {
        'Pasabajos llano 3x3': np.ones((3,3))/9, 
        'Pasabajos llano 5x5': np.ones((5,5))/25, 
        'Pasabajos llano 7x7': np.ones((7,7))/49,
        'Bartlett 3x3': nf.kernel_barlet(3)[1], 
        'Bartlett 5x5': nf.kernel_barlet(5)[1], 
        'Bartlett 7x7': nf.kernel_barlet(7)[1],
        'Gaussiano 5x5': nf.kernel_gaussiano(5)[1],
        'Gaussiano 7x7': nf.kernel_gaussiano(7)[1],
        'Pasaaltos Laplaciano v4 3x3': nf.kernel_laplaciano(4),
        'Pasaaltos Laplaciano v8 3x3': nf.kernel_laplaciano(8),
        'Mejora': nf.kernel_mejora(4),
        'Gradiente Sobel': 'sobel'
    }

    SOBEL = {
        '0 N': np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),
        '1': np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]]),
        '2 O': np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
        '3': np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]]),
        '4 S': np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]),
        '5': np.array([[2, 1, 0], [1, 0, -1], [0, -1, -2]]),
        '6 E': np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]),
        '7': np.array([[0, -1, -2], [1, 0, -1], [2, 1, 0]])
    }

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.img_sobel = imageio.imread('imagenes/Eight-direction-Sobel.png')
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.frame1 = Frame(self, width=400, height=500)
        self.frame1.grid_propagate(False)
        self.frame1.grid(row=0, column=0)

        self.fr_img1 = Frame(self.frame1, width=350, height=300)
        self.fr_img1.grid(row=0, column=0, padx=20, pady=10)
        self.lbl_img1 = Label(self.fr_img1)
        self.txt_img1 = Label(self.frame1,text="Imagen Original")
        
        self.frame2 = Frame(self, width=300, height=500)
        self.frame2.grid_propagate(False)
        self.frame2.grid(row=0, column=1)

        self.fr_btn = Frame(self.frame2,  width=300, height=150)
        self.fr_btn.grid_propagate(False)
        self.fr_btn.grid(row=0,column=0)

        self.btn_operation = Button(self.fr_btn, text="Filtrar -->")
        self.btn_operation['command'] = self.calculate
        self.btn_operation.grid(row=0, column=0, padx=10, pady=10)

        self.btn_open = Button(self.fr_btn, text="Seleccionar..")
        self.btn_open['command'] = self.open_image
        self.btn_open.grid(row=1, column=0, padx=10, pady=10)

        self.btn_save = Button(self.fr_btn, text="Guardar")
        self.btn_save['command'] = self.save_image
        self.btn_save.grid(row=0, column=1, padx=10, pady=10)

        self.fr_filters = Frame(self.fr_btn, width=150, height=100)
        self.fr_filters.grid(row=1, column=1)
        self.cbx_filters = Combobox(self.fr_filters, values=list(self.FILTERS.keys()))
        self.cbx_filters.grid(row=0, column=0)
        self.cbx_filters.bind("<<ComboboxSelected>>", self.filter_selected)
        self.txt_filters = Label(self.fr_filters,text="Filtros")
        self.txt_filters.grid(row=1, column=0)

        self.fr_options = Frame(self.fr_btn, width=150, height=100)
        self.cbx_options = Combobox(self.fr_options)
        self.cbx_options.grid(row=0, column=0)
        self.cbx_options.bind("<<ComboboxSelected>>", self.option_selected)
        self.txt_options = Label(self.fr_options)
        self.txt_options.grid(row=1, column=0)

        self.fr_img_sobel = Frame(self.frame2, width=300, height=300)
        self.fr_img_sobel.grid(row=1, column=0)
        self.lbl_img_sobel = Label(self.fr_img_sobel)

        self.frame3 =  Frame(self, width=400, height=500)
        self.frame3.grid_propagate(False)
        self.frame3.grid(row=0, column=3)

        self.fr_img2 = Frame(self.frame3, width=350, height=300)
        self.fr_img2.grid(row=0, column=0, padx=20, pady=10)
        self.lbl_img2 = Label(self.fr_img2)
        self.txt_img2 = Label(self.frame3,text="Imagen Modificada")

    def set_count(self,event):
        self.count = self.COUNT_VALUES[self.cbx_count.get()]

    def save_image(self):
        im = Image.fromarray(self.img2)
        extension = self.filename.split(".")[-1]
        name = self.filename.split(".")[0]
        im.save(f"descargas/{name}_{self.filter}.{extension}")
        messagebox.showinfo(message="Imagen guardada exitosamente", title="Imagen")

    def option_selected(self,event):
        self.option = self.cbx_options.get()

    def filter_selected(self,event):
        self.filter = self.cbx_filters.get()
        self.lbl_img_sobel.grid_forget()
        self.fr_options.grid_forget()
        if self.filter == 'Gradiente Sobel':
            image_tk1 = ImageTk.PhotoImage(image=Image.fromarray(np.clip(self.img_sobel,0,255).astype('uint8')).resize((300, 300)))
            self.lbl_img_sobel.config(width=300, height=300)
            self.lbl_img_sobel.config(image=image_tk1)
            self.lbl_img_sobel.image = image_tk1
            self.lbl_img_sobel.grid()

            self.fr_options.grid(row=2, column=1)
            self.cbx_options['values'] = list(self.SOBEL.keys())
            self.txt_options['text'] = 'Orientacion'

        # print(self.FILTERS[self.filter])

    def lineal_trozos_aux(self,x,a,b):
        y = np.zeros(len(x))
        for i, v in enumerate(x):
            y[i]=nf.lineal_trozos(v,a,b)
        return y
            
    def calculate(self):
        kernel = self.FILTERS[self.filter]
        if self.filter == 'Gradiente Sobel':
            kernel = self.SOBEL[self.option]
        result = nf.convolution(self.image_luminance,kernel)
        self.img2=np.clip((result*255),0,255).astype('uint8')
        image_tk = ImageTk.PhotoImage(image=Image.fromarray(np.clip((result*255),0,255).astype('uint8')).resize((350, 300)))
        
        self.lbl_img2.config(width=350, height=300)
        self.lbl_img2.config(image=image_tk)
        self.lbl_img2.image = image_tk
        self.lbl_img2.grid()
        self.txt_img2.grid()
    
    def open_image(self):
        path_image = filedialog.askopenfilename()
        self.filename = path_image.split("/")[-1]
        if path_image:
            # Abre la imagen seleccionada con Pillow
            # image = Image.open(path_image)
            self.image_saved = imageio.imread(path_image)
            try:
                if self.image_saved.shape[2] == 3:
                    img_clip = np.clip(self.image_saved/255,0.,1.) #normalizando [0,1]
                    yiq = nf.RGB_to_YIQ(img_clip)
                    self.image_luminance = yiq[:,:,0]
            except IndexError as e:
                self.image_luminance = np.clip(self.image_saved/255,0.,1.)

            # Convierte la imagen a un formato que tkinter pueda mostrar
            image_tk = ImageTk.PhotoImage(image=Image.fromarray(np.clip((self.image_luminance*255),0,255).astype('uint8')).resize((350, 300)))
            self.lbl_img1.config(width=350, height=300)
            self.lbl_img1.config(image=image_tk)
            self.lbl_img1.image = image_tk  # Conserva una referencia para evitar que la imagen sea destruida por el recolector de basur
            self.lbl_img1.grid()
            self.txt_img1.grid(pady=10)

if __name__ == '__main__':
    root = Tk()
    root.wm_title("TP4 Convolucion")
    app = FrMain(root)
    app.mainloop()