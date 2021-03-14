# Some useful links:
# General:
# https://www.tcl.tk/man/tcl8.4/TkCmd/text.htm
# https://docs.python.org/3/library/tk.html
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/text.html
# https://stackoverflow.com/questions/21717115/using-tk-to-create-a-text-editor
# https://github.com/manjunathb4461/text-editor-with-tkinter/blob/master/main.py
# Tags: 
# https://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget/3781773#3781773
# https://stackoverflow.com/questions/3732605/add-advanced-features-to-a-tkinter-text-widget
# Images:
# https://pillow.readthedocs.io/en/stable/reference/ImageGrab.html
# https://github.com/ponty/pyscreenshot
# Line numbers:
# https://stackoverflow.com/a/16375233
import requests
import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import filedialog
from tkinter import Scrollbar
import tkinter.font as tkFont
from utils import *
import subprocess

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
        self.filepath_entry.insert(0,"/home/carter/Desktop/Cours/Thèse/Programming_economics/translation_project/Tinbergen - 1930 - De werkloosheid.pdf")
        self.browse_button = ttk.Button(self.settings_frame, text="Browse", command=self.browseFiles)
        self.browse_button.grid(column=2,row=0, pady=(2,2), sticky="nsew", padx=(5,5))

        self.browse_button = ttk.Button(self.settings_frame, text="Load File", command=self.loadFile)
        self.browse_button.grid(column=1,row=1,columnspan=2, pady=(2,2), sticky="nsew", padx=(5,5))
        
        self.doOCR = tk.BooleanVar()
        self.doOCR.set(False)
        ttk.Checkbutton(self.settings_frame, text='do OCR', variable=self.doOCR,onvalue=True,offvalue=False).grid(column=3,row=0,padx=(5,5), pady=(2,2))

        self.doTranslate = tk.BooleanVar()
        self.doTranslate.set(False)
        ttk.Checkbutton(self.settings_frame, text='Translate', variable=self.doTranslate,onvalue=True,offvalue=False).grid(column=4,row=0,padx=(5,5), pady=(2,2))

        ttk.Label(self.settings_frame, text='Language: ').grid(column=3,row=1,padx=(5,5), pady=(2,2))
        self.lang = tk.StringVar()
        ttk.Combobox(self.settings_frame, textvariable=self.lang, font=self.default_font,state="readonly", 
            values=("Dutch","German","Italian")).grid(column=4,row=1, pady=(2,2), sticky="nsew", columnspan=2)

        # Left editor (original text)
        self.editor_left = tk.Text(wrap="word", background="white",undo=True,autoseparators=True,maxundo=-1,borderwidth=0, highlightthickness=0,spacing3=10)
        self.scrollbar_left = Scrollbar(orient="vertical", borderwidth=1,command=self.editor_left.yview)

        self.editor_left.configure(yscrollcommand=self.scrollbar_left.set)
        self.scrollbar_left.pack(in_=self.left,side=tk.RIGHT,fill=tk.Y,expand=False)
        self.editor_left.pack(in_=self.left,side=tk.LEFT,expand=True,fill=tk.BOTH)
        
        # Right editor (translated text)
        self.editor_right = tk.Text(wrap="word", background="white",undo=True,autoseparators=True,maxundo=-1,borderwidth=0, highlightthickness=0)
        self.scrollbar_right = Scrollbar(orient="vertical", borderwidth=1,command=self.editor_right.yview)

        self.editor_right.configure(yscrollcommand=self.scrollbar_right.set)
        self.scrollbar_right.pack(in_=self.right,side=tk.RIGHT,fill=tk.Y,expand=False)
        self.editor_right.pack(in_=self.right,side=tk.LEFT,expand=True,fill=tk.BOTH)

        # Bindings
        self.editor_left.bind("<Control-s>", self.saveFile)
        self.editor_left.bind("<Control-Shift-s>", self.saveFileAndTranslate)

    def saveFile(self,event):
        original_text = self.editor_left.get('1.0', tk.END)
        translated_text = self.editor_right.get('1.0', tk.END)
        print(self.editor_left.dump('1.0', tk.END))

        with open(ROOT + PROJECT + PATH_SEP + "original.txt", "w") as f:
            f.write(original_text.replace("•",""))
        with open(ROOT + PROJECT + PATH_SEP + "translation.txt", "w") as f:
            f.write(translated_text.replace("•",""))

        with open(ROOT + PROJECT + PATH_SEP + 'project.moul', 'wb') as dict_phrases:
            pickle.dump(self.text, dict_phrases)

    def saveFileAndTranslate(self,event):
        self.translateText()
        self.saveFile()

    def printTags(self):
        current_tags = self.editor_left.tag_names()
        print(current_tags[0])

    def loadFile(self):
        '''
        Load file, either a project folder or a pdf file to ocr and translate
        '''
        file = self.filepath_entry.get()
        if file == "":
            msg.showerror("Error", "Please select a .pdf file or a folder")
            return

        file_ext = file.split(".")[-1]
        if file_ext.lower() == "pdf":
            extractOCR(file,ROOT,PROJECT,self.doOCR.get())
            self.buildPhrasesFromOriginal()
        elif file_ext.lower() == "moul":
            with open(file, 'rb') as dict_phrases:
                self.text = pickle.load(dict_phrases)
            self.buildPhrasesFromProject()
        else:
            msg.showerror("Error", "Wrong file extension")
            return

        if self.doTranslate.get():
            self.translateText()

    def buildPhrasesFromOriginal(self):
        with open(ROOT + PROJECT + PATH_SEP + "original.txt","r") as f:
            text = f.read()

        self.text = {}

        phrases = re.split("(?<!\d)(?<!\s\S)(?<!\S\.\S)[\.\!\?](?!\))(?!\d)",text)
        for i,ph in enumerate(phrases):
            cur_ph = " " + ph.strip() + "."
            # Perhaps do other operations such as detection of endline break
            if i == 0:
                self.text['phrase_'+format(i)] = Phrase(cur_ph,foll=i+1)
                self.editor_left.mark_set("beg_phrase_"+format(i),"insert")
                self.editor_left.mark_gravity("beg_phrase_"+format(i),tk.LEFT)
            else:
                self.text['phrase_'+format(i)] = Phrase(cur_ph,prev=i-1,foll=i+1)

            self.editor_left.insert("insert", cur_ph)
            self.editor_left.mark_set("end_phrase_"+format(i),"insert")
            self.editor_left.mark_gravity("end_phrase_"+format(i),tk.LEFT)
            cur_ind = self.editor_left.index("end_phrase_"+format(i))
            new_ind = format(float(cur_ind) + 0.1)
            self.editor_left.insert(new_ind, "•")
            self.editor_left.mark_set("beg_phrase_"+format(i+1),"insert")
            self.editor_left.mark_gravity("beg_phrase_"+format(i),tk.LEFT)
            self.editor_left.update()
        
        self.n_phrases = i

    def buildPhrasesFromProject(self):
        for i, (key,phrase) in enumerate(self.text.items()):
            if i == 0:
                self.editor_left.mark_set("beg_phrase_" + format(i),tk.END)
                self.editor_right.mark_set("beg_phrase_" + format(i),tk.END)

            self.editor_left.insert(tk.END, phrase.phrase)
            self.editor_left.mark_set("end_phrase_"+format(i),tk.END)
            self.editor_left.insert(tk.END, "•")
            self.editor_left.mark_set("beg_phrase_"+format(i+1),tk.END)
            self.editor_left.update()

            if phrase.translation != '':
                self.editor_right.insert(tk.END,phrase.translation)
                self.editor_right.mark_set("end_phrase_"+format(i),tk.END)
                self.editor_right.mark_gravity("end_phrase_"+format(i),tk.LEFT)
                self.editor_right.insert(tk.END, "•")
                self.editor_right.mark_set("end_phrase_"+format(i+1),tk.END)
                self.editor_right.update()

        self.n_phrases = i

    def translateText(self):
        for i, (key,phrase) in enumerate(self.text.items()):
            if i == 0:
                self.editor_right.mark_set("beg_" + key,tk.END)
            if phrase.changed:
                # result = subprocess.run(["trans", lang_map[self.lang.get()] + ':en', '-brief', phrase.phrase], stdout=subprocess.PIPE)
                # phrase.translation = result.stdout.decode('utf-8')[-1]
                phrase.translation = translate_text(phrase.phrase,source=lang_map[self.lang.get()],target="en")
                phrase.changed = False

            self.editor_right.insert(tk.END,phrase.translation)
            self.editor_right.mark_set("end_" + key,tk.END)
            self.editor_right.mark_gravity("end_phrase_"+format(i),tk.LEFT)
            self.editor_right.insert(tk.END, "•")
            self.editor_right.mark_set("beg_" + key,tk.END)
            self.editor_right.update()

    # Utilities
    def highlightText(self):
        '''Use the current mark which tracks the mouse position'''
        pass

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir=ROOT)

        if filename:
            self.filepath_entry.delete(0, 'end')
            self.filepath_entry.insert(0, filename)

if __name__ == "__main__":
    moulinette = Moulinette()
    moulinette.mainloop()