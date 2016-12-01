
import re

EP = ['$_POST','$_GET','$_COOKIE','$_REQUEST', 'HTTP_GET_VARS', 'HTTP_POST_VARS', 'HTTP_COOKIE_VARS', 'HTTP_REQUEST_VARS','$_FILES','$_SERVERS']

class Slice:
	name = ''
	entryPoints = []
	validations = []
	sensitiveSynks = []

	def __init__(self):
		self.name = 'test'
		self.entryPoints.append('EntryTest')
		self.validations.append('ValidationTest')
		self.sensitiveSynks.append('SynkTest')

	def getItems(self):
		print("Name : " + self.name)
		print("EntryPoints: ")
		for x in range(len(self.entryPoints)):
			print("Entry %d: %s" % (x,self.entryPoints[x]))
		print("SensitiveSynks: ")
		for x in range(len(self.sensitiveSynks)):
			print("Synk %d: %s" % (x,self.sensitiveSynks[x]))

##################
test = Slice()
test.getItems()
##################

def fileParser():
	#Insert FileName
	fileName = "sqli_01.txt" #input("Enter file name: ")
	print("File Name : %s" % fileName)

	#Open fileName
	fo = open(fileName, "r")
	print("Is File Closed ? %s" % fo.closed)

	#Read its content to a list
	content = fo.readlines()
	getEntryPoints(content)

#AUX FUNTIONS
def getEntryPoints(content):
	varsList = []
	entryPoints = []

	#Get Vars
	expr = re.compile('\$([a-zA-Z]\w*)(?=\s*=)')
	for i in range(len(content)):
		if(expr.match(content[i]) is not None):
			varsList.append(expr.match(content[i]).group())
	for i in range(len(varsList)):
		entryPoints.append('')

	#Get ENTRYPOINTS for each VARIABLE : VAR[i] associates ENTRYPOINT[i]
	for ep in range(len(EP)):
		for line in range(len(content)):
			if(EP[ep] in content[line] and varsList[line] in content[line]):
				entryPoints[line] = EP[ep]

	#Acknowledge that for each var in slice there is an EntryPOint Y associated with
	for l in range(len(varsList)):
		print("Var : %s ----> EP : %s" % (varsList[l], entryPoints[l]))

	return 0



##################
fileParser()
##################
