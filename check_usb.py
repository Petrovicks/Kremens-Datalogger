import subprocess
import time

def check_usb():
    df = subprocess. Popen(['df', '/media/usb'], stdout = subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = \
            output.split('\n')[1].split()
    if device == '/dev/sda1' or device == '/dev/sda':
        if int(percent[:-1])<98:
            return True
        else:
            return False
    else:
        return False

if __name__ == '__main__':
    start = time.time()
    print check_usb()
    print time.time()-start
