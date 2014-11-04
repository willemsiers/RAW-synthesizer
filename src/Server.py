import web
import Channel
import Envelope
from xml.dom import minidom
import SynthController
import time

render = web.template.render('static/')

urls = (
  "/", "index",
  "/api/", "api",
  "/api", "api"
)

class api:

	def GET(self):
		web.header('Content-Type', 'text/xml')
		params = web.input(lastid="-1")

		response = minidom.Document()
		parentEl = response.createElement("raw")
		changeEl = response.createElement("changeset")

		lastId = int(params.lastid)
		logAfter = SynthController.readLogAfter(lastId)
		log = logAfter[0]
		newId = logAfter[1]

		for e in log:
			changeEl.appendChild(e)

		changeEl.setAttribute("id",str(newId))
		parentEl.appendChild(changeEl)
		response.appendChild(parentEl)

		return response.toprettyxml()

	def POST(self):
		web.header('Content-Type', 'text/xml')
		data = web.data()
		print data
		data.replace("\n\r",'')
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
		return web.redirect("static/index.htm") #jajaj

epoch = time.time()

def getTime(_time):
	return int(( _time - epoch ) * pow(10,5))

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()