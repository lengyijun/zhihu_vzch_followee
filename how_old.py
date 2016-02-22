# -*- coding: utf-8 -*-
import  requests

if __name__ == '__main__':
    s=requests.session()
    url='http://how-old.net/Home/Analyze?isTest=False&source=&version=001'
    header = {
        'Accept-Encoding':'gzip, deflate',
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
        'Host': "how-old.net",
        'Referer': "http://how-old.net/",
        'X-Requested-With': "XMLHttpRequest"
    }

    data={
        'file':open(r'c:\Users\steven\PycharmProjects\zhihu\follower\Yvonne Lu.jpg','rb')
    }

    r=s.post(url,headers=header,data=data)
    h=r.content
    print(h)