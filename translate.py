import re
item_del="######"
value_del="------"
arg_re = r'"[^\\\"]*(?:\\.[^\\\"]*)*"'
arg_re = '%s(?:\s+%s)*' % (arg_re, arg_re)
find_re = re.compile(r'^msgid\s+(' + arg_re + ')\s*\nmsgstr\s+(' + arg_re + ')\s*\n', re.M)

	

	
class File:
	def __init__(self,filename):
		self.filename=filename
		try:
			f=open(self.filename,"r")
			self.setContent(f.read())
			f.close()
		except IOError:
			self._content=""
			self._contentList=[]
			self._contentDict={}
	def getContent(self):
		return self._content

	def getStrings(self):
		pass
		
	def getDictStrings(self):
		d={}
		for i in self._contentList:
			d[i[0]]=i[1]
		return d
	def setContent(self, s):
		self._content=s
		self._contentList=self.getStrings()
		self._contentDict=self.getDictStrings()
		
	def save(self):
		f=open(self.filename,"w")
		f.write(self._content)
		f.close()

	
class POTFile(File):
	def getStrings(self):
		""" This function get the strings  to translate from a PO (or POT) file. 
		Strings are saved as a list of tuple. The first value is the msgid part, the second value is the msgstr part
		"""
		global find_re
		l=find_re.findall(self._content)
		l=[i for i in l if i[0]!='""']
		return l
		

		
class POFile(POTFile):
	def translate(self, localeDict):
		""" This function use the dictionary passed as argument localeDict to translate the po file.
		The argument, localeDict, is a dictionary {"original string":"localized string"}
		"""
		def repl(m):
			z="msgid "+m.group(1)+"\nmsgstr %s\n\n"
			if localeDict.has_key(m.group(1)): z=z %localeDict[m.group(1)]
			else: z=z %'"not translated"'
			return z
		self.setContent(find_re.sub(repl,self.getContent()))

class POCFile(File):
	def getStrings(self):
		global item_del,value_del
		l=self._content.split(item_del+"\n")
		del l[0]
		del l[-1]
		l2=[]
		for i in l:
			(x,y)=i.strip().split(value_del)
			l2.append((x.strip(),y.strip()))
		return l2
	def add(self,t):
		""" Add an entry in the catalog file only if it is  not already in the catalog file.
		If you want to replace an existing entry use the method update instead.
		"""
		global item_del,value_del
		if not(self._contentDict.has_key(t[0])):
			self._content+=item_del+"\n%s\n"+value_del+"\n%s\n"+item_del+"\n" %t



	


if __name__ == '__main__':
	print "Use ulh to use this module directly"
	