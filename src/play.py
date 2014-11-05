from subprocess import call

def playNote (channel, effect, note, type, volume):
	volume = min(volume, 1023) 
	print str(locals())
	data1 = format(type + (effect << 3) + (volume << 6), 'x')
	while len(data1) < 4:
		data1 = "0" + data1
	data1 = format(note, 'x') + data1
	if len(data1) < 6:
		data1 = "0x0" + data1
	else:
		data1 = "0x" + data1
	#print data1
	call(["./rwi2c", "writeto", hex(channel), data1])	

def setDistortion (distortion):
	print distortion
	dist = distortion | (1<<21)
	call(["./rwi2c", "writeto", hex(0), hex(dist)])
