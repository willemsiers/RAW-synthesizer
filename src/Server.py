import web
import Channel
import Envelope
from xml.dom import minidom
import SynthController
import time

urls = (
  '/*', 'index',
  "/api/", "api",
  "/api", "api"
)

class api:

	def GET(self):
		web.header('Content-Type', 'text/xml')
		params = web.input(lastId="-1")
		lastId = params.lastId
		#synthcontroller get log
		return lastId

	def POST(self):
		web.header('Content-Type', 'text/xml')
		data = web.data()

		dom = minidom.parseString(data)

		response = minidom.Document()
		parent = response.createElement("raw")
		response.appendChild(parent)
		for event in dom.childNodes[0].childNodes:
			tagName = event.tagName
			parser = getattr(SynthController, tagName+"_event")
			parser(event, response, **dict(event.attributes.items()))

		return response.toprettyxml()

class index:
	def GET(self):
		return render.index()

epoch = time.time()

def getTime(_time):
	return int(( _time - epoch ) * pow(10,5))

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()