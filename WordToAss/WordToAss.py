import sys
import os
import docx


dirname = "E:\\coding\\MyTools\\test\\测试\\"
#dirname = sys.argv[1]

flist = os.listdir(dirname)
for efile in flist:
	extname = os.path.splitext(efile)[1]
	if extname == ".doc" or extname == ".docx":
		print(efile)
		docfile = docx.Document(dirname+efile)
		for paragraph in docfile.paragraphs:
			print(paragraph.text)

	if extname == ".mp4":
		print(efile)