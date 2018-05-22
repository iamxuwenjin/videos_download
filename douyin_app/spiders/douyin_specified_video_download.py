# -*- coding: utf-8 -*-
import re
import json
from scrapy import Spider
from scrapy.http import Request
from douyin_app.docs.conf import HEADER


class DouyinSpecifiedVideoSpider(Spider):
    name = "specified_douyin_video"
    video_url = ''
    download_url = 'https://api.amemv.com/aweme/v1/play/?video_id={}&line=1&ratio=720p&media_type=4&vr_type=0&test_cdn=None&improve_bitrate=0'

    def __init__(self, url):
        super(DouyinSpecifiedVideoSpider, self).__init__()
        self.video_url = url

    def start_requests(self):
        url = self.video_url
        header = HEADER
        yield Request(url=url, headers=header, callback=self.get_uri)

    def start_get_video(self, uri, desc):
        url = self.download_url.format(uri)
        header = HEADER
        return Request(url=url, headers=header, callback=self.get_video, meta={'desc': desc})

    def get_uri(self, response):
        response_content = response.body.decode('utf-8')
        try:
            content = re.findall(r'data = \[(.*)?\];', response_content)[0]
        except Exception:
            content = ''
            self.logger.error('解析不到视频信息,,Ծ‸Ծ,,')
        if content:
            json_data = json.loads(content)
            uri = json_data.get('video').get('play_addr').get('uri')
            self.logger.info('解析到视频参数{}(•‾̑⌣‾̑•)✧˖°', format(uri))
            video_desc = json_data.get('desc')[0:10]
            yield self.start_get_video(uri=uri, desc=video_desc)

    def get_video(self, response):
        desc = response.meta.get('desc')
        content = response.body
        with open('./douyin_app/videos/{}.mp4'.format(desc), 'wb') as f:
            f.write(content)
        self.logger.info('下载完成๑乛◡乛๑')
