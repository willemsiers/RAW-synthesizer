from xml.dom import minidom
from Channel import Channel
from Envelope import Envelope

def parse(node):
	return node

channels = {}


def key_down_event(id,time,note,vol,chan):
	print "KEYDOWN: "

def key_up_event():
	print "KEYUP: "

def new_chan_block_event(response, size=5, waveform="square", attack=0, decay=0, sustain=1, release=0):
	print "New channel block requested:"+str(locals())

	ids = []

	for i in range(0,int(size)):
		env = Envelope(attack, decay, sustain, release)
		env.trigger()
		id = len(channels)
		ids.append(id)
		channel = Channel(int(id), waveform, env)
		channels[int(id)] = channel

	#generate response
	for id in ids:
		el = response.createElement("channel")
		el.setAttribute("id", str(id))
		response.firstChild.appendChild(el)


def edit_chan_event(response, id, waveform=None, attack=None, decay=None, sustain=None, release=None):
	channel = channels[int(id)]
	for key, value in locals().iteritems():
		if(not ((key == 'id') or value == None )):

			if(key == 'waveform'):
				setattr(channel, key, value)
			else:
				setattr(channel.envelope, key, value)

def close_chan_event(response, id):
	#crude implementation
	channels[int(id)].volume = 0
	del channels[id]	

def note_del_event(response, ):
	print "notedel event"
