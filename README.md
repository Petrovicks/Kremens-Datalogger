Refactored codebase of the Raspberry Pi-based dataloggers used for wildland fire research.

Hardware: Raspberry Pi 2 B, DS1307 RTC, IR Camera (Lepton)

Pi configuration notes:
- Baudrate wasn't set in config.txt, currently set it to 9600
	- RTC clock supports up to 100 kbits/s (where?)
- main must be located in /home/pi/Desktop
	- dependency in Lepton/ requires this, unsure of specific reason
- update_from_git is used to clean out the Desktop and replace files with an updated clone from this repo
- clock_debugging.py will print out all register values and RTC datetime object
	- contains commented code used to create specific usecases
- Calls to run code upon boot is located in ~/etc/profile 
