#include <string.h> 
#include <unistd.h> 
#include <errno.h> 
#include <stdio.h> 
#include <stdlib.h> 
#include <linux/i2c-dev.h> 
#include <sys/ioctl.h> 
#include <fcntl.h> 
#include <unistd.h>

// The address to use to connect with the I2C device
#define ADDRESS 0x02

// The I2C bus: This is for V2 pi's. For V1 Model B you need i2c-0
static const char *devName = "/dev/i2c-1";

int main(int argc, char** argv) {
	// Check for the correct command line arguments
	if (argc != 2 && argc != 3 && argc != 4) {
		printf("%s%s%s%s%s","usage: ",argv[0]," read(from) ($address) or ",argv[0]," write(to) ($address) $data\n");
		exit(1);
	}

	// Setting up the I2C client (requires i2c-tools
	//printf("I2C: Connecting\n");
	int file;
	if ((file = open(devName, O_RDWR)) < 0) {
		fprintf(stderr, "I2C: Failed to access\n");
		exit(1);
	}

	//Creating a buffer for the read/write operation
	unsigned char cmd[16];

	// Execute a write operation
	if(!strcmp(argv[1],"write")) {
		if(argc == 3) {
			// Requesting the I2C channel
			//printf("I2C: acquiring buss to 0x%x\n", ADDRESS); 
			if (ioctl(file, I2C_SLAVE, ADDRESS) < 0) {
				fprintf(stderr, "I2C: Failed to acquire bus access/talk to slave 0x\n");
				close(file);
				exit(1);
			}
			
			//0 means that the user can select a base by using 0 (octal) or 0x (hexadecimal)
			unsigned long c = strtol(argv[2],NULL,0); 
			//printf("Sending %lu\n", c);
			unsigned char bfr[3];
			bfr[0] = (int)((c >> 16) & 0xFF);
			bfr[1] = (int)((c >> 8) & 0xFF);
			bfr[2] = (int)(c & 0xFF);
			//printf("%s%x%x%x\n","Sending 0x",bfr[0],bfr[1],bfr[2]);
			if (write(file,bfr, 3) == 1) {
				printf("Failed to send data over I2C\n");
			}
		}
		else {
			printf("%s%s%s","usage: ",argv[0]," write $data\n");
		}
	}
	// Execute a write operation to a specific address
	else if(!strcmp(argv[1],"writeto")) {
		if(argc == 4) {
			// Requesting the I2C channel
			unsigned char addr = (unsigned char) strtol(argv[2],NULL,0); 
			//printf("I2C: acquiring buss to 0x%x\n", addr); 
			if (ioctl(file, I2C_SLAVE, addr) < 0) {
				fprintf(stderr, "I2C: Failed to acquire bus access/talk to slave 0x%x\n", addr);
				exit(1);
			}
			
			//0 means that the user can select a base by using 0 (octal) or 0x (hexadecimal)
			unsigned long c = strtol(argv[3],NULL,0); 
			//printf("Sending %lu\n", c);
			unsigned char bfr[3];
			bfr[0] = (int)((c >> 16) & 0xFF);
			bfr[1] = (int)((c >> 8) & 0xFF);
			bfr[2] = (int)(c & 0xFF);
			//printf("%s%x%x%x\n","Sending 0x",bfr[0],bfr[1],bfr[2]);
			if (write(file,bfr, 3) == 1) {
				printf("Failed to send data over I2C\n");
			}
		}
		else {
			printf("%s%s%s","usage: ",argv[0]," writeto $address $data\n");
		}
	}
	// Execute a read operation
	else if (!strcmp(argv[1],"read")) {
		if (argc == 2) {
			// Requesting the I2C channel
			//printf("I2C: acquiring buss to 0x%x\n", ADDRESS); 
			if (ioctl(file, I2C_SLAVE, ADDRESS) < 0) {
				fprintf(stderr, "I2C: Failed to acquire bus access/talk to slave 0x%x\n", ADDRESS);
				exit(1);
			}
			char buf[1];
			if (read(file, buf, 3) == 1) {
				int temp = (int) buf[0];
				//printf("Received %d\n", temp);
			} else {
				printf("Failed to read data over I2C\n");
			}
		}
		else {
			printf("%s%s%s", "usage: ",argv[0], " read \n");
		}
	}
	// Execute a read operation from a certain address
	else if (!strcmp(argv[1],"readfrom")) {
		if (argc == 3) {
			// Requesting the I2C channel
			unsigned char addr = (unsigned char) strtol(argv[2],NULL,0); 
			//printf("I2C: acquiring buss to 0x%x\n", addr); 
			if (ioctl(file, I2C_SLAVE, addr) < 0) {
				fprintf(stderr, "I2C: Failed to acquire bus access/talk to slave 0x%x\n", addr);
				exit(1);
			}
			char buf[1];
			if (read(file, buf, 3) == 1) {
				int temp = (int) buf[0];
				//printf("Received %d\n", temp);
			} else {
				printf("Failed to read data over I2C\n");
			}
		}
		else {
			printf("%s%s%s", "usage: ",argv[0], " readfrom $address \n");
		}
	}
	else {
		printf("%s%s%s%s%s","usage: ",argv[0]," read or ",argv[0]," write byte\n");
		exit(1);
	}


	// Sleep and close the file
	usleep(10000);
	close(file);
	return (EXIT_SUCCESS);
}

