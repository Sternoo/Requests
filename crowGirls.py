import requests
import re
import os
import time


headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}


def generateParameters(target_index):
    """生成请求参数"""
    para = {
        'append': 'list-home',
        'paged': target_index,
        'action': 'ajax_load_posts',
        'query': '',
        'page': 'home'
    }
    return para


def requestHTML(target_url):
    """请求网页"""
    print(target_url)
    response = requests.get(target_url, headers=headers, verify=False)
    res_html = response.text
    return res_html


def parseHTML(target_html):
    """解析网页"""
    titles = re.findall('<h1 class="post-title h3">(.*?)</h1>', target_html)
    if len(titles) > 0:
        title = titles[-1]
    else:
        title = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    res_dir_name = 'girls_pic/' + title
    if not os.path.exists(res_dir_name):
        os.mkdir(res_dir_name)

    res_urls = re.findall('<a href="(.*?)" alt=".*?" title=".*?">', target_html)
    print(res_urls)
    return res_dir_name, res_urls


def savePic(target_dir_name, target_urls):
    """保存图片"""
    for target_url in target_urls:
        # 图片的名字
        file_name = target_dir_name + '/' + target_url.split('/')[-1]
        if not os.path.exists(file_name):
            response = requests.get(target_url, headers=headers)
            with open(file_name, 'wb') as f:
                f.write(response.content)
                print(f'\r保存{file_name}成功', end='')
    # 换行
    print()


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    requests.adapters.DEFAULT_RETRIES = 5
    requestUrl = 'https://www.vmgirls.com/wp-admin/admin-ajax.php'
    for index in range(11, 50):
        print(f'index{index}')
        res = requests.post(requestUrl, data=generateParameters(index), headers=headers)
        urls = re.findall('<a href="(.*?)" class="list-title text-md h-2x" target="_blank">', res.text)
        for url in urls:
            html = requestHTML(url)
            dir_name, urls = parseHTML(html)
            savePic(dir_name, urls)
            nav_links = re.findall('<a href="(.*?)" class="post-page-numbers">.*?</a>', html)
            for link in nav_links:
                html = requestHTML(link)
                dir_name, urls = parseHTML(html)
                savePic(dir_name, urls)

