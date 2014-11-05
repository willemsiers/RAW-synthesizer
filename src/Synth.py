# 
# Will handle what to communicate with the fpga
# 

from Channel import Channel
from Envelope import Envelope
import threading
import time
import play

TIME_STEP = 0.005

class Synth:

	def setDistortion(self, distortion):
		self._distortion = distortion
		self._dist_changed = True

	lock = threading.Lock()
	channels = {}
	freeChannels = []
	blocks = 0

	def __init__(self, maxChannel):
		self._dist_changed = False
		self._overdrive = 4
		for i in range(0, maxChannel):
			env = Envelope(0, 0, 1, 0) #default
			channel = Channel(self, i, 0, env)
			self.freeChannels.append(channel)

		t = threading.Thread(target=self.main, args = ())
		t.daemon = True #autokill
		t.start()

	def main(self):
		print "Starting main synth thread"
		while(True):
			for channel in self.channels.values():
				status = channel.getStatus()
				if(status):
					params = {  'channel':int(channel.getId()), 'effect': int(channel.effect), 
								'note': int(status['note']), 
								'type' : int(status['waveform']), 
								'volume':int(int(status['volume']) * self._overdrive) }

					play.playNote(**params)
			if(self._dist_changed):
				self._dist_changed = False
				play.setDistortion(self._distortion)
			time.sleep(TIME_STEP) 