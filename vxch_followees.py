# -*- coding: utf-8 -*-
from XVThumbImagePlugin import r
import requests, os
import json
import time
from bs4 import BeautifulSoup

# 去掉了cookie
from six import u

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.zhihu.com',
    'Origin': 'https://www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
raw_cookie_get = None
r_vxch_cookie = None

def login_get_cookie():
    global raw_cookie_get
    global r_vxch_cookie
    url = "https://www.zhihu.com/#signin"
    zhihu_mail = "http://www.zhihu.com/login/email"

    zhihu_main = BeautifulSoup(requests.get(url).content)
    xsrf = zhihu_main.find("input", {"name": "_xsrf"}).get("value")

    post_data = {
        '_xsrf': xsrf,
        'password': 'tantrum123',
        'remember_me': 'true',
        'email': 'qb20110427@163.com',
    }

    r = requests.post(zhihu_mail, headers=headers, data=post_data)
    print(r.headers)
    raw_cookie_get = r.headers['Set-Cookie']
    headers['Cookie'] = raw_cookie_get

def download_img(img_src, name):
    img_src = img_src[:-5] + "b" + img_src[-4:]
    print(img_src)
    with open("./follower/" + name + img_src[-4:], "wb") as f:
        f.write(requests.get(img_src).content)

def get_ajax(i, vzch_xsrf):
    global raw_cookie_get
    global r_vxch_cookie
    ajax_post_data = {
        'method': 'next',
        'params': json.dumps({"offset": 20 * i, "order_by": "created", "hash_id": "0970f947b898ecc0ec035f9126dd4e08"}),
        '_xsrf': '',
    }

    ajax_header = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.zhihu.com',
        'Origin': 'https://www.zhihu.com',
        'Referer': 'https://www.zhihu.com/people/excited-vczh/followees',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',

    }
    ajax_post_data['_xsrf'] = vzch_xsrf
    ajax_header['Cookie'] = r_vxch_cookie + ";" + raw_cookie_get

    req = requests.Session().post("https://www.zhihu.com/node/ProfileFolloweesListV2", data=ajax_post_data,
                                  headers=ajax_header)
    # 此处花了我好久才搞定
    data_follow = json.loads(req.text)['msg']
    for i in data_follow:
        i = BeautifulSoup(i)
        img_src = i.find("img").get("src")
        name = i.find("a").get("title")
        download_img(img_src, name)

def vxch_follower_main_page():
    global raw_cookie_get
    global r_vxch_cookie
    r_vxch = requests.get("https://www.zhihu.com/people/excited-vczh/followees", headers=headers)
    r_test = r_vxch.content
    r_vxch_cookie = r_vxch.headers['Set-Cookie']
    vzch_content = BeautifulSoup(r_test)
    follower_list = vzch_content.find_all("a", {"class": "zm-item-link-avatar"})
    vzch_xsrf = vzch_content.find("input", {"name": "_xsrf"}).get("value")

    for i in follower_list:
        name = i.get("title")
        img_src = str(i.find("img").get("src"))
        download_img(img_src, name)

    for i in range(1, 80):
        get_ajax(i, vzch_xsrf)
        time.sleep(1)

if __name__ == '__main__':
    try:
        os.mkdir("./follower")
    except:
        pass

    login_get_cookie()
    vxch_follower_main_page()
