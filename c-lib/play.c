#include "play.h"
#include <linux/i2c-dev.h> 
#include <sys/ioctl.h> 
#include <fcntl.h> 
#include <unistd.h>
#include <stdio.h> 
#include <stdlib.h> 

static const char *devName = "/dev/i2c-1";

int playNote(unsigned char channel, unsigned char effect, unsigned char freq, unsigned char type, unsigned char volume) {
	// Check the variables
	//if (channel >= 128 || effect > 3 || freq > 1024 || type > 8 || volume > 128) {
	//	return (4);
	//}
	
	int file;
	// Setting up the I2C client 
	if ((file = open(devName, O_RDWR)) < 0) {
		return (1);
	}

	// Requesting the I2C channel
	if (ioctl(file, I2C_SLAVE, channel) < 0) {
		return (2);
	}

	// Preparing the data to write
	unsigned char buffer[3];
	buffer[2] = freq;
	buffer[1] = ((volume & 0b1111111) << 1) + ((type & 0b100) >> 2);
	buffer[0] = ((type & 0b11) << 6) + ((effect & 0b111) << 3);

	if (write(file, buffer, 3) == 1) {
		return (3);
	}
}