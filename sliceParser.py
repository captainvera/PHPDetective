
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
#test = Slice()
#test.getItems()
##################

def fileParser():
	#Important vars
	varsList = []
	entryPoints = []
	validation = []
	sensitiveSynks = []


	#Insert FileName
	fileName = "sqli_01.txt" #input("Enter file name: ")
	print("File Name : %s" % fileName)

	#Open fileName
	fo = open(fileName, "r")
	print("Is File Closed ? %s" % fo.closed)

	#Read its content to a list
	content = fo.readlines()

	#FUNTION to create a list of Variables in the SLICE
	getVarList(content,varsList, entryPoints)
	#FUNCTION to create a list of ENTRYPOINTS in the SLICE
	getEntryPoints(content, varsList, entryPoints)
	#FUNCTION to create a list of VALIDATIONS in the SLICE
	#getValidations()
	#FUNCTION to create a list of SENSITIVESYNKS in the SLICE
	#getSynks()

	#Just an AKNOWLEDGE:  VARSLIST[i] has a ENTRYPOINT[i]
	for l in range(len(varsList)):
		print("Var : %s ----> EP : %s" % (varsList[l], entryPoints[l]))


#AUX FUNTIONS
def getVarList(content, varsList, entryPoints):
	#Get VarsList
	expr = re.compile('\$([a-zA-Z]\w*)(?=\s*=)')
	for i in range(len(content)):
		if(expr.match(content[i]) is not None):
			varsList.append(expr.match(content[i]).group())

	#Initialize entryPoints[] to empty string
	for i in range(len(varsList)):
		entryPoints.append('')

def getEntryPoints(content, varsList, entryPoints):
	#Get ENTRYPOINTS for each VARIABLE : VAR[i] associates ENTRYPOINT[i]
	for ep in range(len(EP)):
		for line in range(len(content)):
			#This is important to put the EntryPOint in the correct INDEX
			if(EP[ep] in content[line] and varsList[line] in content[line]):
				entryPoints[line] = EP[ep]



##################
fileParser()
##################
