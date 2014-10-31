# 
# Will handle what to communicate with the fpga
# 

from Channel import Channel
from Envelope import Envelope
import threading
import time
from ctypes import cdll
lib = cdll.LoadLibrary('./play.o')

TIME_STEP = 0.009

class Synth:

	lock = threading.Lock()
	channels = {}
	freeChannels = []

	def __init__(self, maxChannel):

		for i in range(0, maxChannel):
			env = Envelope(0, 0, 1, 0) #default
			channel = Channel(self, i, "0", env)
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
					#print status
					#int playNote(unsigned char channel, unsigned char effect, unsigned char note, unsigned char type, unsigned short volume)

					params = {'channel':channel.getId(), 'effect': int(channel.effect), 
								'note': int(status['note']), 
								'type' : int(status['waveform']), 
								'volume':int(status['volume'])}
					print "calling lib->(" +str(lib.playNote(**params)) + ") from params:" + str(params)
			time.sleep(TIME_STEP) ##lower later 

