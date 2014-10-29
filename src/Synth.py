# 
# Will handle what to communicate with the fpga
# 

from Channel import Channel
from Envelope import Envelope
import threading
import time

class Synth:


	lock = threading.Lock()
	channels = {}
	freeChannels = []
	pendingNotes = []
	playingNotes = []

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
  			print "running..."
  			self.lock.acquire(1) #blocking
 			for channel in self.channels.values():
 				for note in list(channel.notes):
 					if(note.time < )
 					print "found note: "+str(note)
 					channel.notes.remove(note)
 			self.lock.release()
  			time.sleep(0.5) ##lower later 


if __name__ == "__main__":
	synth = Synth(10)
  	time.sleep(10)
