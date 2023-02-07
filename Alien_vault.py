import pefile
from OTXv2 import OTXv2
import hashlib
import IndicatorTypes
import string
import binascii
import os
API_KEY = "your API" 
filename="packedboy"
def hex_editor(filename):
    list_editor=""
    data_list=[]
    full_list=""
    counter=0
    try:
        with open(filename, "rb") as file:
            while 1:
                byte_s = file.read(1)
                data_bytes2ascii = binascii.b2a_hex(byte_s)
                list_editor+=str(data_bytes2ascii, 'UTF-8')+"\t"
                data_list.append(int(str(data_bytes2ascii, 'UTF-8'),16))
                full_list+= str(data_bytes2ascii, 'UTF-8') + " "
                if counter == 16:
                    print(list_editor)
                    print("\t".join(map(chr, data_list)))
                    counter=0
                    list_editor=""
                    data_list=[]
                    full_list+=str(data_bytes2ascii, 'UTF-8')+"\n"
                if not byte_s:
                    break
                counter+=1
    except:
        pass
    print("="*30)
    print(full_list)
def strings(filename, min=8):
    with open(filename, errors="ignore") as file:
        result = ""
        for character in file.read():
            if character in string.printable:
                result += character
                continue
            if len(result) >= min:
                yield result
            result = ""
        if len(result) >= min:
            yield result
size = os.path.getsize(filename)
print("File size:",size)
file=pefile.PE(filename)
print("File hashes:")
with open(filename, mode="rb") as File:
    hash_256 = hashlib.sha256(File.read()).hexdigest()
    hash_md5 = hashlib.md5(File.read()).hexdigest()
    hash_sha1 = hashlib.sha1(File.read()).hexdigest()
    print("MD5:",hash_md5)
    print("SAH-256",hash_256)
    print("SHA-1",hash_sha1)
print("Imphash:",file.get_imphash())
for dll in file.DIRECTORY_ENTRY_IMPORT:
    print(dll)
    for functions in dll.imports:
        print(functions.name)
print(file)
otx = OTXv2(API_KEY, server='https://otx.alienvault.com/')
result = otx.get_indicator_details_full(IndicatorTypes.FILE_HASH_MD5, hash_md5)
print("Alienvault Result:\n",result)
print("String Result:")
for string_line in strings(filename):
    print(string_line)
print("File Hex Editor:")
try:
    hex_editor(filename)
except:
    pass
