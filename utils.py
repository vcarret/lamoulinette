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

import six
from google.cloud import translate_v2 as translate


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


def extractOCR(file, root, project, doOCR):
	pdf = pdfplumber.open(file)# Returns a PDF object

	if project == "":
		project = file.split(".")[0].split(PATH_SEP)[-1]

	proj_path = root + project
	if not path.exists(proj_path):
		mkdir(proj_path)

	destination = proj_path + PATH_SEP + "original.txt"

	if doOCR:
		pages = split_pdf(file)
		service = auth_drive()
		for i,page in enumerate(pages):
			file_up = upload_doc(service,page)
			download_doc(service,file_up,destination)
	else:# Just try to extract the text
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

def split_pdf(file):
	out = "orig_images"
	if not path.exists(out):
		mkdir(out)
	
	pages = convert_from_path(file, dpi=300,output_file="",output_folder=out,first_page=2,fmt='jpeg',paths_only=True)
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
	def __init__(self,phrase,ind=None,prev=None,foll=None,page=None):
		self.phrase = phrase
		self.translation = ""
		self.index = ind
		self.prev = prev
		self.foll = foll
		self.page = page
		self.footnote = []
		self.changed = True

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

    translate_client = translate.Client()# Or use direct credentials in translation_api.json
    # from google.oauth2 import service_account
	# credentials = service_account.Credentials.from_service_account_file('/home/carter/Desktop/Cours/Thèse/Programming_economics/translation_project/translation_api.json')

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text,source_language=source,target_language=target)

    return result["translatedText"]