from collections import defaultdict
from importlib.machinery import SourceFileLoader
import base64
import hashlib
import random
import string
import re

class Tools:

    @classmethod
    def dynamicallyImportModule(modulePath, moduleName):
        className = None
        service_module = SourceFileLoader(moduleName, modulePath).load_module()
        if hasattr(service_module, moduleName.capitalize()):
            className = getattr(service_module, moduleName.capitalize())
        return className

    @classmethod
    def md5(cls, s:str):
        return hashlib.md5(s.encode('utf8')).hexdigest()

    @classmethod
    def b64Encode(cls, s:str):
        bytecode = base64.b64encode(s.encode('utf8'))
        return bytecode.decode('utf8')

    @classmethod
    def b64Decode(cls, s:str):
        bytecode = base64.b64decode(s)
        return bytecode.decode('utf8')

    @classmethod
    def randomStr(cls, rang:int=10):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(rang))

    @classmethod
    def emailValidator(cls, email:str):
        isvalid = True
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not EMAIL_REGEX.match(email):
            isvalid = False
        return isvalid

    @classmethod
    def convertDictToStr(cls, row):
        data = defaultdict()
        for key,val in row.items():
            if val is None:
                val = ""
            data[key] = str(val)
        return data

    @classmethod
    def byteArrayToStr(cls, val):
        if isinstance(val, bytearray):
            return val.decode("utf-8", errors="replace")
        else:
            return val