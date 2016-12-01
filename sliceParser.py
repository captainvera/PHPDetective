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
	print(len(content))
	for i in range(len(content)):
		print(content[i])

#AUX FUNTIONS
def SQLInjection(content):
	return 0

def XSS(content):
	return 0



##################
fileParser()
##################
