from abc import ABC, abstractmethod
from math import ceil
import random

def _get_key(dict, val):
    for k, v in dict.items():
        if v == val:
            return k

def _expand_list(li, size):
    newList = list(li[0 : len(li)])
    l = 0
    for i in range(0, size):
        newList.append(li[l])
        l += 1
        if l == len(li):
            l = 0
    return newList

class WrongKeyException(Exception):
    pass

class WrongEncryptionException(Exception):
    pass

class StringIsNotAKeyException(Exception):
    pass

class Alphabet:
    alphabet = []
    def __init__(self, s):
        self.alphabet = s.split(',')
        self.alphabet.append(',')
        self.alphabet.append('\n')

class Key:    
    encode_type = -1
    key = None
    def __init__(self, s):
        self.encode_type = int(s[0]) 
        s = s[2:len(s)]
        if self.encode_type == 0 or self.encode_type == 1:
            self.key = {}
            p = s.split("||")
            for i in range(0, len(p)):
                k = '\n' if p[i].split("->")[0] == "~" else p[i].split("->")[0]
                v = '\n' if p[i].split("->")[1] == "~" else p[i].split("->")[1]
                self.key.update({ k : v })
        elif self.encode_type == 2:
            self.key = s.split(',')
        else:
            raise StringIsNotAKeyException()
            
    def to_str(self):
        res = str(self.encode_type) + ','
        if self.encode_type == 0 or self.encode_type == 1:
            for i in self.key:    
                k = "~" if _get_key(self.key, i) == '\n' else _get_key(self.key, i)
                v = "~" if i == '\n' else i
                res += v + "->" + k + "||"
            return res[0 : len(res) - 2]
        elif self.encode_type == 2:
            return "2," + ','.join(self.key)

class Encryptor(ABC):
    @abstractmethod
    def Encrypt(self, s, key):
        pass

    @abstractmethod
    def Decrypt(self, s, key):
        pass

    @abstractmethod
    def GenerateKey(self, alph):
        pass

class Replacement(Encryptor): #замены
    def Encrypt(self, s, key):
        if key.encode_type == 0:
            res = "0,"
            for i in range(0, len(s)):
                res += key.key[s[i]]
            return res
        else:
            raise WrongKeyException()

    def Decrypt(self, s, key):
        if s[0] == '0':
            if key.encode_type == 0:
                res = ""
                s = s[2 : len(s)]
                for i in range(0, len(s)):                    
                    res += str(_get_key(key.key, s[i]))
                return res
            else:
                raise WrongKeyException()
        else:
            raise WrongEncryptionException()

    def GenerateKey(self, alph):
        key = "0,"
        a = alph.alphabet[0:len(alph.alphabet)]
        random.shuffle(a)
        for i in range(0, len(alph.alphabet)):            
            key += alph.alphabet[i] + "->" + a[i] + "||"
        key = key[0:len(key)-2]
        return Key(key)

class Transposition(Encryptor): #перестановки
    def Encrypt(self, s, key):
        if key.encode_type == 1:
            h = int(ceil(float(len(s)) / float(len(key.key))))
            w = len(key.key)
            s = s + (' ' * (w*h - len(s)))
            st = []
            for i in range(h):
                st.append([' '] * w)
            l = 0
            for i in range(0, h):
                for j in range(0, w):
                    st[i][j] = s[l]                
                    l += 1 
            res = []
            for i in range(h):
                res.append([' '] * w)            
            for i in range(0, h):
                for j in range(0, w):                    
                    res[i][j] = st[i][int(key.key[str(j)])]
            res_str = "1,"
            for i in range(0, h):
                for j in range(0, w):
                    res_str += res[i][j]
            return res_str
        else:
            raise WrongKeyException()        

    def Decrypt(self, s, key):
        if s[0] == '1':
            if key.encode_type == 1:
                s = s[2 : len(s)]
                h = int(ceil(float(len(s)) / float(len(key.key))))
                w = len(key.key)
                s = s + (' ' * (w*h - len(s)))
                st = []
                for i in range(h):
                    st.append([' '] * w)
                l = 0
                for i in range(0, h):
                    for j in range(0, w):
                        st[i][j] = s[l]                
                        l += 1 
                res = []
                for i in range(h):
                    res.append([' '] * w)            
                for i in range(0, h):
                    for j in range(0, w):                    
                        res[i][int(key.key[str(j)])] = st[i][j]
                res_str = ""
                for i in range(0, h):
                    for j in range(0, w):
                        res_str += res[i][j]
                return res_str
            else:
                raise WrongKeyException()
        else:
            raise WrongEncryptionException()

    def GenerateKey(self, n):
       key = "1,"
       alph = [i for i in range(0, n)]
       a = [i for i in range(0, n)]
       random.shuffle(a)
       for i in range(0, n):
           key += str(alph[i]) + "->" + str(a[i]) + "||"
       key = key[0 : len(key)-2]
       return Key(key)

class Gamming(Encryptor):
    def Decrypt(self, s, key):
        if s[0] == '2':
            if key.encode_type == 2:
                s = s[2 : len(s)]
                st = s.split(',')
                if(len(st) > len(key.key)):
                    n_key = _expand_list(key.key, len(st) - len(key.key))
                else:
                    n_key = key.key 
                res = []
                for i in range(0, len(st)):                    
                    res.append(str(chr((int(st[i]) - int(n_key[i]) + 1103) % 1103)))                    
                return ''.join(res)
            else:
                raise WrongKeyException()
        else:
            raise WrongEncryptionException()

    def Encrypt(self, s, key):
        if key.encode_type == 2:
            if(len(s) > len(key.key)):
                n_key = _expand_list(key.key, len(s) - len(key.key))
            else:
                n_key = key.key            
            res = []
            for i in range(0, len(s)):
                res.append(str((ord(s[i]) + int(n_key[i]) % 1103)))
            return "2," + ','.join(res)
        else:
            raise WrongKeyException()

    def GenerateKey(self, key_size):
        key = "2,"
        for i in range(0, key_size):
            key += str(random.randrange(ord('a'), ord('я') + 1)) + ","
        return Key(key[0 : len(key) - 1])