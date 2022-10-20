import struct


#your input  
list1=[0x41, 0xCB, 0xAB, 0x3B]
# aa=str(bytearray(list1))  # edit: this conversion wasn't needed
aa= bytearray(list1) 
print(struct.unpack('<f', aa))
