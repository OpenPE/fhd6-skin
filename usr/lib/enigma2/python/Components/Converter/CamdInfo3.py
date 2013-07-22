from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
import os

class CamdInfo3(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		camd = ""
		if not info:
			return ""
		if fileExists("/tmp/cam.info"):
			try:
				camdlist = open("/tmp/cam.info", "r")
			except:
				return None	
		elif fileExists("/etc/init.d/softcam"):
			try:
				camdlist = os.popen("/etc/init.d/softcam info")
			except:
				return None
		elif fileExists("/etc/init.d/cardserver"):
			try:
				camdlist = os.popen("/etc/init.d/cardserver info")
			except:
				return None
		else:
			return None

		if camdlist is not None:
			for current in camdlist.readlines():
				camd = current
			camdlist.close()
			return camd
		else:
			return ""

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)
