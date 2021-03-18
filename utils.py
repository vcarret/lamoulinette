import pdfplumber
import re
from datetime import datetime
from pdf2image import convert_from_path
from os import path, mkdir
import pickle
import io
import platform
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
from PIL import ImageTk, Image, ImageGrab
import requests
from pyzotero import zotero
import html
import six
from google.cloud import translate_v2 as translate
import requests
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import Scrollbar
import tkinter.font as tkFont
import subprocess
import json

if platform.system() == "Windows":
	PATH_SEP = "\\"
else:
	PATH_SEP = "/"

ROOT = '/home/carter/Documents/Moulinette/'

lang_map = {
	'': '',
	'Dutch': 'nl',
	'German': 'de',
	'Italian': 'it'
}

# See https://stackoverflow.com/questions/122348/scale-image-down-but-not-up-in-latex for the scaling of images
img_latex = '''\\begin{figure}[H]
    \\centering
    \\scalegraphics{%s}
    \\caption*{%s}
\\end{figure}'''

abs_template = '''\\begin{abstract}
%s
\\end{abstract}'''



def extractOCR(file, root, project, doOCR, firstpage=1):
	pdf = pdfplumber.open(file)# Returns a PDF object

	if project == "":
		project = file.split(".")[0].split(PATH_SEP)[-1]

	proj_path = root + project
	if not path.exists(proj_path):
		mkdir(proj_path)

	destination = proj_path + PATH_SEP + "original.txt"

	if doOCR:
		pages = split_pdf(file,project,firstpage)
		service = auth_drive()
		for i,page in enumerate(pages):
			file_up = upload_doc(service,page)
			download_doc(service,file_up,destination)
	else:# Just try to extract the text
		pages = split_pdf(file,project,firstpage)
		txt_file = open(destination, "w") 
		for n, page in enumerate(pdf.pages):
			text = page.extract_text()
			txt_file.write(text)
		txt_file.close()

	return project

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def auth_drive():
	"""Authenticate in the Drive and returns a usable service object
	"""
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('drive', 'v3', credentials=creds)
	return service

def split_pdf(file,project,firstpage=1):
	out = ROOT + project + PATH_SEP + "orig_images"
	if not path.exists(out):
		mkdir(out)
	
	pages = convert_from_path(file, dpi=300,output_file="",output_folder=out,first_page=firstpage,fmt='jpeg',paths_only=True)

	# images = [Image.open(out + PATH_SEP + x) for x in sorted(os.listdir(out)) if x != "original.jpg"]
	# widths, heights = zip(*(i.size for i in images))
	# total_height = sum(heights)
	# max_widths = max(widths)
	
	# new_im = Image.new('RGB', (max_widths, total_height))
	# y_offset = 0
	# for im in images:
	# 	new_im.paste(im, (0,y_offset))
	# 	y_offset += im.size[1]

	# new_im.save(out+PATH_SEP+'original.jpg')

	return pages

def upload_doc(service,file):
	name = file.split("/")[1]
	file_metadata = {
		'name': name,
		'mimeType': 'application/vnd.google-apps.file',
		'parents': ['1my_JqnNBNak5-aIlt5TZ92IHOazWUU2G']
	}
	media = MediaFileUpload(file,
							mimetype='image/jpeg',
							resumable=True)

	file_up = service.files().create(body=file_metadata,
								  media_body=media,
								  fields='id').execute()
	return(file_up)

def download_doc(service,file_up,destination):	
	out = "down_text"
	if not path.exists(out):
		mkdir(out)
	request = service.files().export_media(fileId=file_up['id'],mimeType='text/plain')

	fh = io.FileIO(destination,"ab")
	downloader = MediaIoBaseDownload(fh, request)
	done = False
	while done is False:
		status, done = downloader.next_chunk()
		print("Download %d%%." % int(status.progress() * 100))

	service.files().delete(fileId=file_up['id']).execute()

class Phrase():
	def __init__(self,phrase,index=None,prev=None,foll=None,page=None):
		self.phrase = phrase
		self.translation = ""
		self.index = index
		self.prev = prev
		self.foll = foll
		self.page = page
		self.footnote = []
		self.changed = True
		self.translate = True

class Footnote(Phrase):
	def __init__(self):
		self.pos = None


def translate_text(text,source="",target="en"):
	"""Translates text into the target language.

	Target must be an ISO 639-1 language code.
	See https://g.co/cloud/translate/v2/translate-reference#supported_languages
	"""
	if text == "":
		return ""

	clean_text = text.replace("\n"," ")
	clean_text = re.sub("\$(?P<math>.+?)\$","<span translate='no'>\g<math></span>",clean_text)

	translate_client = translate.Client()# Or use direct credentials in translation_api.json
	# from google.oauth2 import service_account
	# credentials = service_account.Credentials.from_service_account_file('/home/carter/Desktop/Cours/Thèse/Programming_economics/translation_project/translation_api.json')

	if isinstance(clean_text, six.binary_type):
		clean_text = clean_text.decode("utf-8")

	# Text can also be a sequence of strings, in which case this method
	# will return a sequence of results for each text.
	result = translate_client.translate(clean_text,source_language=source,target_language=target)
	result = re.sub("<span translate='no'>(?P<math>.+?)</span>","\$\g<math>\$",result["translatedText"])

	return html.unescape(result)

def check_num(newval):
	return re.match('^[0-9]*$', newval) is not None and len(newval) <= 5

class ZotItem():
	all_template = {}
	def __init__(self, itemType):
		self.template = self.getTemplate(itemType)
		self.attachment = ''

	def getTemplate(self, itemType):
		if itemType not in self.all_template:
			url = "https://api.zotero.org/items/new?itemType={i}".format(i=itemType)
			default_headers = {
				"User-Agent": "Moulinette",
				"Zotero-API-Version": "3"
			}
			request = requests.get(url=url, headers=default_headers)
			request.encoding = "utf-8"
			self.all_template[itemType] = request.json()
		return self.all_template[itemType].copy()

	def update(self, field, value):
		if field != "creators" and field != "author" and field != "attachment" and field != "collections" and field != "tags" and field in self.template:
			self.template[field] = value.strip()
		elif field == "tags":
			self.template[field] = value.strip().split(",")
		elif field == "collections":
			self.template[field] = [value[0].strip()]
		elif field == "creators" or field == "author":
			self.template["creators"] = value
		# 	author = value.strip().split(" ")[-1]
		# 	self.template["creators"]
		# 	self.template["creators"][0]["lastName"] = 
		# 	try:
		# 		self.template["creators"][0]["firstName"] = " ".join(value.strip().split(" ")[:-1])
		# 	except IndexError:
		# 		pass
		elif field == "attachment":
			self.attachment = value.strip()

	def access(self, key):
		if key in self.template:
			if key == "creators":
				try:
					return(self.template[key][0]['firstName'] + " " + self.template[key][0]['lastName'])
				except (IndexError):
					return('')
			elif key == "collections":
				return(self.template[key][0])
			else:
				return(self.template[key])
		else:
			return('')

class ApiCall():
	def __init__(self, api_key = None, lib_type = None, lib_id = None):
		self.api_instance = zotero.Zotero(int(lib_id), lib_type, api_key)

	def createItem(self, item):
		resp = self.api_instance.create_items([item.template])
		if resp['successful'] != {}:
			return (resp['successful']['0']['key'],resp['successful']['0']['version'],)# The id of the item created
		else:
			return False

	def updateItem(self,item):
		resp = self.api_instance.update_item(item.template)
		return resp

	def uploadFile(self,item,attachment):
		up = self.api_instance.attachment_simple([item.attachment], item.template["key"])
		if up['failure'] != []:
			print("Failure to upload file")


class ZoteroDialog(tk.Toplevel):
	def __init__(self, parent,collection):
		tk.Toplevel.__init__(self, parent)
		self.geometry("%dx%d" % (1000, 1000))

		self.canvas = tk.Canvas(self)

		self.canvas = tk.Canvas(self, borderwidth=0)
		self.frame = tk.Frame(self.canvas)
		self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.vsb.set)

		self.vsb.pack(side="right", fill="y")
		self.canvas.pack(side="right", fill="both", expand=True)
		self.canvas.create_window((4,4), window=self.frame, anchor="nw",tags="self.frame")

		self.frame.bind("<Configure>", self.onFrameConfigure)
		self.frame.bind("<MouseWheel>", self.mouse_scroll)
		self.frame.bind_all("<Button-4>", self.mouse_scroll)
		self.frame.bind_all("<Button-5>", self.mouse_scroll)

		self.var = tk.StringVar()
		self.populate(collection)

	def populate(self, collection):
		i = 0
		for item in collection:
			data = format(i) + ": "
			if "meta" in item:
				if "creatorSummary" in item["meta"]:
					data += item["meta"]["creatorSummary"] 
				else:
					continue
				if "parsedDate" in item["meta"]:
					data += " - " + item["meta"]["parsedDate"]
			if "data" in item:
				if "title" in item["data"]:
					data += " - " + item["data"]["title"]
			label = ttk.Label(self.frame,text=data)
			label.grid(column=1, row=i, sticky='nsew')
			label.bind("<Button-1>",lambda e,data=item['key']:self.return_key(data))
			i += 1

	def return_key(self, event=None):
		self.var.set(event)
		self.destroy()

	def show(self):
		self.wm_deiconify()
		self.wait_window()
		return self.var.get()

	def onFrameConfigure(self,event=None):
		'''Reset the scroll region to encompass the inner frame'''
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def mouse_scroll(self, event):
		x, y = self.winfo_pointerxy()
		print(self.winfo_pointerxy())
		if "canvas" in str(self.winfo_containing(x,y)):
			if event.delta:
				self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
			else:
				if event.num == 5:
					move = 1
				else:
					move = -1
				self.canvas.yview_scroll(move, "units")


item_types = [
	"document",
	"book",
	"bookSection",
	"journalArticle",
	"magazineArticle",
	"newspaperArticle",
	"letter",
	"note",
	"thesis",
	"manuscript",
	"interview",
	"film",
	"artwork",
	"webpage",
	"attachment",
	"report",
	"bill",
	"case",
	"hearing",
	"patent",
	"statute",
	"email",
	"map",
	"blogPost",
	"instantMessage",
	"forumPost",
	"audioRecording",
	"presentation",
	"videoRecording",
	"tvBroadcast",
	"radioBroadcast",
	"podcast",
	"computerProgram",
	"conferencePaper",
	"encyclopediaArticle",
	"dictionaryEntry"
]

item_fields = [
	"itemType",
	"title",
	"abstractNote",
	"series",
	"seriesNumber",
	"volume",
	"numberOfVolumes",
	"edition",
	"place",
	"publisher",
	"date",
	"numPages",
	"language",
	"url",
	"archive",
	"archiveLocation",
	"libraryCatalog",
	"extra",
	"creators",
	"attachment",
	"tag",
	"note",
	"bookSection",
	"issue"
]


common_abbr = {
	'dutch': {
		'a.h.w.': 'als het ware',
		'bijv.': 'bijvoorbeeld',
		'blz.': 'bladzijde',
		'b.v.': 'bijvoorbeeld',
		'd.w.z.': 'dat wil zeggen',
		'Dr.': 'Dokter',
		'e.a.': 'en andere',
		'id.': 'idem',
		'i.e.': 'dat wil zeggen',
		'm.a.w.': 'met andere woorden',
		'm.i.': 'mijn mening',
		't.a.v.': 'ten aanzien van',
		't.o.v.': 'ten opzichte van',
		'Vgl.': 'Vergelijk',
		'vgl.': 'vergelijk',
		'w.o.': 'waaronder',
	},
	'german': {
		'bzw.': 'beziehungsweise',
		'Abb.': 'Abbildung',
		'abb.': 'abbildung',
		'd.h.': 'das heißt',
		'd. h.': 'das heißt',
		'z. B.': 'zum Beispiel',
		'z.B.': 'zum Beispiel',
		'a. a. o.': 'am angegebenen Orte',
		# ' s.': 'seite',
		# 'Vjh.': 'Vierteljahrshefte'
	}
}