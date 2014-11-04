import Server
from xml.dom import minidom
from Channel import Channel
from Envelope import Envelope
from Synth import Synth
import time

synth = Synth(63)
blocks = 0

_log = []

def appendLog(event):
	event.setAttribute("eventtime", str(Server.getTime(time.time())))
	_log.append(event)

#returns all items from lastReceivedId (exclusive) till the end, and also returns the to-be lastReceivedId
def readLogAfter(lastReceivedId):
	return (_log[(lastReceivedId+1):], len(_log)-1)

def key_down_event(event, response, note,  chan, vol=1):
	channel = synth.channels[int(chan)]
	channel.noteOn(int(note), float(vol))

def key_up_event(event, response, chan):
	channel = synth.channels[int(chan)]
	elem = minidom.Document().createElement("note")

	elem.setAttribute("start", str(Server.getTime(channel.getEnvelope().startTime)))
	elem.setAttribute("end", str(Server.getTime(time.time())))
	elem.setAttribute("note", str(channel.getNote()))
	elem.setAttribute("vol", str(channel.getVelocity()))
	elem.setAttribute("chan", str(chan))
	appendLog(elem)
	channel.noteOff()

def new_chan_block_event(event, response, size=5, waveform=1, attack=0.2, decay=0.1, sustain=0.9, release=0.7):
	print "New channel block requested:"+str(locals())

	blockId = synth.blocks
	synth.blocks = synth.blocks + 1
	
	ids = []

	for i in range(0,int(size)):
		env = Envelope(float(attack), float(decay), float(sustain), float(release))
		channel = synth.freeChannels.pop()
		channel.closing = False
		channel.setEnvelope(env)
		channel.setWaveform(int(waveform))
		id = channel.getId()
		ids.append(id)
		synth.channels[id] = channel

	#generate response
	sub = response.createElement("channel_block")
	sub.setAttribute("id", str(blockId))

	for id in ids:

		el = response.createElement("channel")
		el.setAttribute("id", str(id))
		el.setAttribute("waveform", str(waveform))
		sub.appendChild(el)
		
	appendLog(sub)
	response.firstChild.appendChild(sub)


def edit_chan_event(event, response, id, waveform=None, attack=None, decay=None, sustain=None, release=None):
	channel = synth.channels[int(id)]
	for key, value in locals().iteritems():
		if(not ((key == 'id') or value == None )):
			if(key == 'waveform'):
				setattr(channel, key, value)
			else:
				setattr(channel.envelope, key, value)

	appendLog(event)

def close_chan_event(event, response, id):
	channel = synth.channels[int(id)]
	channel.setVolume(0)
	channel.closing = True
	appendLog(event)


def set_master_volume(event, response, volume):
	Channel.MAX_VOLUME = volume

def set_distortion(event, response, level):
	print "'set_distortion called'"