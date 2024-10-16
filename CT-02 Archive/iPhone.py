import pymtp
mtp = pymtp.MTP()
mtp.connect()

print(mtp.get_devicename())
