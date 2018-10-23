from settings import PROXY_PATH
import random

def getProxy():
    proxy_file_path = PROXY_PATH
    with open(proxy_file_path) as proxy_file:
        proxies = proxy_file.readlines()
    for i in range(len(proxies)):
        proxies[i] = proxies[i].strip('\n')
    return proxies

if __name__ == '__main__':
    p= getProxy()
    proxy = random.choice(p)

    print(proxy)