import subprocess

def mount_usb():
    blkid = subprocess.Popen(['sudo', 'blkid'], stdout = subprocess.PIPE)
    subprocess.Popen(['sudo','umount','/media/usb'])
    output = blkid.communicate()[0]
    num = len(output.split('\n'))
    mounted = False
    for i in range(num-1):
        device = output.split('\n')[i].split()[0][:-1]
        if device[:-1] == '/dev/sda':
            subprocess.Popen(['sudo','mount',device,'/media/usb'])
            mounted = True
        elif device == '/dev/sda':
            subprocess.Popen(['sudo','mount','/dev/sda','/media/usb'])
            mounted = True
        elif device == '/dev/sdb1':
            subprocess.Popen(['sudo','mount','/dev/sdb1','/media/usb'])
            mounted = True
        elif device == '/dev/sdb':
            subprocess.Popen(['sudo','mount','/dev/sdb','/media/usb'])
            mounted = True
    return mounted
if __name__ == '__main__':
    print mount_usb()
