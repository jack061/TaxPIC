import random
import requests

class Downloader:
    '''
    下载器, 输入请求url,下载器进行请求，返回请求的数据
    '''

    def request_data_from_url(self, url, method='get', post_data= {}, referer = None, user_agent = None, other_headers = {}, timeout = -1):

        ip = '%d.%d.%d.%d' % (random.choice(range(100,244)),random.choice(range(100,244)),random.choice(range(100,244)),random.choice(range(100,244)))

        if url.find("//") == 0:
            #没有标识协议，加http 协议标识
            url = 'http:' + url

        # 开始构造headers
        headers = {'X-Forwarded-For':ip}
        if user_agent: headers['User-Agent'] = user_agent
        if referer: headers['RefererAgent'] = referer
        headers.update(other_headers)


        if method == 'get':
            req = requests.get(url, headers=headers, verify=False, timeout=timeout if timeout > 0 else 1)
        else:
            req = requests.post(url, data=post_data, headers=headers, verify=False, timeout=timeout if timeout > 0 else 1)

        data = req.text
        return data

