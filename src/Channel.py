import time
import Envelope

class Channel:

	#current channel's volume [0-1]
	_waveshapes = ['square', 'sine', 'triangle', 'saw', 'noise']
	_lastAmplitude = -1
	_volume = 1.000
	effect = 0 #unused still
	

	def __init__(self, channelNumber, waveform, envelope):
	    print("Initialising Channel...#"+str(channelNumber))
	    self._id = channelNumber
	    self.setWaveform(waveform)
	    self.setEnvelope(envelope)
	    self._changed = True #True to update the first time the channel is created
 	    self._note = 0
 	    self._volume = 1

 	def setWaveform(self, waveform):
 		self._waveform = waveform
 		self._changed = True

 	def setEnvelope(self, envelope):
 		self._envelope = envelope
 		#no need to update _changed

	#call whenever the key is pressed (note as a string)
	def noteOn(self, note, velocity):
		self._note = note
		self._envelope.trigger()
		self._volume = velocity
		# self._changed = True (Not needed)

	#call whenever the key is released
	def noteOff(self):
		self._envelope.untrigger()

	def setVolume(self, volume):
		self._volume = min(127, max(0, volume))
		self._changed = True

	#envelope's amplitude multiplied with the channel's volume
	def getAmplitude(self):
		return self._envelope.getAmplitude() * self._volume

	def getNote(self):
		return self._note	

	def getStatus(self):
		amplitude = self.getAmplitude()
		self._changed = (self._changed or (not (amplitude == self._lastAmplitude)))

		if(not (self._changed)):
			return False
		else:
			self._lastAmplitude = amplitude
			self._changed = False
			return {'volume' : amplitude,
					'waveform' : self._waveform,
					'note' : self._note}

	def getId(self):
		return self._id

if __name__ == '__main__':
	print "channel main"
	env = Envelope.Envelope(0.5,0.3,0.65,0.8)
	channel = Channel(0, 3, env)
	channel.noteOn('26')
	time.sleep(1)
	channel.noteOff()
	while(True):
		print channel.getAmplitude()
