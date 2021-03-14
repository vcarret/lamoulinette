# Some useful links:
# General:
# https://www.tcl.tk/man/tcl8.4/TkCmd/text.htm
# https://docs.python.org/3/library/tk.html
# http://epydoc.sourceforge.net/stdlib/Tkinter.Text-class.html
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
from PIL import ImageTk, Image

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
        self.right = ttk.Frame(self.content)

        self.content.pack(fill = tk.BOTH,expand=True)
        self.top.pack(side = tk.TOP, fill = tk.X, padx=10,pady=5,ipadx=5,ipady=5)
        self.left.pack(side = tk.LEFT, expand=True, fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5)
        self.right.pack(side = tk.RIGHT, expand=True, fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5)

        # Functions
        self.check_num_wrapper = (self.content.register(check_num), '%P')

        # Top settings
        # self.settings_frame = ttk.Labelframe(self.top, text="Settings")
        # self.settings_frame.pack(fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5)

        self.notebook_settings = ttk.Notebook(self.top)
        self.notebook_settings.pack(fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5,expand=True)

        # Loading settings
        self.load_settings = ttk.Frame(self.notebook_settings)
        # self.load_settings.pack(fill=tk.BOTH,expand=True)
        # self.notebook_settings.add(self.load_settings)

        ttk.Label(self.load_settings, text='File: ').grid(column=0,row=0)
        self.filepath_entry = ttk.Entry(self.load_settings, font=self.default_font)
        self.filepath_entry.grid(column=1,row=0, pady=(2,2), sticky="nsew")
        self.filepath_entry.insert(0,"/home/carter/Documents/Moulinette/Tinbergen - 1930 - De werkloosheid/project.moul")#/home/carter/Desktop/Cours/Thèse/Programming_economics/translation_project/Tinbergen - 1930 - De werkloosheid.pdf
        self.browse_button = ttk.Button(self.load_settings, text="Browse", command=self.browseFiles)
        self.browse_button.grid(column=2,row=0, pady=(2,2), sticky="nsew", padx=(5,5))

        self.load_button = ttk.Button(self.load_settings, text="Load File", command=self.loadFile)
        self.load_button.grid(column=1,row=1,columnspan=2, pady=(2,2), sticky="nsew", padx=(5,5))

        self.project = ""
        
        self.doOCR = tk.BooleanVar()
        self.doOCR.set(False)
        ttk.Checkbutton(self.load_settings, text='do OCR', variable=self.doOCR,onvalue=True,offvalue=False).grid(column=3,row=0,padx=(5,5), pady=(2,2))

        self.doTranslate = tk.BooleanVar()
        self.doTranslate.set(False)
        ttk.Checkbutton(self.load_settings, text='Translate', variable=self.doTranslate,onvalue=True,offvalue=False).grid(column=4,row=0,padx=(5,5), pady=(2,2))

        ttk.Label(self.load_settings, text='Language: ').grid(column=3,row=1,padx=(5,5), pady=(2,2))
        self.lang = tk.StringVar()
        ttk.Combobox(self.load_settings, textvariable=self.lang, font=self.default_font,state="readonly", 
            values=("Dutch","German","Italian")).grid(column=4,row=1, pady=(2,2), sticky="nsew", columnspan=2)

        ttk.Label(self.load_settings,text='First Page: ').grid(column=6, row=0, sticky='nsew')
        self.firstpage = tk.StringVar()
        self.firstPageBox = ttk.Entry(self.load_settings, textvariable=self.firstpage, validate='key', validatecommand=self.check_num_wrapper)
        self.firstPageBox.grid(column=7, row=0, sticky='nsew')
        self.firstPageBox.insert(0,1)

        # Editing settings
        self.edit_settings = ttk.Frame(self.notebook_settings)
        # self.edit_settings.pack(fill=tk.BOTH,expand=True)

        self.insert_button = ttk.Button(self.edit_settings, text="I",width=2, command=self.insertMark)
        self.insert_button.grid(column=0,row=0,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

        self.dontTranslate_button = ttk.Button(self.edit_settings, text="Ⱦ",width=2, command=self.dontTranslate)
        self.dontTranslate_button.grid(column=1,row=0,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

        self.findBox = ttk.Entry(self.edit_settings, font=self.default_font)
        self.findBox.grid(column=0,row=1,columnspan=2, pady=(2,2), sticky="nsew", padx=(2,2))
        self.findBox.bind("<Return>", self.find)

        self.find = ttk.Button(self.edit_settings, text="Find", command=self.find)
        self.find.grid(column=2,row=1,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

        self.replaceBox = ttk.Entry(self.edit_settings, font=self.default_font)
        self.replaceBox.grid(column=3,row=1,columnspan=2, pady=(2,2), sticky="nsew", padx=(2,2))
        self.replaceBox.bind("<Return>", self.replace)

        self.replace = ttk.Button(self.edit_settings, text="Replace", command=self.replace)
        self.replace.grid(column=5,row=1,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

        self.regexp = tk.BooleanVar()
        self.regexp.set(False)
        ttk.Checkbutton(self.edit_settings, text='regexp?', variable=self.regexp,onvalue=True,offvalue=False).grid(column=0,row=3,padx=(2,2), pady=(2,2))

        self.nocase = tk.BooleanVar()
        self.nocase.set(True)
        ttk.Checkbutton(self.edit_settings, text='nocase?', variable=self.nocase,onvalue=True,offvalue=False).grid(column=1,row=3,padx=(2,2), pady=(2,2))

        self.exact = tk.BooleanVar()
        self.exact.set(False)
        ttk.Checkbutton(self.edit_settings, text='exact?', variable=self.exact,onvalue=True,offvalue=False).grid(column=2,row=3,padx=(2,2), pady=(2,2))


        # End notebook settings
        self.notebook_settings.add(self.load_settings,text="Load")
        self.notebook_settings.add(self.edit_settings,text="Edit")

        # Left editor (original text)
        self.editor_left = tk.Text(wrap="word", background="white",undo=True,autoseparators=True,maxundo=-1,borderwidth=0, highlightthickness=0,spacing3=10)
        self.scrollbar_left = Scrollbar(orient="vertical", borderwidth=1,command=self.editor_left.yview)

        self.editor_left.configure(yscrollcommand=self.scrollbar_left.set)
        self.scrollbar_left.pack(in_=self.left,side=tk.RIGHT,fill=tk.Y,expand=False)
        self.editor_left.pack(in_=self.left,side=tk.LEFT,expand=True,fill=tk.BOTH)
        
        # Right panel
        self.notebook_rightpanel = ttk.Notebook(self.right)
        self.notebook_rightpanel.pack(fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5,expand=True)

        # Right editor (translated text)
        self.right_editor_content = ttk.Frame(self.notebook_rightpanel)
        self.right_editor_content.pack(fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5,expand=True)

        self.editor_right = tk.Text(wrap="word", background="white",undo=True,autoseparators=True,maxundo=-1,borderwidth=0, highlightthickness=0)
        self.scrollbar_right = Scrollbar(orient="vertical", borderwidth=1,command=self.editor_right.yview)

        self.editor_right.configure(yscrollcommand=self.scrollbar_right.set)
        self.scrollbar_right.pack(in_=self.right_editor_content,side=tk.RIGHT,fill=tk.Y,expand=False)
        self.editor_right.pack(in_=self.right_editor_content,side=tk.LEFT,expand=True,fill=tk.BOTH)

        # Right viewer
        self.right_viewer_content = ttk.Frame(self.notebook_rightpanel)
        self.right_viewer_content.pack(fill=tk.BOTH, padx=2,pady=2,ipadx=2,ipady=2,expand=True)

        self.scrollbar_viewer_right = Scrollbar(self.right_viewer_content,orient="vertical", borderwidth=1)
        self.viewer_right = tk.Canvas(self.right_viewer_content,background='gray65',yscrollcommand=self.scrollbar_viewer_right.set)#, scrollregion=(0, 0, 1000, 1000))
        # self.viewer_right.pack(fill=tk.BOTH, padx=2,pady=2,ipadx=2,ipady=2,expand=True)
        self.scrollbar_viewer_right.config(command=self.viewer_right.yview)

        # self.viewer_right.configure()
        self.scrollbar_viewer_right.pack(side=tk.RIGHT,fill=tk.Y,expand=False)
        self.viewer_right.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        self.viewer_right.config(scrollregion=self.right_viewer_content.bbox(tk.ALL))


        # End notebook settings
        self.notebook_rightpanel.add(self.right_viewer_content,text="Viewer")
        self.notebook_rightpanel.add(self.right_editor_content,text="Translation")


        # Tags
        self.editor_left.tag_configure("current_phrase", background="#d8d8d8")
        self.editor_left.tag_lower("current_phrase")

        # Bindings
        self.bind("<Control-s>", self.saveFile)
        self.bind("<Control-Shift-S>", self.saveFileAndTranslate)
        self.bind("<Control-i>", self.insertMark)
        self.unbind("<Control-f>")
        self.bind("<Control-Alt-f>", self.setFocusFinder)
        self.editor_left.bind("<Control-f>", self.setFocusFinder)
        self.bind("<Control-h>", self.setFocusReplace)
        self.editor_left.bind("<Control-a>", self.selectAll)

    def insertMark(self,event=None):
        cur_pos = self.editor_left.index("insert")
        prev_mark = self.getBegPhrase(cur_pos)
        print(prev_mark)
        pos_beg = self.editor_left.mark_previous(prev_mark)
        num = prev_mark.split("_")[2]
        pos_end = self.editor_left.index("end_phrase_"+format(num))

        self.editor_left.insert(cur_pos, "•")
        self.editor_left.mark_set("end_phrase_"+format(num),cur_pos)
        self.text["phrase_"+format(num)].phrase = self.editor_left.get(pos_beg,cur_pos).replace("•","")

        self.text["n_phrases"] += 1

        self.editor_left.mark_set("beg_phrase_"+format(self.text["n_phrases"]),cur_pos+"+1c")        
        self.editor_left.mark_set("end_phrase_"+format(self.text["n_phrases"]),pos_end)
        new_ph = self.editor_left.get(cur_pos,pos_end).replace("•","")

        self.text['phrase_'+format(self.text["n_phrases"])] = Phrase(new_ph,index=self.text["n_phrases"],prev=num,foll=self.text["phrase_"+format(num)].foll)

        self.text["phrase_"+format(num)].foll = format(self.text["n_phrases"])

    def saveFile(self,event):
        original_text = self.editor_left.get('1.0', tk.END)
        translated_text = self.editor_right.get('1.0', tk.END)

        if self.project == "":
            msg.showerror("Error", "No project selected")
            return

        with open(ROOT + self.project + PATH_SEP + "original.txt", "w") as f:
            f.write(original_text.replace("•",""))
        with open(ROOT + self.project + PATH_SEP + "translation.txt", "w") as f:
            f.write(translated_text.replace("•",""))

        self.rebuildPhrases()
        self.checkChanges()
        [print(x) for x in self.editor_left.dump('1.0', tk.END, **{"mark":True,'text':True})]
        with open(ROOT + self.project + PATH_SEP + 'project.moul', 'wb') as dict_phrases:
            pickle.dump((self.project,self.text), dict_phrases)

    def saveFileAndTranslate(self,event):
        original_text = self.editor_left.get('1.0', tk.END)
        translated_text = self.editor_right.get('1.0', tk.END)

        with open(ROOT + self.project + PATH_SEP + "original.txt", "w") as f:
            f.write(original_text.replace("•",""))

        self.rebuildPhrases()
        self.checkChanges()
        # self.translateText()
        
        with open(ROOT + self.project + PATH_SEP + "translation.txt", "w") as f:
            f.write(translated_text.replace("•",""))

        with open(ROOT + self.project + PATH_SEP + 'project.moul', 'wb') as dict_phrases:
            pickle.dump((self.project,self.text), dict_phrases)

    def rebuildPhrases(self):
        marks = self.editor_left.dump('1.0', tk.END, **{"mark":True})
        begend_prev = None
        first = True
        for i,(obj,name,ind) in enumerate(marks):
            tmp = name.split("_")
            begend = tmp[0]
            try:
                num = tmp[2]
            except:
                continue

            if i > 0:
                if begend == "beg" and begend == begend_prev:
                    # Displace the index to the place of the index that is being deleted
                    prev_ind = self.editor_left.index("beg_phrase_"+num_prev)
                    self.editor_left.mark_set("beg_phrase_"+num,prev_ind)

                    self.editor_left.mark_unset("beg_phrase_"+num_prev)
                    self.editor_left.mark_unset("end_phrase_"+num_prev)
                    prev = self.text["phrase_"+num_prev].prev
                    foll = self.text["phrase_"+num_prev].foll
                    if prev is not None:
                        self.text["phrase_"+format(prev)].foll = foll
                    else:
                        self.text["first"] = foll
                    if foll is not None:
                        self.text["phrase_"+format(foll)].prev = prev
                    else:
                        self.text["last"] = prev
                    del self.text["phrase_"+format(num_prev)]

            begend_prev = begend
            num_prev = num

    def checkChanges(self):
        i = self.text["phrase_"+format(self.text["first"])].index
        while i is not None:
            key = "phrase_"+format(i)
            phrase = self.text[key]

            beg_phrase = self.editor_left.index("beg_phrase_"+format(phrase.index))
            end_phrase = self.editor_left.index("end_phrase_"+format(phrase.index))
            cur_phrase = self.editor_left.get(beg_phrase,end_phrase)
            if phrase.phrase != cur_phrase:
                phrase.phrase = cur_phrase
                phrase.changed = True

            i = self.text[key].foll

    def loadFile(self):
        '''
        Load file, either a pdf to ocr and translate or a moul file (project)
        '''
        file = self.filepath_entry.get()
        if file == "":
            msg.showerror("Error", "Please select a .pdf or . moul file")
            return

        file_ext = file.split(".")[-1]
        if file_ext.lower() == "pdf":
            self.project = extractOCR(file,ROOT,self.project,self.doOCR.get(),int(self.firstpage.get()))
            self.buildPhrasesFromOriginal()
        elif file_ext.lower() == "moul":
            with open(file, 'rb') as dict_phrases:
                self.project,self.text = pickle.load(dict_phrases)
            #self.project = file.split(".")[0].split(PATH_SEP)[-2]
            self.buildPhrasesFromProject()
        else:
            msg.showerror("Error", "Wrong file extension")
            return

        if self.doTranslate.get():
            self.translateText()

        self.loadViewer()
        self.highlight_current_line()

    def loadViewer(self):
        self.update()
        height, width = self.right_viewer_content.winfo_height(),self.right_viewer_content.winfo_width()
        self.images = []
        root_path = ROOT + self.project + PATH_SEP + "orig_images" + PATH_SEP
        for i,path in enumerate(os.listdir(root_path)):
            self.images.append(Image.open(root_path + path).resize((height, width), Image.ANTIALIAS))

            image = ImageTk.PhotoImage(self.images[i])
            print(image.width(),image.height())
            self.viewer_right.create_image((50, height*i+10), image=image,anchor='nw')
            # self.viewer_right.image = image
                
        self.viewer_right.configure(scrollregion = self.viewer_right.bbox("all"))


    def buildPhrasesFromOriginal(self):
        with open(ROOT + self.project + PATH_SEP + "original.txt","r") as f:
            text = f.read()

        self.text = {}

        phrases = re.split("(?<!\d)(?<!\s\S)(?<!\S\.\S)[\.\!\?](?!\))(?!\d)",text)
        self.editor_left.insert("1.0", "•")
        for i,ph in enumerate(phrases):
            cur_ph = " " + ph.strip() + "."
            cur_ph = cur_ph.replace("•","*")
            # Perhaps do other operations such as detection of endline break

            prev = i-1 if i > 0 else None
            foll = i+1 if i < (len(phrases)-1) else None
            self.text['phrase_'+format(i)] = Phrase(cur_ph,index=i,prev=prev,foll=foll)

            self.editor_left.mark_set("beg_phrase_"+format(i),"insert")
            self.editor_left.mark_gravity("beg_phrase_"+format(i),tk.LEFT)

            self.editor_left.insert("insert", cur_ph)
            self.editor_left.insert("insert", "•")

            cur_ind = self.editor_left.index("insert")
            new_ind = cur_ind+"-1c"
            self.editor_left.mark_set("end_phrase_"+format(i),new_ind)
            self.editor_left.mark_gravity("end_phrase_"+format(i),tk.RIGHT)
        
        self.text["first"] = 0
        self.text["last"] = i
        self.text["n_phrases"] = i

    def buildPhrasesFromProject(self):
        i = self.text["phrase_"+format(self.text["first"])].index       
        self.editor_left.insert("insert", "•")
        self.editor_right.insert("insert", "•")
        while i is not None:
            key = "phrase_"+format(i)
            phrase = self.text[key]
        # for i, (key,phrase) in enumerate(self.text.items()):
            self.editor_left.mark_set("beg_" + key,"insert")
            self.editor_left.mark_gravity("beg_"+key,tk.LEFT)
            self.editor_right.mark_set("beg_" + key,"insert")
            self.editor_right.mark_gravity("beg_"+key,tk.LEFT)

            self.editor_left.insert("insert", phrase.phrase)
            self.editor_left.insert("insert", "•")
            cur_ind = self.editor_left.index("insert")
            new_ind = cur_ind+"-1c"
            self.editor_left.mark_set("end_"+key,new_ind)
            self.editor_left.mark_gravity("end_"+key,tk.RIGHT)
            # self.editor_left.update()

            self.editor_right.insert("insert", phrase.translation)
            self.editor_right.insert("insert", "•")
            cur_ind = self.editor_right.index("insert")
            new_ind = cur_ind+"-1c"
            self.editor_right.mark_set("end_"+key,new_ind)
            self.editor_right.mark_gravity("end_"+key,tk.RIGHT)
            # self.editor_right.update()

            i = self.text[key].foll

    def translateText(self):
        i = self.text["phrase_"+format(self.text["first"])].index       
        self.editor_right.insert("insert", "•")
        while i is not None:
            key = "phrase_"+format(i)
            phrase = self.text[key]

            self.editor_right.mark_set("beg_" + key,tk.END)
            self.editor_right.mark_gravity("beg_" + key,tk.LEFT)
            if not phrase.translate:
                phrase.translation = phrase.phrase
            elif phrase.changed:
                # result = subprocess.run(["trans", lang_map[self.lang.get()] + ':en', '-brief', phrase.phrase], stdout=subprocess.PIPE)
                # phrase.translation = result.stdout.decode('utf-8')[-1]
                phrase.translation = translate_text(phrase.phrase,source=lang_map[self.lang.get()],target="en")
                phrase.changed = False

            self.editor_right.insert("insert", phrase.translation)
            self.editor_right.insert("insert", "•")
            cur_ind = self.editor_right.index("insert")
            new_ind = cur_ind+"-1c"
            self.editor_right.mark_set("end_"+key,new_ind)
            self.editor_right.mark_gravity("end_"+key,tk.RIGHT)
            self.editor_right.update()

            i = self.text[key].foll

    def dontTranslate(self):
        # Maybe find a way to signal it?
        cur_pos = self.editor_left.index("insert")
        prev_mark = self.getBegPhrase(cur_pos)
        self.text["phrase_"+prev_mark.split("_")[-1]].translate = False

    def find(self,event=None):
        self.editor_left.tag_remove('found','1.0',tk.END)
        s = self.findBox.get()
        if s:
            idx = "1.0"
            while True:
                idx = self.editor_left.search(s,idx,stopindex=tk.END,nocase=self.nocase.get(),regexp=self.regexp.get(),exact=self.exact.get()) 
                if not idx: 
                    break

                lastidx = '% s+% dc' % (idx, len(s)) 
                self.editor_left.tag_add('found', idx, lastidx)  
                idx = lastidx  

            self.editor_left.tag_config('found', foreground ='red') 
        self.findBox.focus_set() 

    def replace(self,event=None):
        self.editor_left.tag_remove('found','1.0',tk.END)
        s = self.findBox.get()
        r = self.replaceBox.get()
        if s:
            idx = "1.0"
            while True:
                idx = self.editor_left.search(s,idx,stopindex=tk.END,nocase=self.nocase.get(),regexp=self.regexp.get(),exact=self.exact.get()) 
                if not idx: 
                    break

                lastidx = '% s+% dc' % (idx, len(s)) 
                self.editor_left.delete(idx, lastidx)  
                self.editor_left.insert(idx, r)

                lastidx = '% s+% dc' % (idx, len(r)) 
                self.editor_left.tag_add('found', idx, lastidx)  
                idx = lastidx  

            self.editor_left.tag_config('found', foreground ='green',background='yellow') 
        self.findBox.focus_set() 

    def selectAll(self,event):
        self.editor_left.tag_add("sel","1.0",tk.END)
        return "break"
        # self.editor_left.icursor(tk.END)

    def highlight_current_line(self, interval=100):
        '''Updates the 'current line' highlighting every "interval" milliseconds'''
        self.editor_left.tag_remove("current_phrase", 1.0, "end")
        cur_pos = self.editor_left.index("insert")
        prev_mark = self.getBegPhrase(cur_pos)
        # try:
        pos_beg = self.editor_left.index(prev_mark)
        pos_end = self.editor_left.index(prev_mark.replace("beg","end"))
        # except:
            # pass
        self.editor_left.tag_add("current_phrase", pos_beg, pos_end)
        self.after(interval, self.highlight_current_line)


    def getBegPhrase(self,cur_pos):
        prev_mark = self.editor_left.mark_previous(cur_pos)
        if prev_mark == "current" or prev_mark == "tk::anchor1":
            prev_mark = self.editor_left.mark_previous(self.editor_left.index("current"))
        return prev_mark

    def setFocusFinder(self,event):
        self.findBox.insert(0,self.editor_left.get("sel.first","sel.last"))
        self.findBox.focus_set()
        return "break"

    def setFocusReplace(self,event):
        self.replaceBox.insert(0,self.editor_left.get("sel.first","sel.last"))
        self.replaceBox.focus_set()

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir=ROOT)

        if filename:
            self.filepath_entry.delete(0, 'end')
            self.filepath_entry.insert(0, filename)

if __name__ == "__main__":
    moulinette = Moulinette()
    moulinette.mainloop()