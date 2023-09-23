from tkinter import Tk,Label,Button,Entry, Frame,filedialog
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import imageio
import numpy as np 

import funciones_pdi as nf

class FrImage(Frame):

    def __init__(self, master=None, bg=None, txt_btn_open=None,operations=None, text_op=None,img_example=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets(bg,txt_btn_open,operations,text_op,img_example)
        
    def create_widgets(self,bg,txt_btn_open,operations,text_op,img_example):
        self.fr_img = Frame(self, width=350, height=500,bg=bg)
        self.fr_img.grid_propagate(False)
        self.fr_img.grid()
        self.fr_subimg = Frame(self.fr_img, width=300, height=300)
        self.fr_subimg.grid(padx=25, pady= 10)
        self.lbl_img = Label(self.fr_subimg)
        self.btn_open = Button(self.fr_img, text=txt_btn_open)
        self.btn_open['command'] = self.open_image
        self.btn_open.grid()
        self.btn_example = Button(self.fr_img, text="Ejemplo")
        self.btn_example['command'] = lambda: self.image_example(img_example)
        self.btn_example.grid()
        self.cbx_op = Combobox(self.fr_img, values=operations)
        self.cbx_op.grid(pady=10)
        self.cbx_op.bind("<<ComboboxSelected>>", self.operation_selected)
        self.lbl_op = Label(self.fr_img,text=text_op,bg=bg)
        self.lbl_op.grid(pady=8)
    
        
    def open_image(self):
        path_image = filedialog.askopenfilename()
        if path_image:
            # Abre la imagen seleccionada con Pillow
            image = Image.open(path_image)
            self.image_saved = imageio.imread(path_image)
            image = image.resize((300,300))
            # Convierte la imagen a un formato que tkinter pueda mostrar
            image_tk = ImageTk.PhotoImage(image)
            self.lbl_img.config(width=300, height=300)
            self.lbl_img.config(image=image_tk)
            self.lbl_img.image = image_tk  # Conserva una referencia para evitar que la imagen sea destruida por el recolector de basur
            self.lbl_img.grid()
    
    def image_example(self,img_example):
        self.image_saved = img_example
        image_tk = ImageTk.PhotoImage(image=Image.fromarray((self.image_saved).astype('uint8')).resize((300, 300)))
        self.lbl_img.config(width=300, height=300)
        self.lbl_img.config(image=image_tk)
        self.lbl_img.image = image_tk
        self.lbl_img.grid()
    
    def operation_selected(self,event):
        self.election = self.cbx_op.get()

class FrMain(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.operations=["Suma"]
        self.formats=["RGB Clampeada", "RGB Promediada", "YIQ Clampeada", "YIQ Promediada", "If Lighter", "If Darker"]
        self.img_example1 = imageio.imread('imageio:astronaut.png')[56:456, 6:506, :]
        self.img_example2 = imageio.imread('imageio:coffee.png')[:,50:550,:]
        self.create_widgets() 

    def create_widgets(self):
        self.frame1 = FrImage(self,
                              bg='azure3',txt_btn_open="Abrir imagen 1", 
                              operations=self.operations, text_op="Operacion",
                              img_example=self.img_example1)
        self.frame1.grid(row=0, column=0)
        
        self.frame2 = FrImage(self,bg='azure3', 
                              txt_btn_open="Abrir imagen 2", 
                              operations=self.formats, text_op="Formato",
                              img_example=self.img_example2)
        self.frame2.grid(row=0, column=1)
        
        self.fr_img_result = Frame(self, width=350, height=500,bg='azure3')
        self.fr_img_result.grid_propagate(False)
        self.fr_img_result.grid(row=0, column=2)
        self.fr_subimg = Frame(self.fr_img_result, width=300, height=300)
        self.fr_subimg.grid(padx=25, pady= 10)
        self.lbl_img = Label(self.fr_subimg)
        self.btn_open = Button(self.fr_img_result, text="Procesar")
        self.btn_open['command'] = self.resolve
        self.btn_open.grid()

    def resolve(self):
        #Para imagenes en RGB
        if (self.frame2.election == self.formats[0]) or (self.frame2.election == self.formats[1]):
            if self.frame2.election == self.formats[0]: #RGB clampeada
                result = nf.suma_clampeada_RGB(self.frame1.image_saved/255, self.frame2.image_saved/255)
            if self.frame2.election == self.formats[1]: #RGB promediada
                result = nf.suma_lineal_RGB(self.frame1.image_saved/255, self.frame2.image_saved/255)
            image_tk = ImageTk.PhotoImage(image=Image.fromarray((result*255).astype('uint8')).resize((300, 300)))

        #Para YIQ
        if (self.frame2.election != self.formats[0]) and (self.frame2.election != self.formats[1]):
            img1 = np.clip(self.frame1.image_saved/255.,0.,1.) #normalizando [0,1]
            img2 = np.clip(self.frame2.image_saved/255.,0.,1.) #normalizando [0,1]
            yiq1 = nf.RGB_to_YIQ(img1)
            yiq2 = nf.RGB_to_YIQ(img2)

            if self.frame2.election == self.formats[2]: #YIQ Clampeado
                result = nf.suma_clampeada_YIQ(yiq1,yiq2)
            if self.frame2.election == self.formats[3]: #YIQ Clampeado
                result = nf.suma_promediada_YIQ(yiq1,yiq2)
            if self.frame2.election == self.formats[4]: #If Ligther
                result = nf.if_ligther(yiq1,yiq2)
            if self.frame2.election == self.formats[5]: #If Darker
                result = nf.if_darker(yiq1,yiq2)
            result = nf.YIQ_to_RGB(result)
            image_tk = ImageTk.PhotoImage(image=Image.fromarray(np.clip((result*255),0,255).astype('uint8')).resize((300, 300)))
        
        self.lbl_img.config(width=300, height=300)
        self.lbl_img.config(image=image_tk)
        self.lbl_img.image = image_tk 
        self.lbl_img.grid()

if __name__ == '__main__':
    root = Tk()
    root.wm_title("TP2 Operaciones Aritmeticas")
    app = FrMain(root)
    app.mainloop()