from xml.dom import minidom
from Channel import Channel
from Envelope import Envelope
from Synth import Synth

synth = Synth(5)

def key_down_event(response, note,  chan, vol="1"):
	channel = synth.channels[int(chan)]
	channel.noteOn(note, float(vol))

def key_up_event(response, chan):
	channel = synth.channels[int(chan)]
	channel.noteOff()

def new_chan_block_event(response, size=5, waveform="0", attack=2, decay=0, sustain=1, release=2):
	print "New channel block requested:"+str(locals())

	ids = []

	for i in range(0,int(size)):
		env = Envelope(float(attack), float(decay), float(sustain), float(release))
		channel = synth.freeChannels.pop()
		channel.setEnvelope(env)
		channel.setWaveform(waveform)
		id = channel.getId()
		ids.append(id)
		synth.channels[id] = channel

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
	synth.channels[int(id)].setVolume(0)
	# todo move channel to free

def note_del_event(response, ):
	print "notedel event"
