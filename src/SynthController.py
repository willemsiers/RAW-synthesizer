import Server
from xml.dom import minidom
from Channel import Channel
from Envelope import Envelope
from Synth import Synth
import time

synth = Synth(63)

_log = []

def appendLog(event):
	event.setAttribute("eventtime", Server.getTime(time.time()))
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
	elem.setAttribute("start", Server.getTime(channel.getEnvelope().startTime))
	elem.setAttribute("end", Server.getTime(time.time()))
	elem.setAttribute("note", channel.getNote())
	elem.setAttribute("vol", channel.getVelocity())
	elem.setAttribute("chan", chan)
	appendLog(elem)

	channel.noteOff()



def new_chan_block_event(event, response, size=5, waveform=0, attack=2, decay=0, sustain=1, release=2):
	print "New channel block requested:"+str(locals())

	ids = []

	for i in range(0,int(size)):
		env = Envelope(float(attack), float(decay), float(sustain), float(release))
		channel = synth.freeChannels.pop()
		channel.setEnvelope(env)
		channel.setWaveform(int(waveform))
		id = channel.getId()
		ids.append(id)
		synth.channels[id] = channel

	#generate response
	for id in ids:
		el = response.createElement("channel")
		el.setAttribute("id", str(id))
		response.firstChild.appendChild(el)


def edit_chan_event(event, response, id, waveform=None, attack=None, decay=None, sustain=None, release=None):
	channel = synth.channels[int(id)]
	for key, value in locals().iteritems():
		if(not ((key == 'id') or value == None )):
			if(key == 'waveform'):
				setattr(channel, key, value)
			else:
				setattr(channel.envelope, key, value)

def close_chan_event(event, response, id):
	#crude implementation
	channel = synth.channels[int(id)]
	channel.setVolume(0)
	##UNFINISHED: should only remove ffrom active channels AFTER an update with volume 0 has been sent to the fpga
	synth.channels.pop[int(id)] #should be threadsafe?
	synth.freeChannels.append(channel)