import time
from NoteFrequencyTable import noteToFreq
import Envelope

class Channel:

	#current channel's volume [0-1]
	volume = 1
	waveform = 5
	waveshapes = ['square', 'sine', 'triangle', 'saw', 'noise']
	notes = []

	def __init__(self, channelNumber, waveform, envelope):
	    print("Initialising Channel...#"+str(channelNumber))
	    self.id = channelNumber
	    self.waveform = waveform
	    self.envelope = envelope

	#set the frequency to play and trigger the envelope (frequency in hz)
	def freqOn(self, frequency):
		self.frequency = frequency
		self.envelope.trigger()

	#call whenever the key is pressed (note as a string)
	def noteOn(self, note):
		self.freqOn(noteToFreq[note])

	#call whenever the key is released
	def noteOff(self):
		self.envelope.untrigger()

	#envelope's amplitude multiplied with the channel's volume
	def getAmplitude(self):
		return self.envelope.getAmplitude() * self.volume

	def getChannelNumber(self):
		return self.channelNumber

if __name__ == '__main__':
	print "channel main"
	env = Envelope.Envelope(0.5,0.3,0.65,0.8)
	channel = Channel(0, 3, env)
	channel.noteOn('C5')
	time.sleep(1)
	channel.noteOff()
	while(True):
		print channel.getAmplitude()
