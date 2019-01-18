Codebase used for datalogging kits used for wildland fire research. Codebase will undergo heavy refactoring.

Hardware: Raspberry Pi 2 B, DS1307 RTC, IR Camera (unknown)

Pi configuration notes:

- CPU is overclocked to 800 MHz (unknown reason why)
- Baudrate wasn't set in config.txt, currently set it to 9600
	- RTC clock supports up to 100 kbits/s (where?)
- Calls to run code upon boot is located in ~/etc/profile 
	- Pi manually sets a hardcoded date as a starting point since DS1307 only cares about time after the year 2000
	- TODO: Add github intergration where upon detecting wifi on boot, will clean current working directory and clone repo into the cwd properly.
		- Lepton requires recursive (parent and all subdirectories) rwx permissions to be set.
- Currently assumes operation in the Pi's desktop (/home/pi/Desktop/)
