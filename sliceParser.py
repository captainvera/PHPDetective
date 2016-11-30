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


test = Slice()
test.getItems()
