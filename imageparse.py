import os, sys, re
import urllib
import string

IMAGES_DIR = "images"

def parse(file):
	baseName = os.path.basename(file)
	newStr = ""
	with open(file, 'r') as f:
		str = f.read()

		match = re.search("\!\[.*\]\((.*)\)", str)
		lastMatch = match
		
		while match:
			imgURL = match.group(1)
			imgName = os.path.basename(imgURL)
			newURL = os.path.join(IMAGES_DIR, imgName)
			
			if os.path.exists(newURL):
				print "image already exists: %s" % (match.group(0))
			else:
				urllib.urlretrieve(imgURL, newURL)

			newStr += str[:match.start(1)]
			newStr += newURL
			str = str[match.end(1):]
			lastMatch = match
			match = re.search("\!\[.*\]\((.*)\)", str)

		if lastMatch:
			newStr += str

	#if we found some matches
	if newStr:
		with open(file, 'w') as f:
			f.write(newStr)

path = "."
files = [p for p in os.listdir(path) if p.lower().endswith('.md')]

for f in files:
	print f
	parse(f)
	print 