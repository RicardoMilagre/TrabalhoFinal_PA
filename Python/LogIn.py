

from tkinter import *
from PIL import ImageTk, Image
from Python.MenuDB import MenuDataBase
from Python.Reconhecimento import ReconhecimentoFacial


def LogIn():
    janela = Tk()
    janela.title('Log In Menu')
    janela.geometry('1920x1080')
    janela.state('zoomed')
    frame = Frame(janela, width=600, height=400)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.5)
    img = ImageTk.PhotoImage(Image.open("Outros/recurso2.jpg"))
    label = Label(frame, image=img)
    label.pack()
    # FILE###########################################################################################################
    menubar = Menu(janela, background='#ff8800', foreground='black', activebackground='white', activeforeground='black')
    file = Menu(menubar, tearoff=0, foreground='black')
    file.add_command(label="Log In", command=lambda: [ReconhecimentoFacial(), janela.destroy(), MenuDataBase()])
    file.add_separator()
    file.add_command(label="Exit", command=janela.quit)
    menubar.add_cascade(label="File", menu=file)
    janela.config(menu=menubar)
    janela.mainloop()

LogIn()