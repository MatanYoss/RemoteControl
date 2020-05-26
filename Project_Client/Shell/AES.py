from Crypto import Random
from Crypto.Cipher import AES
import hashlib
import base64
import time
import os




class AES_Crypto():
    def __init__(self):
        self.BLOCK_SIZE = 16  # Bytes
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE).encode()
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        self.signeture = hashlib.md5("CyberCyberCyber".encode()).hexdigest()


    def encrypt_Block(self, kelet, key):
        try:
            raw = self.pad(kelet) ## get str
        except:
            raw = self.pad(kelet.encode())
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv)
        res = base64.b64encode(iv + cipher.encrypt(raw)) ## ret bytes
        return res

    def Create_key(self, f_name):
        return hashlib.md5(f_name.encode('utf8')).hexdigest()

    def decrypt_Block(self, kelet, key):
        kelet = base64.b64decode(kelet) ## get bytes
        iv = kelet[:16]
        cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(kelet[16:])) ## ret str

    def Encrypt_File(self, file_place, key):
        ## get string to encrypt ==> ret b64 bytes
        ## get bytes to decrypt ==> ret plaintext
        file1 = open(file_place, 'rb')
        new_path = self.Make_Dir(file_place)
        file_name = file_place[file_place.rfind("\\"):len(file_place)]
        file2 = open(new_path + "\\" + file_name, 'w')
        while True:
            f = file1.read(16)
            if not f:
                break
            file2.write(self.encrypt_Block(f, key).decode() + "_")
        file2.write(self.encrypt_Block(file_place[file_place.rfind('.'):], key).decode() + "_" + \
                    self.signeture)
        file1.close()
        file2.close()
        os.replace(new_path + "\\" + file_name, file_place)
        os.rmdir(new_path)
        index = file_place.rfind('.')
        os.rename(file_place, file_place[:index] + ".enc")

    def Check_Signeture(self, hash):
        print(hash)
        print(self.signeture)
        if(hash != self.signeture):
            return False
        return True


    def Decrypt_File(self, file_name, key):
        file3 = open(file_name, 'r')
        d = file3.read().split("_")
        signeture_hash = ""
        #print(d)
        try:
            signeture_hash = d[-1]
        except: # file is empty...
            signeture_hash = ""
        if(signeture_hash == "" or self.Check_Signeture(signeture_hash) == False):
            return "Invalid_Encryption"
        file_type = self.decrypt_Block(d[len(d) -2], key)
        #print(file_type)
        file4 = open(file_name[:-4] + file_type.decode(), 'wb')


        for x in range(len(d) -2):
            file4.write(self.decrypt_Block(d[x], key))


        file3.close()
        file4.close()
        os.remove(file_name)
        return str(file_name[:-4] +  file_type.decode())

    def Make_Dir(self, file_place):
        disc = file_place[file_place.rfind(':') -1]
        path = disc + ":\\data"
        os.mkdir(path)
        return path










