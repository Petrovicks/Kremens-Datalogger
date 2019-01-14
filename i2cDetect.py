import smbus
def i2cDetect(num):
    bus = smbus.SMBus(1)
    check = []
    for device in range(128):
        try:
            bus.read_byte(device)
            check.append(device)
        except:
            pass
    if check[0] == num:
        return True
    else:
        return False
if __name__ == '__main__':
    print i2cDetect(104)


