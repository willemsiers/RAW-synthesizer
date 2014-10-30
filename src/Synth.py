# 
# Will handle what to communicate with the fpga
# 

from Channel import Channel
from Envelope import Envelope
import threading
import time
from ctypes import cdll
lib = cdll.LoadLibrary('./play.o')

class Synth:

	lock = threading.Lock()
	channels = {}
	freeChannels = []

	def __init__(self, maxChannel):

		for i in range(0, maxChannel):
			env = Envelope(0, 0, 1, 0) #default
			channel = Channel(i, "square", env)
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
 					print status
 					#int playNote(unsigned char channel, unsigned char effect, unsigned char note, unsigned char type, unsigned char volume)
 					print "calling C: " +str(lib.playNote(channel.getId(), channel.effect, status['note'], status['waveform'], int(status['volume'])))
			time.sleep(0.24) ##lower later 


if __name__ == "__main__":
	synth = Synth(10)
  	time.sleep(10)
