# Some useful links:
# General:
# https://www.tcl.tk/man/tcl8.4/TkCmd/text.htm
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/text.html
# https://stackoverflow.com/questions/21717115/using-tk-to-create-a-text-editor
# https://github.com/manjunathb4461/text-editor-with-tkinter/blob/master/main.py
# Tags: 
# https://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget/3781773#3781773
# https://stackoverflow.com/questions/3732605/add-advanced-features-to-a-tkinter-text-widget
# Images:
# https://pillow.readthedocs.io/en/stable/reference/ImageGrab.html
# https://github.com/ponty/pyscreenshot
import requests
import os
import re
import platform
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import filedialog
from tkinter import Scrollbar
import tkinter.font as tkFont
from utils import *

if platform.system() == "Windows":
    PATH_SEP = "\\"
else:
    PATH_SEP = "/"

ROOT = '/home/carter/Documents/Moulinette/'
PROJECT = 'Tinbergen - 1930 - De werkloosheid'


class Moulinette(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("La Moulinette")
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth()-3, self.winfo_screenheight()-3))
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(size=16, family="courier 10 pitch")

        self.content = ttk.Frame(self)
        self.top = ttk.Frame(self.content)
        self.left = ttk.Labelframe(self.content,text="Original Text")
        self.right = ttk.Labelframe(self.content,text="Translated Text")

        self.content.pack(fill = tk.BOTH,expand=True)
        self.top.pack(side = tk.TOP, fill = tk.X, padx=10,pady=5,ipadx=5,ipady=5)
        self.left.pack(side = tk.LEFT, expand=True, fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5)
        self.right.pack(side = tk.RIGHT, expand=True, fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5)

        # Top settings
        self.settings_frame = ttk.Labelframe(self.top, text="Settings")
        self.settings_frame.pack(fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5)

        ttk.Label(self.settings_frame, text='File: ').grid(column=0,row=0)
        self.filepath_entry = ttk.Entry(self.settings_frame, font=self.default_font)
        self.filepath_entry.grid(column=1,row=0, pady=(2,2), sticky="nsew")
        # self.filepath_entry.insert(0,"/home/carter/Desktop")
        self.browse_button = ttk.Button(self.settings_frame, text="Browse", command=self.browseDir)
        self.browse_button.grid(column=2,row=0, pady=(2,2), sticky="nsew", padx=(5,5))

        self.browse_button = ttk.Button(self.settings_frame, text="Load File", command=self.loadFile)
        self.browse_button.grid(column=1,row=1,columnspan=2, pady=(2,2), sticky="nsew", padx=(5,5))
        
        self.doOCR = tk.BooleanVar()
        self.doOCR.set(False)
        ttk.Checkbutton(self.settings_frame, text='do OCR', variable=self.doOCR,onvalue=True,offvalue=False).grid(column=3,row=0,padx=(5,5), pady=(2,2))

        self.doTranslate = tk.BooleanVar()
        self.doTranslate.set(False)
        ttk.Checkbutton(self.settings_frame, text='Translate', variable=self.doTranslate,onvalue=True,offvalue=False).grid(column=4,row=0,padx=(5,5), pady=(2,2))

        # Left editor (original text)
        self.editor_left = tk.Text(wrap="word", background="white",undo=True,autoseparators=True,maxundo=-1,borderwidth=0, highlightthickness=0,spacing3=10)
        self.scrollbar_left = Scrollbar(orient="vertical", borderwidth=1,command=self.editor_left.yview)

        self.editor_left.configure(yscrollcommand=self.scrollbar_left.set)
        self.scrollbar_left.pack(in_=self.left,side=tk.RIGHT,fill=tk.Y,expand=False)
        self.editor_left.pack(in_=self.left,side=tk.LEFT,expand=True,fill=tk.BOTH)
        
        # Right editor (translated text)
        self.editor_right = tk.Text(wrap="word", background="white",borderwidth=0, highlightthickness=0)
        self.scrollbar_right = Scrollbar(orient="vertical", borderwidth=1,command=self.editor_right.yview)

        self.editor_right.configure(yscrollcommand=self.scrollbar_right.set)
        self.scrollbar_right.pack(in_=self.right,side=tk.RIGHT,fill=tk.Y,expand=False)
        self.editor_right.pack(in_=self.right,side=tk.LEFT,expand=True,fill=tk.BOTH)


        # self.editor_left.bind("<space>", self.printTags)

    def printTags(self):
        current_tags = self.editor_left.tag_names()
        print(current_tags[0])

    def loadFile(self):
        '''
        Load file, either an internal Moulinette file (a current translation) or a pdf file to ocr and translate
        '''
        file = self.filepath_entry.get()
        if file == "":
            msg.showerror("Error", "Please select a .pdf or a .moul file")
            return

        file_ext = file.split(".")[-1]
        if file_ext.lower() == "pdf":
            doOCR(file,ROOT,PROJECT,self.doOCR.get())    
        elif file_ext.lower() == "moul":
            pass
        else:
            msg.showerror("Error", "Wrong file extension")
            return

        # for index, (key,value) in enumerate(phrases.items()):
            

    # Utilities
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        try:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except:
            pass

    def mouse_scroll(self, event):
        try:
            x, y = self.winfo_pointerxy()
            if "scrollframe" in str(self.winfo_containing(x,y)):
                if event.delta:
                    self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                else:
                    if event.num == 5:
                        move = 1
                    else:
                        move = -1
                    self.canvas.yview_scroll(move, "units")
        except:
            pass

    def highlightText(self):
        '''Use the current mark which tracks the mouse position'''
        pass

    def browseDir(self):
        directory = filedialog.askdirectory()

        while directory and not os.path.isdir(directory):
            msg.showerror("Error", "This is not a directory")
            directory = filedialog.askopenfilename()

        if directory:
            self.filepath_entry.delete(0, 'end')
            self.filepath_entry.insert(0, directory)

        self.loadFile()



if __name__ == "__main__":
    moulinette = Moulinette()
    moulinette.mainloop()