import re
import aiohttp
import json
import asyncio
import time


async def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
    async with aiohttp.ClientSession() as session:
       async with session.get(url, headers=headers) as response:
            print('开始请求网页：{}'.format(url))
            res = await response.text()
            return res


def parse_one_page(html):  #正则解析网页
    pattern = re.compile(r'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern, html)
    for item in items:
        print({
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
            })


if __name__ == '__main__':
    start_time = time.time()
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(get_page('https://maoyan.com/board/4?offset={}'.format(str(i*10)))) for i in range(11)]
    loop.run_until_complete(asyncio.wait(tasks))
    for t in tasks:
        parse_one_page(t.result())
    loop.close()
    end_time = time.time()
    print('共花费时间：{}'.format(end_time-start_time))
