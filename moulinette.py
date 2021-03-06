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
from utils import *

class Moulinette(tk.Tk):
	def __init__(self):
		super().__init__()

		self.title("La Moulinette")
		self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth()-3, self.winfo_screenheight()-3))
		self.default_font = tkFont.nametofont("TkDefaultFont")
		self.default_font.configure(size=16, family="courier 10 pitch")

		self.content = ttk.Frame(self)
		self.top = ttk.Frame(self.content)
		self.left = ttk.Frame(self.content)
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
		# self.filepath_entry.insert(0,"/home/carter/Desktop/Cours/Th??se/Programming_economics/translation_project/Tinbergen - 1930 - De werkloosheid.pdf")#
		# self.filepath_entry.insert(0,"/home/carter/Documents/Moulinette/Tinbergen - 1930 - De werkloosheid/project.moul")
		self.browse_button = ttk.Button(self.load_settings, text="Browse", command=self.browseFiles)
		self.browse_button.grid(column=2,row=0, pady=(2,2), sticky="nsew", padx=(5,5))

		self.browse_zot_button = ttk.Button(self.load_settings, text="Browse Zotero", command=self.browseZotero)
		self.browse_zot_button.grid(column=1,row=1,columnspan=1, pady=(2,2), sticky="nsew", padx=(5,5))

		ttk.Button(self.load_settings, text="???", command=self.updateZotero).grid(column=0,row=1,columnspan=1, pady=(2,2), sticky="nsew", padx=(5,5))

		self.load_button = ttk.Button(self.load_settings, text="Load File", command=self.loadFile)
		self.load_button.grid(column=2,row=1,columnspan=1, pady=(2,2), sticky="nsew", padx=(5,5))

		self.project = ""
		
		self.desalt = tk.BooleanVar()
		self.desalt.set(False)
		ttk.Checkbutton(self.load_settings, text='de-salt', variable=self.desalt,onvalue=True,offvalue=False).grid(column=3,row=0,padx=(5,5), pady=(2,2))

		# We should always avoid translating during the first run. Force user to clean the text before sending it to Google Translate API which charges per char
		self.doTranslate = tk.BooleanVar()
		self.doTranslate.set(False)
		# ttk.Checkbutton(self.load_settings, text='Translate', variable=self.doTranslate,onvalue=True,offvalue=False).grid(column=4,row=0,padx=(5,5), pady=(2,2))

		ttk.Label(self.load_settings, text='Language: ').grid(column=3,row=1,padx=(5,5), pady=(2,2))
		self.lang = tk.StringVar()
		ttk.Combobox(self.load_settings, textvariable=self.lang, font=self.default_font,state="readonly", 
			values=("Dutch","German","Italian","Norwegian","French")).grid(column=4,row=1, pady=(2,2), sticky="nsew", columnspan=2)

		ttk.Label(self.load_settings,text='First Page: ').grid(column=4, row=0, sticky='nsew')
		self.firstpage = tk.StringVar()
		self.firstPageBox = ttk.Entry(self.load_settings, textvariable=self.firstpage, validate='key', validatecommand=self.check_num_wrapper)
		self.firstPageBox.grid(column=5, row=0, sticky='nsew')
		self.firstPageBox.insert(0,1)

		# Editing settings
		self.edit_settings = ttk.Frame(self.notebook_settings)
		self.edit_settings.pack(fill=tk.BOTH,expand=True)

		self.insert_button = ttk.Button(self.edit_settings, text="I",width=2, command=self.insertImage)
		self.insert_button.grid(column=0,row=0,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

		self.dontTranslate_button = ttk.Button(self.edit_settings, text="??",width=2, command=self.dontTranslate)
		self.dontTranslate_button.grid(column=1,row=0,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

		self.footnote_button = ttk.Button(self.edit_settings, text="F",width=2, command=self.insertFn)
		self.footnote_button.grid(column=2,row=0,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

		self.makePhrases_button = ttk.Button(self.edit_settings, text="P",width=2, command=self.buildPhrasesFromEditor)
		self.makePhrases_button.grid(column=3,row=0,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

		self.translate_button = ttk.Button(self.edit_settings, text="T",width=2, command=self.translateText)
		self.translate_button.grid(column=4,row=0,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

		self.makePDF_button = ttk.Button(self.edit_settings, text="M",width=2, command=self.makePDF)
		self.makePDF_button.grid(column=5,row=0,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

		self.uploadPDF_button = ttk.Button(self.edit_settings, text="U",width=2, command=self.uploadPDF)
		self.uploadPDF_button.grid(column=6,row=0,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

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
		ttk.Checkbutton(self.edit_settings, text='regexp?', variable=self.regexp,onvalue=True,offvalue=False).grid(column=0,row=2,padx=(2,2), pady=(2,2))

		self.nocase = tk.BooleanVar()
		self.nocase.set(True)
		ttk.Checkbutton(self.edit_settings, text='nocase?', variable=self.nocase,onvalue=True,offvalue=False).grid(column=1,row=2,padx=(2,2), pady=(2,2))

		self.exact = tk.BooleanVar()
		self.exact.set(False)
		ttk.Checkbutton(self.edit_settings, text='exact?', variable=self.exact,onvalue=True,offvalue=False).grid(column=2,row=2,padx=(2,2), pady=(2,2))

		self.findFirstPageBox = ttk.Entry(self.edit_settings, font=self.default_font)
		self.findFirstPageBox.grid(column=3,row=2,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

		ttk.Button(self.edit_settings, text="Find pages", command=self.findPages).grid(column=4,row=2,columnspan=1, pady=(2,2), sticky="nsew", padx=(2,2))

		# End notebook settings
		self.notebook_settings.add(self.load_settings,text="Load")
		self.notebook_settings.add(self.edit_settings,text="Edit")

		# Left panel
		self.notebook_leftpanel = ttk.Notebook(self.left)
		self.notebook_leftpanel.pack(fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5,expand=True)

		# Left editor (original text)
		self.left_editor_content = ttk.Frame(self.notebook_leftpanel)
		self.left_editor_content.pack(fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5,expand=True)

		self.editor_left = tk.Text(wrap="word", background="white",undo=True,autoseparators=True,maxundo=-1,borderwidth=0, highlightthickness=0,spacing3=10)
		self.scrollbar_left = Scrollbar(orient="vertical", borderwidth=1,command=self.editor_left.yview)

		self.editor_left.configure(yscrollcommand=self.scrollbar_left.set)
		self.scrollbar_left.pack(in_=self.left_editor_content,side=tk.RIGHT,fill=tk.Y,expand=False)
		self.editor_left.pack(in_=self.left_editor_content,side=tk.LEFT,expand=True,fill=tk.BOTH)
		
		# Zotero settings
		with open("zotero_key.json","r") as f:
			self.zotero_api = json.load(f)

		self.apiInstance = ApiCall(self.zotero_api["api_key"],self.zotero_api["lib_type"],self.zotero_api["lib_id"])

		self.zotero_settings = tk.Frame(self.notebook_leftpanel)
		self.zotero_settings.pack(fill=tk.BOTH, padx=2,pady=2,ipadx=2,ipady=2,expand=True)

		ttk.Label(self.zotero_settings, text='Destination: ').grid(column=0,row=0,padx=(2,2), pady=(2,2))
		self.destination = tk.StringVar()
		self.destChoices = ttk.Combobox(self.zotero_settings, textvariable=self.destination, font=self.default_font,state="readonly", 
			values=list(self.zotero_api["destinations"].keys()))
		self.destChoices.grid(column=1,row=0, pady=(2,2), sticky="nsew", columnspan=2)
		self.destChoices.current(0)

		ttk.Label(self.zotero_settings, text='Item Type: ').grid(column=0,row=1,padx=(2,2), pady=(2,2))
		self.itemType = tk.StringVar()
		self.itemChoices = ttk.Combobox(self.zotero_settings, textvariable=self.itemType, font=self.default_font,state="readonly", 
			values=item_types)
		self.itemChoices.grid(column=1,row=1, pady=(2,2), sticky="nsew", columnspan=2)
		self.itemChoices.current(0)
		self.itemChoices.bind("<<ComboboxSelected>>", self.itemTypeUpdated)

		ttk.Label(self.zotero_settings, text='Creator: ').grid(column=0,row=2,padx=(2,2), pady=(2,2))
		self.firstName = tk.StringVar()
		ttk.Entry(self.zotero_settings, textvariable=self.firstName, font=self.default_font).grid(column=1,row=2, pady=(2,2), sticky="nsew", columnspan=1)
		self.lastName = tk.StringVar()
		ttk.Entry(self.zotero_settings, textvariable=self.lastName, font=self.default_font).grid(column=2,row=2, pady=(2,2), sticky="nsew", columnspan=1)

		# End notebook settings
		self.notebook_leftpanel.add(self.left_editor_content,text="Editor")
		self.notebook_leftpanel.add(self.zotero_settings,text="Zotero")

		# Right panel
		self.notebook_rightpanel = ttk.Notebook(self.right)
		self.notebook_rightpanel.pack(fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5,expand=True)

		# Right editor (translated text)
		self.right_editor_content = ttk.Frame(self.notebook_rightpanel)
		self.right_editor_content.pack(fill=tk.BOTH, padx=10,pady=5,ipadx=5,ipady=5,expand=True)

		self.editor_right = CustomText(self.right_editor_content) 
		# tk.Text(wrap="word", background="white",undo=True,autoseparators=True,maxundo=-1,borderwidth=0, highlightthickness=0,spacing3=10)
		self.scrollbar_right = Scrollbar(orient="vertical", borderwidth=1,command=self.editor_right.yview)
		self.editor_right.configure(yscrollcommand=self.scrollbar_right.set)
		self.linenumbers = TextLineNumbers(self.right_editor_content, width=30)
		self.linenumbers.attach(self.editor_right)

		self.scrollbar_right.pack(side=tk.RIGHT,fill=tk.Y,expand=False)
		self.linenumbers.pack(side="left", fill="y")
		self.editor_right.pack(side=tk.RIGHT,expand=True,fill=tk.BOTH)

		self.editor_right.bind("<<Change>>", self._on_change)
		self.editor_right.bind("<Configure>", self._on_change)

		# Right viewer
		self.right_viewer_content = ttk.Frame(self.notebook_rightpanel)
		self.right_viewer_content.pack(fill=tk.BOTH, padx=2,pady=2,ipadx=2,ipady=2,expand=True)

		# End notebook settings
		self.notebook_rightpanel.add(self.right_viewer_content,text="Viewer")
		self.notebook_rightpanel.add(self.right_editor_content,text="Translation")


		# Tags
		# self.editor_left.tag_configure("current_phrase", background="#d8d8d8")
		# self.editor_left.tag_lower("current_phrase")

		# Bindings
		self.bind("<Control-s>", self.saveProject)
		self.bind("<Control-Shift-S>", self.saveProject)
		# self.unbind("<Control-f>")
		self.bind("<Control-h>", self.setFocusReplace)
		self.bind("<Control-p>", self.buildPhrasesFromEditor)
		self.bind("<Alt-r>", self.insertImage)
		self.bind("<Alt-Left>",self.imageLeft)
		self.bind("<Alt-Right>",self.imageRight)
		# self.editor_left.unbind("<Control-Right>")

		self.editor_left.bind("<Control-BackSpace>", self.deleteWord)
		self.editor_left.bind("<Control-f>", self.setFocusFinder)
		self.editor_left.bind("<Control-a>", self.selectAll)
		self.editor_left.bind("<Control-Return>", self.insertPar)
		self.editor_left.bind("<Control-KP_Enter>", self.insertPar)
		self.editor_left.bind("<KP_Enter>", self.insertSimpleNewl)
		self.editor_left.bind("<Alt-f>", self.insertFootnote)
		self.editor_left.bind("<Alt-i>", self.insertItalics)
		self.editor_left.bind("<Alt-u>", self.insertUnderline)
		self.editor_left.bind("<Alt-b>", self.insertBold)
		self.editor_left.bind("<Alt-e>", self.insertEquation)
		self.editor_left.bind("<Alt-c>", self.insertCenterline)
		self.editor_left.bind("<Alt-Shift-E>", self.insertEquation)
		self.editor_left.bind("<Alt-p>", self.insertSimplePar)
		self.editor_left.bind("<Control-Shift-L>", self.replLinebreaks)
		# self.bind("<KeyPress>",self.printEv)

		self.editor_right.bind("<Alt-i>", self.insertItalicsRight)

	def printEv(self,event):
		print(event)

	def saveProject(self,event=None):
		'''Saves the original and translated texts, the zotero item and the project name. With shift pressed, also saves changes made to Zotero metadata''' 
		original_text = self.editor_left.get('1.0', tk.END)
		translated_text = self.editor_right.get('1.0', tk.END)

		if self.project == "":
			msg.showerror("Error", "No project selected")
			return

		with open(ROOT + self.project + PATH_SEP + "original.txt", "w") as f:
			f.write(original_text.replace("???",""))

		with open(ROOT + self.project + PATH_SEP + "translation.txt", "w") as f:
			f.write(translated_text.replace("???",""))

		with open(ROOT + self.project + PATH_SEP + ".translation", "wb") as f:
			pickle.dump(self.editor_right.dump('1.0', tk.END, **{"tag":True}),f)

		# [print(x) for x in self.editor_left.dump('1.0', tk.END, **{"mark":True,'text':True})]
		if event and event.state == 21:# code for ctrl+shift+S
			for k,v in self.values_zotero.items():
				self.zotItem.update(k,v.get())
			
			self.zotItem.template["itemType"] = self.itemType.get()
			self.zotItem.template["creators"] = [{
				'creatorType': 'author',
				'firstName': self.firstName.get(),
				'lastName': self.lastName.get()
			}]

			try:
				resp = self.apiInstance.updateItem(self.zotItem)
			except:
				version = self.apiInstance.api_instance.item(self.zotItem.template["key"])['version']
				self.zotItem.template["version"] = version
				resp = self.apiInstance.updateItem(self.zotItem)

			if not resp:
				print("something went wrong with Zotero update")

		with open(ROOT + self.project + PATH_SEP + 'project.moul', 'wb') as f:
			pickle.dump((self.zotItem,self.project), f)

	def loadZoteroItem(self,itemKey):
		item = self.apiInstance.api_instance.item(itemKey)
		data = ""
		if "meta" in item:
			if "creatorSummary" in item["meta"]:
				data += item["meta"]["creatorSummary"] 
			if "parsedDate" in item["meta"]:
				data += " - " + item["meta"]["parsedDate"]
		if "data" in item:
			if "title" in item["data"]:
				data += " - " + item["data"]["title"]

		self.project = data
		self.zotItem = ZotItem(self.itemType.get())
		self.zotItem.template = item["data"]
		self.loadZotero()
		self.update()

		if not path.exists(ROOT + self.project):
			mkdir(ROOT + self.project)

		file = ROOT + self.project + PATH_SEP + self.project +'.pdf'
		if not os.path.exists(file):
			if "attachment" in item["links"]:
				fileKey = item["links"]["attachment"]["href"].split("/")[-1]
				with open(file, 'wb') as f:
					f.write(self.apiInstance.api_instance.file(fileKey))
			else:
				msg.showerror("Error", "There is no pdf file attached to the item")
				return

		self.filepath_entry.delete(0,tk.END)
		self.filepath_entry.insert(0,file)
		self.extractOCR()
		# self.loadText()
		self.loadViewer()

		self.saveProject()

	def loadText(self):
		with open(ROOT + self.project + PATH_SEP + "original.txt","r") as f:
			text = f.read()

		self.editor_left.insert("1.0",text)

		if os.path.exists(ROOT + self.project + PATH_SEP + "translation.txt"):
			with open(ROOT + self.project + PATH_SEP + "translation.txt","r") as f:
				text = f.read()

			self.editor_right.insert("1.0",text)
			if os.path.exists(ROOT + self.project + PATH_SEP + ".translation"):
				with open(ROOT + self.project + PATH_SEP + ".translation","rb") as f:
					tags = pickle.load(f)
					for tag in tags:
						if tag[1][:6] == "phrase":
							if tag[0] == "tagon":
								pos_beg = tag[2]			
							elif tag[0] == "tagoff":
								pos_end = tag[2]
								self.editor_right.tag_add(tag[1],pos_beg,pos_end)

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
			if not self.lang.get():
				msg.showerror("Error", "Please select a language")
				return
			self.extractOCR()
			self.zotItem = ZotItem(self.itemType.get())
			self.zotItem.template["collections"] = [self.zotero_api["destinations"]["Translations"]]
			resp = self.apiInstance.createItem(self.zotItem)
			if resp:
				self.zotItem.template["key"] = resp[0]
				self.zotItem.template["version"] = int(resp[1])
			else:
				print("something went wrong with Zotero")
		elif file_ext.lower() == "moul":
			with open(file, 'rb') as f:
				self.zotItem,self.project = pickle.load(f)
			self.loadText()
		else:
			msg.showerror("Error", "Wrong file extension")
			return

		# if self.doTranslate.get():
		# 	self.translateText()

		self.loadViewer()
		self.loadZotero()

	def loadZotero(self):
		'''Loads the fields corresponding to the current itemType in the Zotero panel on the left'''
		self.values_zotero = {}
		if self.zotItem.template["itemType"] != self.itemType.get():
			self.itemType.set(self.zotItem.template["itemType"])

		self.firstName.set(self.zotItem.template["creators"][0]["firstName"])
		self.lastName.set(self.zotItem.template["creators"][0]["lastName"])

		for i,(field,value) in enumerate(self.zotItem.template.items()):
			if field != "itemType" and field != "relations" and field != "collections" and field != "tags" and field != "key" and field != "version" and field != 'creators':
				ttk.Label(self.zotero_settings, text=field+': ').grid(column=0,row=i+3,padx=(2,2), pady=(2,2))
				self.values_zotero[field] = tk.StringVar()
				if value != "":
					self.values_zotero[field].set(value)
				ttk.Entry(self.zotero_settings, textvariable=self.values_zotero[field], font=self.default_font).grid(column=1,row=i+3, pady=(2,2), sticky="nsew", columnspan=2)
	
	def itemTypeUpdated(self,event=None):
		new_template = self.zotItem.getTemplate(self.itemType.get())
		for i,(field,value) in enumerate(self.values_zotero.items()):
			if field in self.zotItem.template:
				new_template[field] = value.get()

		if "key" in self.zotItem.template:
			new_template["key"] = self.zotItem.template["key"]
		if "version" in self.zotItem.template:
			new_template["version"] = self.zotItem.template["version"]

		new_template["collections"] = self.zotItem.template["collections"]

		new_template["creators"][0]["firstName"] = self.firstName.get()
		new_template["creators"][0]["lastName"] = self.lastName.get()

		self.zotItem.template = new_template

		for i,(k,v) in enumerate(self.zotero_settings.children.items()):
			if i >= 7:
				v.grid_forget()

		self.loadZotero()

	def loadViewer(self):
		'''Loads the "viewer" on the right panel. The image was concatenated just after the pdf split'''
		self.update()
		self.width = self.right_viewer_content.winfo_width()
		self.height = self.right_viewer_content.winfo_height()

		self.imgs = [Image.open(ROOT + self.project + PATH_SEP + "orig_images" + PATH_SEP + x) for x in sorted(os.listdir(ROOT + self.project + PATH_SEP + "orig_images")) if x != "original.jpg"]

		for i,img in enumerate(self.imgs):
			height_img,width_img=img.height,img.width
			scale = self.width/width_img
			new_height = scale*height_img
			self.imgs[i] = img.resize((self.width,(int(new_height))), Image.ANTIALIAS)

		self.ph_img = ImageTk.PhotoImage(self.imgs[0])
		self.img_index = 0

		self.viewer_settings = tk.Frame(self.right_viewer_content)
		self.viewer_settings.pack(side=tk.BOTTOM,expand=True,fill=tk.BOTH)

		self.image_window = ScrollableImage(self.right_viewer_content, project=self.project, image=self.ph_img, scrollbarwidth=6, width=self.width-140, height=self.height)
		self.image_window.pack(side="right", fill="both",expand=True)

		self.buttonRight = ttk.Button(self.viewer_settings, text=">",width=2, command=self.imageRight)
		self.buttonRight.pack(side="right")

		self.buttonLeft = ttk.Button(self.viewer_settings, text="<",width=2, command=self.imageLeft)
		self.buttonLeft.pack(side="right")

		if not path.exists(ROOT + self.project + PATH_SEP + "new_images"):
			mkdir(ROOT + self.project + PATH_SEP + "new_images")

		self.img_n = len(os.listdir(ROOT + self.project + PATH_SEP + "new_images"))

	def imageRight(self,event=None):
		if self.img_index < len(self.imgs)-1:
			self.img_index += 1
			self.ph_img = ImageTk.PhotoImage(self.imgs[self.img_index])
			self.image_window.pack_forget()
			self.image_window = ScrollableImage(self.right_viewer_content, project=self.project,image=self.ph_img, scrollbarwidth=6,width=self.width-140, height=self.height)
			self.image_window.pack(side="right", fill="both",expand=True)

		return "break"

	def imageLeft(self,event=None):
		if self.img_index > 0:
			self.img_index -= 1
			self.ph_img = ImageTk.PhotoImage(self.imgs[self.img_index])
			self.image_window.pack_forget()
			self.image_window = ScrollableImage(self.right_viewer_content, project=self.project,image=self.ph_img, scrollbarwidth=6, width=self.width-140, height=self.height)
			self.image_window.pack(side="right", fill="both",expand=True)

		return "break"

	def extractOCR(self):
		file = self.filepath_entry.get()
		if self.project == "":
			self.project = file.split(".")[0].split(PATH_SEP)[-1]

		proj_path = ROOT + self.project
		if not path.exists(proj_path):
			mkdir(proj_path)

		pages = split_pdf(file,self.project,int(self.firstpage.get()))
		lang = lang_map_tess[self.lang.get()]
		self.dict_abbr = common_abbr[self.lang.get().lower()]
		
		for img in pages:
			text = parse_img(img,lang,self.desalt.get())
			text = self.transf_text(text)
			self.editor_left.insert("insert",text)
			self.editor_left.update()

		with open(proj_path + PATH_SEP + "original.txt", "w") as f:
			text = self.editor_left.get('1.0',tk.END)
			f.write(text)

	def replLinebreaks(self,event=None):
		text = self.editor_left.get("1.0",tk.END)
		reg = re.compile(r"(?P<bef>(?<!figure\}))(?P<aft>\n(?![ ]*\\))")
		text = reg.sub(r'\g<bef>\\par\g<aft>',text)
		# text = text.replace("\n","\\par\n")
		self.editor_left.delete("1.0",tk.END)
		self.editor_left.insert("1.0",text)

	def transf_text(self,text):
		text = text.replace("-\n","")# words broken endline
		text = text.replace("\n\n","\\par\n")# paragraphs
		text = re.sub(r"(?<!\\par)\n"," ",text)# endline breaks

		text = re.sub('|'.join(self.dict_abbr.keys()),self.abbr_repl,text)
		text = text.replace("$","??")

		return text

	def abbr_repl(self,match):
		repl = self.dict_abbr[match.group()] if match.group() in self.dict_abbr else match.group()
		return repl

	def buildPhrasesFromEditor(self,event=None):
		'''Builds the phrase dictionary from the left panel editor
		'''
		if self.editor_right.get("1.0",tk.END).strip():
			msgbox = msg.askokcancel("Warning", "This may break the link with translation")
			if not msgbox:
				return

		text = self.editor_left.get("1.0",tk.END)
		for tag in self.editor_left.tag_names():
			self.editor_left.tag_delete(tag)

		self.editor_left.tag_configure("color_phrase_1", background="#cecece")
		self.editor_left.tag_lower("color_phrase_1")
		self.editor_left.tag_configure("color_phrase_2", background="#bcbcbc")
		self.editor_left.tag_lower("color_phrase_2")

		self.regex = re.compile('|'.join([
			r'(?:(?P<bef_fig>[^\$\.\?\!\;\:]*?)(?P<fig>\\begin\{[a-z]*?\}.*?\\end\{[a-z]*?\}))',
			r'(?:(?P<bef_par>[^\$\.\?\!\;\:]*?)\\(?P<par>par))',
			r'(?:(?P<bef_cmd>[^\$\.\?\!\;\:]*?)\\(?P<cmd>[a-z]+?)\{(?P<cmd_text>.+?)\})',# Footnotes in particular
			r'(?P<text>.+?(?<!\d)(?<!\(\w)(?<! [A-Za-z])(?<!\S\.\S)[\.\?\!\;\:](?!\.+)(?!\))(?!\d))']),# Beware one of the lookbehind excludes phrases in parenthesis 
		flags=re.S)

		phrases = self.regex.finditer(text)
		for i,match in enumerate(phrases):
			# print(format(i) + ": " + match.group())
			beg,end = match.span()
			idx = '1.0 + %dc' % (beg)
			lastidx = '1.0 + %dc' % (end)
			self.editor_left.tag_add("color_phrase_"+format(i%2+1),idx,lastidx)  
			self.editor_left.tag_add("phrase_"+format(i),idx,lastidx)

		# print(self.editor_left.dump('1.0', tk.END, ))#**{"tags":True,'text':True}

	def translateText(self):
		'''Based on the regex above and the named groups detected
		'''
		if os.path.exists(ROOT + self.project + PATH_SEP + ".dict_phrases"):
			with open(ROOT + self.project + PATH_SEP + ".dict_phrases","rb") as f:
				dict_phrases = pickle.load(f)
				check = True
		else:
			dict_phrases = {}
			check = False

		text = self.editor_left.get("1.0",tk.END)
		# text = text.replace("\n","s")
		translate_client = translate.Client()# Or use direct credentials in translation_api.json
		# from google.oauth2 import service_account
		# credentials = service_account.Credentials.from_service_account_file('/home/carter/Desktop/Cours/Th??se/Programming_economics/translation_project/translation_api.json')

		phrases = self.regex.finditer(text)

		for i,ph in enumerate(phrases):
			if check and ph.group(0) != dict_phrases["phrase_"+format(i)]:
				self.editor_right.mark_set("insert","phrase_"+format(i)+".first")
				self.editor_right.delete("phrase_"+format(i)+".first","phrase_"+format(i)+".last")
			elif check:
				continue
			
			dict_phrases["phrase_"+format(i)] = ph.group(0)
			pos_beg = self.editor_right.index("insert")

			# Check which group has been matched
			if ph.groupdict()["text"]:
				cur_ph = ph.groupdict()["text"]
				trans_ph = translate_text(cur_ph,translate_client,src=lang_map_google[self.lang.get()],target="en")
				self.editor_right.insert("insert", " " + trans_ph)
			elif ph.groupdict()["fig"]:
				self.editor_right.insert(pos_beg,"\n")
				self.editor_right.insert(pos_beg,ph.groupdict()["fig"])
				self.editor_right.insert(pos_beg,"\n")
				if ph.groupdict()["bef_fig"].strip():
					cur_ph = ph.groupdict()["bef_fig"]
					trans_ph = translate_text(cur_ph,translate_client,src=lang_map_google[self.lang.get()],target="en")
					self.editor_right.insert(pos_beg," " + trans_ph)
			elif ph.groupdict()["cmd"]:
				self.editor_right.insert(pos_beg,"}")
				cur_ph = ph.groupdict()["cmd_text"]
				trans_ph = translate_text(cur_ph,translate_client,src=lang_map_google[self.lang.get()],target="en")
				self.editor_right.insert(pos_beg,trans_ph)
				fnspace = "" if ph.groupdict()["cmd"] == "footnote" else " "
				self.editor_right.insert(pos_beg,fnspace+"\\"+ph.groupdict()["cmd"]+"{")
				if ph.groupdict()["bef_cmd"].strip():
					cur_ph = ph.groupdict()["bef_cmd"]
					trans_ph = translate_text(cur_ph,translate_client,src=lang_map_google[self.lang.get()],target="en")
					self.editor_right.insert(pos_beg," " + trans_ph)
			elif ph.groupdict()["par"]:
				self.editor_right.insert(pos_beg,"\\par \n")
				if ph.groupdict()["bef_par"].strip():
					cur_ph = ph.groupdict()["bef_par"]
					trans_ph = translate_text(cur_ph,translate_client,src=lang_map_google[self.lang.get()],target="en")
					self.editor_right.insert(pos_beg, " " + trans_ph)

			pos_end = self.editor_right.index("insert")
			self.editor_right.tag_add("phrase_"+format(i),pos_beg,pos_end)	
			self.editor_right.update()
			self.editor_left.update()

		with open(ROOT + self.project + PATH_SEP + ".dict_phrases","wb") as f:
			pickle.dump(dict_phrases,f)

		self.saveProject()

	def dontTranslate(self,event=None):
		'''Flags the phrase where the cursor currently is to not be translated. 
		TODO: update the tag after insertion
		TODO: merge with other insert operations'''
		cur_phrase = self.editor_left.tag_names("insert")[1]
		self.editor_left.insert(cur_phrase+".last","\dont{")
		self.editor_left.insert(cur_phrase+".last"+"-1c","}")

	def insertFn(self,event=None):
		cur_phrase = self.editor_left.tag_names("insert")[1]
		self.editor_left.insert(cur_phrase+".first","\\footnote{")
		self.editor_left.insert(cur_phrase+".last"+"-1c","}")

	def insertImage(self,event=None):
		img = Image.open(ROOT + self.project + PATH_SEP + "new_images/tmp.jpg")
		ph_img = ImageTk.PhotoImage(img)

		# self.editor_left.image_create("insert",image=ph_img,padx=2,pady=2,align="center")
		img_name = "image_" + format(self.img_n) + ".jpg"
		new_img_latex = img_latex % (ROOT + self.project + PATH_SEP + "new_images/image_" + format(self.img_n) + ".jpg", "")
		self.editor_left.insert("insert",new_img_latex)
		img.save(ROOT + self.project + PATH_SEP + "new_images"+ PATH_SEP + img_name)
		self.img_n += 1

		return "break"

	def makePDF(self):
		translator = "Vincent Carret"
		translation_date = datetime.today().strftime("%B %d, %Y")

		title = self.zotItem.template["title"]
		author = self.zotItem.template["creators"][0]["firstName"] + " " + self.zotItem.template["creators"][0]["lastName"]
		date = self.zotItem.template["date"]
		abstract = self.zotItem.template["abstractNote"]
		if abstract.strip():
			abstract = abs_template % abstract
		content = self.editor_right.get("1.0",tk.END)
		content = content.replace("%","\\%")
		content = content.replace("\\caption*{}","")
		content = content.replace("&","\&")
		content = content.replace("???","-")

		with open("tex_template.tex", "r") as f:
			template = f.read()

		template = template % (title,author,translator,translation_date,date,abstract,content,)
		with open(ROOT + self.project + PATH_SEP + "Translation of " + self.project + ".tex","w") as f:
			f.write(template)

		subprocess.run(["pdflatex","-output-directory", ROOT+self.project, ROOT+self.project+PATH_SEP+"Translation of " + self.project +".tex"])

	def uploadPDF(self):
		resp = self.apiInstance.api_instance.attachment_simple([ROOT+self.project+PATH_SEP+ "Translation of " + self.project + ".pdf"],self.zotItem.template["key"])
		if resp["failure"] != []:
			print("Failure to upload file")

	def findPages(self,event=None):
		s = int(self.findFirstPageBox.get())
		nchars = tk.IntVar()
		if s:
			idx = "1.0"
			for i in range(len(self.imgs)):
				if not idx:
					idx = '1.0'
				s_newl = "\n"+format(s)
				idx = self.editor_left.search(s_newl,idx,stopindex=tk.END,count=nchars) 
				if not idx:
					s += 1
					continue

				self.editor_left.insert(idx+'+1c','[')
				self.editor_left.insert(idx+'+%dc' % (nchars.get()+1),']')
				s += 1

	def find(self,event=None):
		self.editor_left.tag_remove('found','1.0',tk.END)
		s = self.findBox.get()
		nchars = tk.IntVar()
		first = True
		if s:
			idx = "1.0"
			while True:
				idx = self.editor_left.search(s,idx,stopindex=tk.END,nocase=self.nocase.get(),regexp=self.regexp.get(),exact=self.exact.get(),count=nchars) 
				if not idx: 
					break

				if first and self.editor_left.compare(idx, '>','insert'):
					self.editor_left.see(idx)
					first = False

				lastidx = '% s+% dc' % (idx, nchars.get()) 
				self.editor_left.tag_add('found', idx, lastidx)  
				idx = lastidx  

			self.editor_left.tag_config('found', foreground ='red') 
		self.editor_left.update()
		self.findBox.focus_set() 

	def replace(self,event=None):
		self.editor_left.tag_remove('found','1.0',tk.END)
		s = self.findBox.get()
		r = self.replaceBox.get()
		nchars = tk.IntVar()
		if s:
			idx = "1.0"
			while True:
				idx = self.editor_left.search(s,idx,stopindex=tk.END,nocase=self.nocase.get(),regexp=self.regexp.get(),exact=self.exact.get(),count=nchars) 

				if not idx or self.editor_left.compare(idx, '>', self.editor_left.index(tk.END)):
					break

				lastidx = '%s + %dc' % (idx, nchars.get()) 
				self.editor_left.delete(idx, lastidx)  
				self.editor_left.insert(idx, r)

				lastidx = '%s + %dc' % (idx, len(r)) 
				self.editor_left.tag_add('found', idx, lastidx)  
				idx = lastidx  

			self.editor_left.tag_config('found', foreground ='green',background='yellow') 
		self.findBox.focus_set() 

	def selectAll(self,event):
		self.editor_left.tag_add("sel","1.0",tk.END)
		return "break"
		# self.editor_left.icursor(tk.END)

	def insertPar(self,event=None):
		self.editor_left.insert("insert","\\par")
		if event.keycode == 104:
			self.editor_left.insert("insert","\n")
		if self.editor_left.tag_ranges(tk.SEL):
			self.editor_left.delete("sel.first","sel.last")

	def insertGen(self,word):
		if self.editor_left.tag_ranges(tk.SEL):
			self.editor_left.insert("sel.first","\\%s{" % word)
			self.editor_left.insert("sel.last","}")
		else:
			self.editor_left.insert("insert","\\%s{}" % word)
			self.editor_left.mark_set("insert","insert"+"-%dc" % 1)

	def insertFootnote(self,event=None):
		self.insertGen("footnote")

	def insertItalics(self,event=None):
		self.insertGen("textit")

	def insertUnderline(self,event=None):
		self.insertGen("underline")

	def insertBold(self,event=None):
		self.insertGen("textbf")
	
	def insertCenterline(self,event=None):
		self.insertGen("centerline")

	def deleteWord(self,event=None):
		self.editor_left.delete("insert -1c wordstart", "insert")
		return 'break'

	# Rewrite this correctly
	def insertGenRight(self,word):
		if self.editor_right.tag_ranges(tk.SEL):
			self.editor_right.insert("sel.first","\\%s{" % word)
			self.editor_right.insert("sel.last","}")
		else:
			self.editor_right.insert("insert","\\%s{}" % word)
			self.editor_right.mark_set("insert","insert"+"-%dc" % 1)

	def insertItalicsRight(self,event=None):
		self.insertGenRight("textit")

	def insertEquation(self,event=None):
		if event.state == 24:
			first = "$"
			last = "$"
		elif event.state == 25:
			first = "\\begin{equation}\n"
			last = "\n\\end{equation}"
		else:
			print(event)
			return
		if self.editor_left.tag_ranges(tk.SEL):
			self.editor_left.insert("sel.first","%s" % first)
			self.editor_left.insert("sel.last","%s" % last)
		else:
			self.editor_left.insert("insert","%s" % first + last)
			self.editor_left.mark_set("insert","insert"+"-%dc" % len(last))

	def insertSimplePar(self,event=None):
		self.editor_left.insert("insert","\\par")

	def insertSimpleNewl(self,event=None):
		self.editor_left.insert("insert","\n")

	def setFocusFinder(self,event):
		if self.editor_left.tag_ranges(tk.SEL):
			self.findBox.delete(0,'end')
			self.findBox.insert(0,self.editor_left.get("sel.first","sel.last"))
		self.findBox.focus_set()
		return "break"

	def setFocusReplace(self,event):
		if self.editor_left.tag_ranges(tk.SEL):
			self.replaceBox.delete(0,'end')
			self.replaceBox.insert(0,self.editor_left.get("sel.first","sel.last"))
		self.replaceBox.focus_set()

	def browseFiles(self):
		filename = filedialog.askopenfilename(initialdir=ROOT)

		if filename:
			self.filepath_entry.delete(0, 'end')
			self.filepath_entry.insert(0, filename)

	def browseZotero(self):
		if not self.lang.get():
			msg.showerror("Error", "Please select a language")
			return

		if not os.path.exists(ROOT + ".zotero_coll"):
			self.updateZotero()

		with open(ROOT + ".zotero_coll","rb") as f:
			collection = pickle.load(f)

		itemKey = ZoteroDialog(self.content,collection).show()
		if itemKey:
			self.loadZoteroItem(itemKey)

	def updateZotero(self):
		collection = self.apiInstance.api_instance.collection_items(self.zotero_api["destinations"]["Translations"],sort="creator", limit=100)#,sort="creator",direction="desc",limit=50)

		with open(ROOT + ".zotero_coll","wb") as f:
			pickle.dump(collection, f)

	def _on_change(self, event):
		self.linenumbers.redraw()

class ScrollableImage(tk.Frame):
	'''Scrollable image. See: https://stackoverflow.com/a/56046307'''
	def __init__(self, master=None, **kw):
		self.project = kw.pop('project', None)
		self.path = ROOT + self.project + PATH_SEP
		self.image = kw.pop('image', None)
		sw = kw.pop('scrollbarwidth', 10)
		super(ScrollableImage, self).__init__(master=master, **kw)
		self.cnvs = tk.Canvas(self, highlightthickness=0, **kw)
		self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
		# Vertical and Horizontal scrollbars
		self.v_scroll = tk.Scrollbar(self, orient='vertical', width=sw)
		self.h_scroll = tk.Scrollbar(self, orient='horizontal', width=sw)
		# Grid and configure weight.
		self.cnvs.grid(row=0, column=0,  sticky='nsew')
		self.h_scroll.grid(row=1, column=0, sticky='ew')
		self.v_scroll.grid(row=0, column=1, sticky='ns')
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		# Set the scrollbars to the canvas
		self.cnvs.config(xscrollcommand=self.h_scroll.set, 
						   yscrollcommand=self.v_scroll.set)
		# Set canvas view to the scrollbars
		self.v_scroll.config(command=self.cnvs.yview)
		self.h_scroll.config(command=self.cnvs.xview)
		# Assign the region to be scrolled 
		self.cnvs.config(scrollregion=self.cnvs.bbox('all'))
		self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouse_scroll)
		self.cnvs.bind_class(self.cnvs, "<Button-4>", self.mouse_scroll)
		self.cnvs.bind_class(self.cnvs, "<Button-5>", self.mouse_scroll)

		self.cnvs.bind("<Button-1>", self.saveCoord)
		self.cnvs.bind("<ButtonRelease-1>", self.saveImg)

	def saveCoord(self,event=None):
		self.x,self.y = self.winfo_pointerxy()

	def saveImg(self,event):
		endx,endy = self.winfo_pointerxy()
		position = (self.x,self.y,endx,endy)
		image = ImageGrab.grab(position)
		image.save(self.path + "new_images" + PATH_SEP + "tmp.jpg")

	def mouse_scroll(self, evt):
		x, y = self.winfo_pointerxy()
		# print(str(self.winfo_containing(x,y)))
		if "scrollableimage" in str(self.winfo_containing(x,y)):
			if evt.delta:
				self.cnvs.yview_scroll(int(-1*(evt.delta/120)), "units")
			else:
				if evt.num == 5:
					move = 1
				else:
					move = -1
				self.cnvs.yview_scroll(move, "units")

# See https://stackoverflow.com/a/16375233
class TextLineNumbers(tk.Canvas):
	def __init__(self, *args, **kwargs):
		tk.Canvas.__init__(self, *args, **kwargs)
		self.textwidget = None

	def attach(self, text_widget):
		self.textwidget = text_widget
		
	def redraw(self, *args):
		'''redraw line numbers'''
		self.delete("all")

		i = self.textwidget.index("@0,0")
		while True :
			dline= self.textwidget.dlineinfo(i)
			if dline is None: break
			y = dline[1]
			linenum = str(float(i)+47).split(".")[0]
			self.create_text(2,y,anchor="nw", text=linenum)
			i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
	def __init__(self, *args, **kwargs):
		tk.Text.__init__(self, *args, **kwargs)

		# create a proxy for the underlying widget
		self._orig = self._w + "_orig"
		self.tk.call("rename", self._w, self._orig)
		self.tk.createcommand(self._w, self._proxy)

	def _proxy(self, *args):
		# let the actual widget perform the requested action
		cmd = (self._orig,) + args
		result = self.tk.call(cmd)

		# generate an event if something was added or deleted,
		# or the cursor position changed
		if (args[0] in ("insert", "replace", "delete") or 
			args[0:3] == ("mark", "set", "insert") or
			args[0:2] == ("xview", "moveto") or
			args[0:2] == ("xview", "scroll") or
			args[0:2] == ("yview", "moveto") or
			args[0:2] == ("yview", "scroll")
		):
			self.event_generate("<<Change>>", when="tail")

		# return what the actual widget returned
		return result      


if __name__ == "__main__":
	moulinette = Moulinette()
	moulinette.mainloop()