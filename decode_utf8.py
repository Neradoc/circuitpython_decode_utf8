# SPDX-FileCopyrightText: Copyright (c) 2025 Neradoc
# SPDX-License-Identifier: MIT
"""
Original Code point 	Byte 1 	Byte 2 	Byte 3 	Byte 4
U+0000 		U+007F 		0yyyzzzz 	
U+0080 		U+07FF 		110xxxyy 	10yyzzzz 	
U+0800 		U+FFFF 		1110wwww 	10xxxxyy 	10yyzzzz 	
U+010000 	U+10FFFF 	11110uvv 	10vvwwww 	10xxxxyy 	10yyzzzz

Going through each byte, pass low ASCII bytes.
For high bytes, assume UTF8 character
- find the length based on top bits
- try to decode the UTF8 bytes for that length
  - if it works, take that and skip the correct number of bytes
  - if not just ignore the byte an loop to the next one
"""

def decode_ascii(source):
    return bytes([x for x in source if x < 0x80]).decode()

M1 = 0b1110_0000
M2 = 0b1111_0000
M3 = 0b1111_1000
B1 = 0b1100_0000
B2 = 0b1110_0000
B3 = 0b1111_0000

def try_decode(inb):
    try:
        return inb.decode("utf8")
    except:
        return False

def decode_no_errors(source):
    try:
        out = source.decode("utf8")
    except:
        out = ""
        i = 0
        while i < len(source):
            char = source[i]
            if char < 128:
                out += chr(char)
            else:
                size = -1 # if not like a starting UTF8
                if char & M1 == B1: # 2 bytes utf8 char
                    size = 1
                elif char & M2 == B2: # 3 bytes utf8 char
                    size = 2
                elif char & M3 == B3: # 4 bytes utf8 char
                    size = 3
                res = try_decode(source[i:i + size + 1])
                if res:
                    i = i + size
                    out += res
            i = i + 1
    return out

def _test():
    sources = [
        b'\x80abc' + 'é©¢ç'.encode("utf8"),
        b'\x80' + "😛😀😍".encode("utf8"),
    ]

    for source in sources:
        print(source)
        print(">", decode_ascii(source))
        print(">", decode_no_errors(source))

if __name__ == "__main__":
    _test()
