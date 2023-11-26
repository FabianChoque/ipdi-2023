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
        'Dilatacion 3x3': np.ones((3,3)),
        'Dilatacion 5x5': np.ones((5,5)), 
        'Erosion 3x3': np.ones((3,3)),
        'Erosion 3x3': np.ones((3,3)),
        'Erosion 5x5': np.ones((5,5)),
        'Apertura 3x3': np.ones((3,3)),
        'Apertura 5x5': np.ones((5,5)),
        'Cierre 3x3': np.ones((3,3)),
        'Cierre 5x5': np.ones((5,5)),
        'Frontera 3x3': np.ones((3,3)),
        'Frontera 5x5': np.ones((5,5)),
        'Mediana 3x3': 3,
        'Mediana 5x5': 5,
        'Mediana 7x7': 7,
    }

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.frame1 = Frame(self, width=400, height=425)
        self.frame1.grid_propagate(False)
        self.frame1.grid(row=0, column=0)

        self.fr_img1 = Frame(self.frame1, width=350, height=300)
        self.fr_img1.grid(row=0, column=0, padx=20, pady=10)
        self.lbl_img1 = Label(self.fr_img1)
        self.txt_img1 = Label(self.frame1,text="Imagen Original")
        self.txt_img1.grid(row=1, column=0, padx=10, pady=10)
        self.btn_open = Button(self.frame1, text="Cargar", width = 20)
        self.btn_open['command'] = self.open_image
        self.btn_open.grid(row=2, column=0, padx=10)

        self.frame2 = Frame(self, width=200, height=425)
        self.frame2.grid_propagate(False)
        self.frame2.grid(row=0, column=1)

        self.fr_btn = Frame(self.frame2,  width=200, height=300)
        self.fr_btn.grid_propagate(False)
        self.fr_btn.grid(row=0,column=0)

        self.btn_operation = Button(self.fr_btn, text="Filtrar -->", width = 20)
        self.btn_operation['command'] = self.calculate
        self.btn_operation.grid( padx=20,pady=20)

        self.btn_copy= Button(self.fr_btn, text="<-- Copiar", width = 20)
        self.btn_copy['command'] = self.copy_image
        self.btn_copy.grid(padx=20,pady=20)

        self.fr_filters = Frame(self.fr_btn, width=150, height=100)
        self.fr_filters.grid(padx=20,pady=20)
        self.cbx_filters = Combobox(self.fr_filters, values=list(self.FILTERS.keys()), width = 20)
        self.cbx_filters.grid()
        self.cbx_filters.bind("<<ComboboxSelected>>", self.filter_selected)
        self.txt_filters = Label(self.fr_filters,text="Filtros")
        self.txt_filters.grid()

        self.frame3 = Frame(self, width=400, height=425)
        self.frame3.grid_propagate(False)
        self.frame3.grid(row=0, column=3)

        self.fr_img2 = Frame(self.frame3, width=350, height=300)
        self.fr_img2.grid(row=0, column=0, padx=20, pady=10)
        self.lbl_img2 = Label(self.fr_img2)
        self.txt_img1 = Label(self.frame3,text="Imagen Original")
        self.txt_img1.grid(row=1, column=0, padx=10, pady=10)
        self.btn_save = Button(self.frame3, text="Guardar", width = 20)
        self.btn_save['command'] = self.save_image
        self.btn_save.grid(row=2, column=0, padx=10)

    def copy_image(self):
        self.img1 = self.img2
        self.show_image(self.img1, self.lbl_img1)
        
    def save_image(self):
        im = Image.fromarray(self.img2)
        extension = self.filename.split(".")[-1]
        name = self.filename.split(".")[0]
        im.save(f"descargas/{name}_{self.filter}.{extension}")
        messagebox.showinfo(message="Imagen guardada exitosamente", title="Imagen")

    def filter_selected(self,event):
        self.filter = self.cbx_filters.get()

    def lineal_trozos_aux(self,x,a,b):
        y = np.zeros(len(x))
        for i, v in enumerate(x):
            y[i]=nf.lineal_trozos(v,a,b)
        return y
            
    def calculate(self):
        kernel = self.FILTERS[self.filter]
        if 'Dilatacion'in self.filter:
            self.img2 = nf.im_dilate(self.img1, kernel)
        if 'Erosion' in self.filter:
            self.img2 = nf.im_erode(self.img1, kernel)
        if 'Frontera' in self.filter:
            self.img2 = nf.im_border_ext(self.img1, kernel)
        if 'Apertura' in self.filter:
            self.img2 = nf.im_open(self.img1, kernel)
        if 'Cierre' in self.filter:
            self.img2 = nf.im_close(self.img1, kernel)
        if 'Mediana' in self.filter:
            self.img2 = (nf.mediana(self.img1,kernel))/255

        self.show_image(self.img2,self.lbl_img2)

    def open_image(self):
        path_image = filedialog.askopenfilename()
        self.filename = path_image.split("/")[-1]
        if path_image:
            # Abre la imagen seleccionada con Pillow
            self.image_saved = imageio.imread(path_image)
            try:
                if self.image_saved.shape[2] == 3:
                    img_clip = np.clip(self.image_saved/255,0.,1.) #normalizando [0,1]
                    yiq = nf.RGB_to_YIQ(img_clip)
                    self.img1 = yiq[:,:,0]
            except IndexError as e:
                self.img1 = np.clip(self.image_saved/255,0.,1.)
        self.show_image(self.img1,self.lbl_img1)
    
    def show_image(self,img,label):
        # Convierte la imagen a un formato que tkinter pueda mostrar
        image_tk = ImageTk.PhotoImage(image=Image.fromarray(np.clip((img*255),0,255).astype('uint8')).resize((350, 300)))
        label.config(width=350, height=300)
        label.config(image=image_tk)
        label.image = image_tk  # Conserva una referencia para evitar que la imagen sea destruida por el recolector de basur
        label.grid()

if __name__ == '__main__':
    root = Tk()
    root.wm_title("TP5 Morfologia")
    app = FrMain(root)
    app.mainloop()