# coding=utf-8
import re
import time
import random
from copy import deepcopy
from douyin_app.docs.douyin_signature_algorithm import *


base_param = {
        'ac': 'wifi',
        'aid': '1128',
        'app_name': 'aweme',
        'channel': 'aweGW',
        'device_brand': 'HUAWEI',
        'device_platform': 'android',
        'device_type': 'HUAWEI+NXT-AL10',
        'dpi': '480',
        'feed_style': '1',
        'language': 'zh',
        'manifest_version_code': '166',
        'os_api': '23',
        'os_version': '6.0',
        'resolution': '1080*1812',
        'retry_type': 'retry_http',
        'ssmix': 'a',
        'update_version_code': '1662',
        'version_code': '166',
        'version_name': '1.6.6'
    }


def parse(url):
    custom_param = deepcopy(base_param)

    _rticket = int(round(time.time() * 1000))
    ts = int(time.time())

    custom_param['_rticket'] = _rticket
    custom_param['ts'] = ts
    custom_param['device_id'] = random.randint(35000000000, 50000000000)
    custom_param['iid'] = random.randint(20000000000, 35000000000)
    custom_param['openudid'] = ''.join([random.choice(list('0123456789abcdef')) for i in range(16)])
    custom_param['uuid'] = '863' + str(random.randint(200000000000, 350000000000))

    api, necessary_para = re.split(r'\?', url)

    necessary_para_list = necessary_para.split('&')
    for para in necessary_para_list:
        k, v = re.split(r'=', para)
        custom_param[k] = v

    base_url = api + '?' + dict2str(custom_param)

    return base_url, ts


def dict2str(p_dict):
    d2l = []
    for key, value in p_dict.items():
        d2l.append(key + '=' + str(value))
    return '&'.join(d2l)


def generate_douyin_url(base_url):

    base_url, ts = parse(base_url)

    sig = calcSig()
    full_url = sig.work(base_url, ts)

    return full_url


if __name__ == '__main__':
    url = 'https://aweme.snssdk.com/aweme/v1/user/?user_id=74755115308'
    url = generate_douyin_url(url)
    print(url)

