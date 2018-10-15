import random
import string

def getASCIIRandomStr( length):
    s = string.ascii_letters + string.digits
    s =  s*int(length/len(s)+1)
    return ''.join(random.sample((s), length))

def getLittleHexRandomStr(length):
    s = 'abcdef' + string.digits
    s = s*(length/len(s)+1)
    return ''.join(random.sample((s), length))

def getNumRandomStr(length):
    return ''.join(random.sample(string.digits*int(length/10+1), length))

def getFloatRandom(min=0, max=1):
    return random.uniform(min, max)

if __name__ == '__main__':
    print (getASCIIRandomStr(32))
    print (getNumRandomStr(131))
    print (getFloatRandom())