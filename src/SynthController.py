from xml.dom import minidom
from Channel import Channel
from Envelope import Envelope
from Synth import Synth

synth = Synth(5)

def key_down_event(response, time, note,  chan, vol="1"):
	print "KEYDOWN "
	synth.lock.acquire(1) #do block
	channel = synth.channels[int(chan)]
	id = len(channel.notes)
	channel.notes.append( {'startTime' : time, 'note' : note, 'volume': float(vol)})
	synth.lock.release()

def key_up_event():
	print "KEYUP: "

def new_chan_block_event(response, size=5, waveform="square", attack=0, decay=0, sustain=1, release=0):
	print "New channel block requested:"+str(locals())

	ids = []

	for i in range(0,int(size)):
		env = Envelope(attack, decay, sustain, release)
		channel = synth.freeChannels.pop()
		channel.envelope = env
		channel.waveform = waveform
		ids.append(channel.id)
		synth.channels[channel.id] = channel

	#generate response
	for id in ids:
		el = response.createElement("channel")
		el.setAttribute("id", str(id))
		response.firstChild.appendChild(el)


def edit_chan_event(response, id, waveform=None, attack=None, decay=None, sustain=None, release=None):
	channel = synth.channels[int(id)]
	for key, value in locals().iteritems():
		if(not ((key == 'id') or value == None )):

			if(key == 'waveform'):
				setattr(channel, key, value)
			else:
				setattr(channel.envelope, key, value)

def close_chan_event(response, id):
	#crude implementation
	synth.channels[int(id)].volume = 0
	del synth.channels[id]	

def note_del_event(response, ):
	print "notedel event"
