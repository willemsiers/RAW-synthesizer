import time

import sys
import select

MIN_TIME = 0.0001 #quality code
MAX_SUSTAINED_TIME = 6

class Envelope:

	def __init__(self, attack, decay, sustain, release):
		self.attack = max(attack, MIN_TIME)
		self.decay = max(decay,MIN_TIME)
		self.sustain = sustain
		self.release = max(release,MIN_TIME)
		self.sustained = 0;
		self.endTime = 0;

	def trigger(self):
		self.startTime = time.time()
		self.sustained = None
		self.started = True;

	def untrigger(self, volume=-1):
		self.endTime = time.time()
		if(volume == -1):
			self.sustained = self.getAmplitude()
		else:
			self.sustained = volume

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
				if(currentTime >= MAX_SUSTAINED_TIME):
					self.untrigger(volume)

		volume = min(1, max(volume, 0))
		return volume

	def set_attack(self, val):
		self.attack = max(MIN_TIME, val)

	def set_decay(self, val):
		self.decay = max(MIN_TIME, val)

	def set_sustain(self, val):
		self.sustain = max(MIN_TIME, val)

	def set_release(self, val):
		self.release = max(MIN_TIME, val)

#function used for debugging
def checkInput():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False

if __name__ == '__main__':

	A = 1
	D = 1
	S = 0.2
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

