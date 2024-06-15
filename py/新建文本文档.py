import time
import requests
from fake_useragent import UserAgent

pages = int(input('请输入你想爬取的页数:'))
ua = UserAgent()
user_agent = ua.random
headers = {
    'User-Agent': user_agent
}

for i in range(pages):

    url = f"https://movie.douban.com/j/chart/top_list?type=19&interval_id=100%3A90&action=&start={i*20}&limit=20"

    response = requests.get(url, headers=headers)
    json_data = response.json()

    for json in json_data:

        with open(f'Li.json','a',encoding='utf-8') as f:
            f.write(str(json) + ',\n')

    print(f'第{i+1}页数据下载成功')
    time.sleep(3)