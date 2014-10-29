import web
import Channel
import Envelope
from xml.dom import minidom
import SynthController

urls = (
  '/*', 'index',
  "/api/", "api",
  "/api", "api"
)

class api:

	changes = {}
	lastReceivedUpdate = 0

	def GET(self):
		web.header('Content-Type', 'text/xml')
		params = web.input(lastId="-1")
		lastId = params.lastId
		print lastId
		return lastId

	def POST(self):
		web.header('Content-Type', 'text/xml')
		data = web.data()

		dom = minidom.parseString(data)

		updateId = self.lastReceivedUpdate
		self.lastReceivedUpdate += 1
		updateChanges = []

		response = minidom.Document()
		parent = response.createElement("raw")
		response.appendChild(parent)
		for node in dom.childNodes[0].childNodes:
			tagName = node.tagName
			parser = getattr(SynthController, tagName+"_event")
			parser(response, **dict(node.attributes.items()))

			updateChanges.append(node)

		self.changes[updateId] = updateChanges
		return response.toprettyxml()

class index:
	def GET(self):
		return render.index()

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()