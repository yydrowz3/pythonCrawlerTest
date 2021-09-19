import random
import re
import time
from lxml import etree
import bs4
import requests
from urllib.parse import urljoin

PATTERN = re.compile(r'<a[^>]*?>\s*<span class="title">(.*?)</span>')


def regex_find():
    for page in range(10):
        resp = requests.get(
            url=f'https://movie.douban.com/top250?start={page * 25}',
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/83.0.4103.97 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;'
                          'q=0.9,image/webp,image/apng,*/*;'
                          'q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            },
        )
        items = PATTERN.findall(resp.text)
        for item in items:
            print(item)
        time.sleep(random.randint(1, 5))


def xPath_find():
    for page in range(10):
        resp = requests.get(
            url=f'https://movie.douban.com/top250?start={page * 25}',
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/83.0.4103.97 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;'
                          'q=0.9,image/webp,image/apng,*/*;'
                          'q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
        )
        html = etree.HTML(resp.text)
        spans = html.xpath('/html/body/div[3]/div[1]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]')
        for span in spans:
            print(span.text)


def bs_find1():
    for page in range(10):
        resp = requests.get(
            url=f'https://movie.douban.com/top250?start={page * 25}',
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/83.0.4103.97 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;'
                          'q=0.9,image/webp,image/apng,*/*;'
                          'q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            },
        )
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        elements = soup.select('.info>div>a')
        for element in elements:
            span = element.select_one('.title')
            print(span.text)
        time.sleep(random.random() * 5)


def bs_find2():
    headers = {'user-agent': 'Baiduspider'}
    base_url = 'https://www.zhihu.com/'
    resp = requests.get(urljoin(base_url, 'explore'), headers=headers)
    soup = bs4.BeautifulSoup(resp.text, 'lxml')
    href_regex = re.compile(r'^/question')
    links_set = set()
    for a_tag in soup.find_all('a', {'href': href_regex}):
        if 'href' in a_tag.attrs:
            href = a_tag.attrs['href']
            full_url = urljoin(base_url, href)
            links_set.add(full_url)
    print('Total %d question pages found.' % len(links_set))
    print(links_set)


def main():
    # regex_find()
    # xPath_find()
    # bs_find1()
    bs_find2()


if __name__ == '__main__':
    main()
