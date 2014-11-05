import time
import Envelope

MAX_VOLUME = pow(2,10)-1

class Channel:

	#current channel's volume [0-MAX_VOLUME]
	_lastAmplitude = -1
	effect = 0 #unused still

	def __init__(self, synth, channelNumber, waveform, envelope):
	    print("Initialising Channel...#"+str(channelNumber))
	    self._id = channelNumber
	    self.setWaveform(waveform)
	    self.setEnvelope(envelope)
	    self._changed = True #True to update the first time the channel is created
 	    self._note = 0
 	    self._velocity = 0
 	    self._synth = synth
 	    self._closing = False

 	def setWaveform(self, waveform):
 		self._waveform = waveform
 		self._changed = True

 	def setEnvelope(self, envelope):
 		self._envelope = envelope
 		#no need to update _changed

 	def getEnvelope(self):
 		return self._envelope

	def noteOn(self, note, velocity):
		self._note = note
		self._envelope.trigger()
		self._velocity = velocity
		# self._changed = True (Not needed)

	#call whenever the key is released
	def noteOff(self):
		self._envelope.untrigger()

	def getVelocity(self):
		return self._velocity


	# envelope multiplied with the available shared volume and then multiplied with the velocity
	def getAmplitude(self):
		return self._envelope.getAmplitude() * ( MAX_VOLUME / len(self._synth.channels))

	def getNote(self):
		return self._note	

	def getStatus(self):
		amplitude = self.getAmplitude()
		self._changed = (self._changed or (not (amplitude == self._lastAmplitude)))
		self._lastAmplitude = amplitude

		if(int(amplitude) == int(0) and self._closing):
			self._synth.channels.pop[int(id)]
			self._synth.freeChannels.append(channel)
		

		if(not (self._changed)):
			return False
		else:
			self._changed = False
			return {'note' : self._note,
					'volume' : amplitude,
					'waveform' : self._waveform
					}

	def getId(self):
		return self._id