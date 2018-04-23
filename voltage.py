# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# This code is designed to work with the PECMAC125A_DLCT03C20 I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Current?sku=PECMAC125A_DLCT03C20#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# PECMAC125A address, 0x2A(42)
# Command for reading device identification data
# 0x6A(106), 0x02(2), 0x00(0),0x00(0), 0x00(0) 0x00(0), 0xFE(254)
# Header byte-2, command-2, byte 3, 4, 5 and 6 are reserved, checksum
command2 = [0x6A, 0x02, 0x00, 0x00, 0x00, 0x00, 0xFE]
bus.write_i2c_block_data(0x2A, 0x92, command2)
j = 10
time.sleep(0.5)

# PECMAC125A address, 0x2A(42)
# Read data back from 0x55(85), 3 bytes
# Type of Sensor, Maximum Current, No. of Channels
data = bus.read_i2c_block_data(0x2A, 0x55, 3)

# Convert the data
typeOfSensor = data[0]
maxCurrent = data[1]
noOfChannel = data[2]

# Output data to screen
print "Type of Sensor : %d" %typeOfSensor
print "Maximum Voltage : %d V" %maxCurrent
print "No. of Channels : %d" %noOfChannel

# PECMAC125A address, 0x2A(42)
# Command for reading voltage
# 0x6A(106), 0x05(5), 0x01(1),0x02(2), 0x00(0), 0x00(0) 0x04(4)
# Header byte-2, command-5, start channel-1, stop channel-12, byte 5 and 6 reserved, checksum
command1 = [0x6A, 0x05, 0x01, 0x02, 0x00, 0x00, 0x04]
bus.write_i2c_block_data(0x2A, 0x92, command1)
time.sleep(0.5)

# PECMAC125A address, 0x2A(42)
# Read data back from 0x55(85), No. of Channels * 3 bytes
# current MSB1, current MSB, current LSB
data1 = bus.read_i2c_block_data(0x2A, 0x55, 2*3)

# Convert the data
for i in range(0, 2) :
        msb1 = data1[i * 3]
        msb = data1[1 + i * 3]
        lsb = data1[2 + i * 3]

        # Convert the data to ampere
        volt = (msb1 * 65536 + msb * 256 + lsb) / 1000.0

        # Output data to screen
        print "Channel no : %d " %(i + 1)
        print "volt Value : %.3f A" %volt

