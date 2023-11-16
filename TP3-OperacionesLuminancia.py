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

    COUNT_VALUES = {'10': 10, '20': 20, '50': 50}

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.min_lineal = 0
        self.max_lineal = 1
        self.count = self.COUNT_VALUES['10']
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.frame1 = Frame(self, width=450, height=600)
        self.frame1.grid_propagate(False)
        self.frame1.grid(row=0, column=0)

        self.fr_img1 = Frame(self.frame1, width=300, height=250)
        self.fr_img1.grid(row=0, column=0, padx=20, pady=10)
        self.lbl_img1 = Label(self.fr_img1)

        self.fr_frecuency1 = Frame(self.frame1, width=450, height=300)
        self.fr_frecuency1.grid(row=1, column=0, padx=10, pady=10)
        self.lbl_frecuency1 = Label(self.fr_frecuency1)
        self.txt_frecuency1 = Label(self.fr_frecuency1,text="Frecuencia")
        self.lbl_frecuency1.grid(row=1,column=1)
        
        self.frame2 = Frame(self, width=300, height=600)
        self.frame2.grid_propagate(False)
        self.frame2.grid(row=0, column=1)

        self.fr_btn = Frame(self.frame2,  width=300, height=200)
        self.fr_btn.grid_propagate(False)
        self.fr_btn.grid(row=0,column=0, pady=10)

        self.btn_operation = Button(self.fr_btn, text="Calcular")
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
        self.cbx_filters = Combobox(self.fr_filters, values=["Raiz", "Exponencial", "Lineal"])
        self.cbx_filters.grid(row=0, column=0)
        self.cbx_filters.bind("<<ComboboxSelected>>", self.operation_selected)
        self.txt_filters = Label(self.fr_filters,text="Filtros")
        self.txt_filters.grid(row=1, column=0,pady=8)

        self.fr_count = Frame(self.fr_btn, width=150, height=100)
        self.fr_count.grid(row=2, column=0)
        self.cbx_count = Combobox(self.fr_count, values=list(self.COUNT_VALUES.keys()))
        self.cbx_count.grid(row=0, column=0)
        self.cbx_count.bind("<<ComboboxSelected>>", self.set_count)
        self.txt_count = Label(self.fr_count,text="Contadores")
        self.txt_count.grid(row=1, column=0,pady=8)

        self.fr_function = Frame(self.frame2, width=280, height=200)
        self.fr_function.grid_propagate(False)
        self.fr_function.grid(padx=10,pady=10)

        self.fr_slider = Frame(self.frame2, width=280, height=60)
        self.fr_slider.grid_propagate(False)
        self.fr_slider.grid(padx=10)
        self.slider = Slider(self.fr_slider, width = 280, height = 60, min_val = 0, max_val = 1, init_lis = [0,1], show_value = True)
        self.slider.setValueChageCallback(lambda _: self.refresh_lineal())

        self.frame3 = Frame(self, width=450, height=600)
        self.frame3.grid_propagate(False)
        self.frame3.grid(row=0, column=3)

        self.fr_img2 = Frame(self.frame3, width=300, height=250)
        self.fr_img2.grid(row=0, column=0, padx=20, pady=10)
        self.lbl_img2 = Label(self.fr_img2)
        
        self.fr_frecuency2 = Frame(self.frame3, width=450, height=300)
        self.fr_frecuency2.grid(row=1, column=0, padx=10, pady=10)
        self.lbl_frecuency2 = Label(self.fr_frecuency2)
        self.lbl_frecuency2.grid(row=1,column=1)

    def set_count(self,event):
        self.count = self.COUNT_VALUES[self.cbx_count.get()]

    def save_image(self):
        im = Image.fromarray(self.img2)
        extension = self.filename.split(".")[-1]
        name = self.filename.split(".")[0]
        im.save(f"descargas/{name}_{self.filter}.{extension}")
        messagebox.showinfo(message="Imagen guardada exitosamente", title="Imagen")

    def operation_selected(self,event):
        x = np.arange(0.0, 1.0, 0.01)
        x = np.append(x, 1)
        self.filter = self.cbx_filters.get()
        if(self.filter=='Raiz'):
            y = np.sqrt(x)
            self.slider.pack_forget()
        else:
            if(self.filter=='Exponencial'):
                y = x*x
                self.slider.pack_forget()
            else:
                if (self.filter=='Lineal'):
                    values = [round(v,1) for v in self.slider.getValues()]
                    y = self.lineal_trozos_aux(x,values[0],values[1])
                    self.slider.pack()
        self.draw_function(x,y)

    def lineal_trozos_aux(self,x,a,b):
        y = np.zeros(len(x))
        for i, v in enumerate(x):
            y[i]=nf.lineal_trozos(v,a,b)
        return y

    def draw_function(self,x,y):
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.set(title='Funcion '+self.filter)
        ax.plot(x, y)
        canvas = FigureCanvasTkAgg(fig, master=self.fr_function)# Crea el area de dibujo en Tkinter
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
            
    def calculate(self):
        img_clip = np.clip(self.image_saved/255,0.,1.) #normalizando [0,1]
        yiq = nf.RGB_to_YIQ(img_clip)
        self.calculate_histogram(yiq[:,:,0].flatten(),self.fr_frecuency1)
        
        if (self.filter == 'Raiz'):
            yiq_modified = nf.more_ligther(yiq)
        if (self.filter == 'Exponencial'):
            yiq_modified = nf.more_darker(yiq)
        if (self.filter == 'Lineal'):
            yiq_modified = nf.histogram_lineal(yiq,self.min_lineal,self.max_lineal)
        rgb = nf.YIQ_to_RGB(yiq_modified)

        self.img2=np.clip((rgb*255),0,255).astype('uint8')
        image_tk = ImageTk.PhotoImage(image=Image.fromarray(np.clip((rgb*255),0,255).astype('uint8')).resize((300, 300)))
        
        self.lbl_img2.config(width=300, height=250)
        self.lbl_img2.config(image=image_tk)
        self.lbl_img2.image = image_tk
        self.lbl_img2.grid()
        fig, ax = plt.subplots(figsize=(4, 3))
        canvas = FigureCanvasTkAgg(fig, master=self.fr_frecuency2)# Crea el area de dibujo en Tkinter
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
        self.calculate_histogram(yiq_modified[:,:,0].flatten(),self.fr_frecuency2)

    def calculate_histogram(self,values,frecuency1):
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.set(title='Histograma')
        n, bins, patches = ax.hist(values, bins=self.count, range=(0,1), density=True)    
        altura_total = np.sum(n)
        factor_de_escala = 100 / altura_total
        n *= factor_de_escala
        # Graficar el histograma escalado
        ax.bar(bins[:-1], n, width=np.diff(bins), align="edge", edgecolor='black')
        # Establecer límite en el eje y hasta 100%
        ax.set_ylim(0, 100)     
        canvas = FigureCanvasTkAgg(fig, master=frecuency1)# Crea el area de dibujo en Tkinter
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
    
    def open_image(self):
        path_image = filedialog.askopenfilename()
        self.filename = path_image.split("/")[-1]
        if path_image:
            # Abre la imagen seleccionada con Pillow
            image = Image.open(path_image)
            self.image_saved = imageio.imread(path_image)
            image = image.resize((300,250))
            # Convierte la imagen a un formato que tkinter pueda mostrar
            image_tk = ImageTk.PhotoImage(image)
            self.lbl_img1.config(width=300, height=250)
            self.lbl_img1.config(image=image_tk)
            self.lbl_img1.image = image_tk  # Conserva una referencia para evitar que la imagen sea destruida por el recolector de basur
            self.lbl_img1.grid()
    
    def refresh_lineal(self):
        x = np.arange(0.0, 1.0, 0.01)
        values = [round(v,1) for v in self.slider.getValues()]
        self.min_lineal = values[0]
        self.max_lineal = values[1]
        y = self.lineal_trozos_aux(x,self.min_lineal, self.max_lineal)
        self.draw_function(x,y)

if __name__ == '__main__':
    root = Tk()
    root.wm_title("TP3 Operaciones de Luminancias")
    app = FrMain(root)
    app.mainloop()