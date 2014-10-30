#include <string.h> 
#include <unistd.h> 
#include <errno.h> 
#include <stdio.h> 
#include <stdlib.h> 
#include <linux/i2c-dev.h> 
#include <sys/ioctl.h> 
#include <fcntl.h> 
#include <unistd.h>

int main (int argc, char** argv) {
	playNote((unsigned char) 32, (unsigned char) 2, (unsigned char) 2, (unsigned char) 2, (unsigned char) 7);
}