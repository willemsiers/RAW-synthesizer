import time

import sys
import select

class Envelope:

	MAX_VOLUME = 1

	def __init__(self, attack, decay, sustain, release):
		self.attack = attack
		self.decay = decay
		self.sustain = sustain
		self.release = release
		self.sustained = 0;
		self.endTime = 0;

	def trigger(self):
		self.startTime = time.time()
		self.sustained = None
		self.started = True;

	def untrigger(self):
		self.endTime = time.time()
		self.sustained = self.getAmplitude()

	def getAmplitude(self):
		volume = -1
		if((not (self.sustained is None))):
			currentTime = time.time() - self.endTime
			volume = self.sustained - self.sustained * (currentTime / self.release)
		else:
			currentTime = time.time()-self.startTime
			if(currentTime <= self.attack):
				volume = currentTime / self.attack
			elif(currentTime <= self.attack + self.decay):
				volume = 1-(((currentTime-self.attack)/self.decay)*(1-self.sustain))
			else: 
				volume = self.sustain

		volume = min(1, max(volume, 0))
		return volume

#function used for debugging
def checkInput():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False

if __name__ == '__main__':

	A = 2
	D = 1
	S = 0.25
	R = 1

	tone = Envelope(A,D,S,R)
	started = False
	while(True):
		if (checkInput()):
			tone.untrigger() if started else tone.trigger()
			started = not started
		print tone.getAmplitude()
		time.sleep(0.025)


	A = float(raw_input('A=\n'))
	D = float(raw_input('D=\n'))
	S = float(raw_input('S=\n'))
	R = float(raw_input('R=\n'))

	tone = ADSR(A,D,S,R)
	tone.trigger()

	vol = 0
	while(vol != -1):
		vol = tone.getAmplitude()
		print(vol)

