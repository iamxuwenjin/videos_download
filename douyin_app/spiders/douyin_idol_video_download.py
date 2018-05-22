# -*- coding: utf-8 -*-
"""
无签名版本
"""
import re
import json
from scrapy import Spider
from scrapy.http import Request
from douyin_app.docs.conf import HEADER


class DouyinIdolVideoSpider(Spider):
    name = "idol_douyin_video"

    idol_url = ''
    video_list_url = 'https://api.amemv.com/aweme/v1/aweme/post/?user_id={}&max_cursor={}&count=20&device_id=39681429254&ac=wifi&channel=xiaomi&aid=1128&app_name=aweme'

    max_cursor = 0
    uid = None

    def __init__(self, url):
        super(DouyinIdolVideoSpider, self).__init__()
        self.idol_url = url

    def start_requests(self):
        try:
            self.uid = re.findall(r'user/(\d+)', self.idol_url)[0]
            self.logger.info('解析到idol信息{}(•‾̑⌣‾̑•)✧˖°', format(self.uid))
            yield self.start_get_video_list(self.uid)
        except Exception:
            self.logger.error('解析不到视频信息,,Ծ‸Ծ,,')

    def start_get_video_list(self, uid):
        url = self.video_list_url.format(uid, self.max_cursor)
        header = HEADER
        return Request(url=url, headers=header, callback=self.get_video_list)

    def start_get_video(self, url, desc):
        url = url
        header = HEADER
        return Request(url=url, headers=header, callback=self.get_video, meta={'desc': desc})

    def get_video_list(self, response):
        content = response.body.decode('utf-8')
        content = json.loads(content)
        video_list = content.get('aweme_list')
        if video_list:
            for video in video_list:
                download_url = video.get('video').get('play_addr_lowbr').get('url_list')[0]
                desc = video.get('desc')
                self.logger.info('解析到下载链接()(•‾̑⌣‾̑•)✧˖°', format(download_url))
                yield self.start_get_video(download_url, desc)
        if content.get('has_more'):
            self.max_cursor = content.get('max_cursor')
            yield self.start_get_video_list(self.uid)

    def get_video(self, response):
        desc = response.meta.get('desc')
        content = response.body
        with open('./douyin_app/videos/{}.mp4'.format(desc), 'wb') as f:
            f.write(content)
        self.logger.info('下载完成๑乛◡乛๑')
