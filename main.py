import os
import util
from util import logger
from weibo2 import Weibo
import datetime  # 新增，用于处理日期相关操作
import requests
import json
import re
import time

def fasong(cont):
    #print(cont)
    pattern = r'\[(.*?)\]'
    # 使用findall方法查找所有匹配的内容
    matches = re.findall(pattern, cont)
    extracted_texts_newline_separated = "\n".join(matches)


    post_data = {
        'msgtype': 'text',
        'text': {
            "content":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"微博新增实时上升热搜"+"\n"+"每15分钟更新"+"\n"+"\n"+extracted_texts_newline_separated
        }}
    headers = {
        'Content-Type': 'application/json'
    }
    url = 'https://oapi.dingtalk.com/robot/send?access_token=c444192bb30e622f728047fe04421e58511082af4a6b27ea6412636247b2013a'
    respnse = requests.post(url, headers=headers, data=json.dumps(post_data))
    print(post_data)
    
def generate_archive_md(searches):
    """生成归档readme"""
    def search(item):
        return '1. [{}]'.format(item['desc'])

    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    readme = ''
    file = os.path.join('template', 'archive.md')
    with open(file) as f:
        readme = f.read()

    readme = readme.replace("{updateTime}", util.current_time())
    readme = readme.replace("{searches}", searchMd)
    return readme


def generate_readme(searches):
    """生成今日readme"""
    def search(item):
        return '1. [{}]'.format(item['desc'])

    searchMd = '暂无数据'
    if searches:
        searchMd = '\n'.join([search(item) for item in searches])

    readme = ''
    file = os.path.join('template', 'README.md')
    with open(file) as f:
        readme = f.read()

    readme = readme.replace("{updateTime}", util.current_time())
    readme = readme.replace("{searches}", searchMd)

    return readme
   

def save_readme(md):
    logger.debug('readme:%s', md)
    util.write_text('README.md', md)


def save_archive_md(md):
    logger.debug('archive md:%s', md)
    name = '{}.md'.format(util.current_date())
    file = os.path.join('archives', name)
    util.write_text(file, md)


def save_raw_content(content: str, filePrefix: str):
    filename = '{}-{}.json'.format(filePrefix, util.current_date())
    file = os.path.join('raw', filename)
    util.write_text(file, content)


def run():
    weibo = Weibo()
    # 热搜
    searches, resp = weibo.get_hot_search()
    #print(resp)
    if resp:
        save_raw_content(resp.text, 'hot-search')
        

    # 判断当天的README.md是否已存在，若存在则读取已有内容
    readme_exist = os.path.exists('README.md')
    existing_readme_content = ''
    if readme_exist:
        with open('README.md', 'r') as f:
            existing_readme_content = f.read()

    # 处理新获取内容与已有内容的去重合并（这里简单示例去重逻辑，假设searches是列表，里面元素可哈希，实际可能需根据具体数据结构调整）
    new_search_items = []
    if existing_readme_content:
        existing_search_items = [line.strip() for line in existing_readme_content.split('\n') if line.strip().startswith('1. [')]
        for search_item in searches:
   
            search_str = '1. [{}]'.format(search_item['desc'])#需要注意 每次的链接不一样！！
            if search_str not in existing_search_items:
                new_search_items.append(search_item)
    else:
        new_search_items = searches

    # 生成更新后的readme内容
    readme = generate_readme(new_search_items)
    fasong(readme) 

    save_readme(readme)
    

    # 判断当天的归档文件是否已存在，若存在则读取已有内容
    archive_exist = os.path.exists(os.path.join('archives', '{}.md'.format(util.current_date())))
    existing_archive_content = ''
    if archive_exist:
        with open(os.path.join('archives', '{}.md'.format(util.current_date())), 'r') as f:
            existing_archive_content = f.read()

    # 处理新获取内容与已有归档内容的去重合并（同理，这里也是简单示例去重逻辑，可能需按实际调整）
    new_archive_search_items = []
    if existing_archive_content:
        existing_archive_search_items = [line.strip() for line in existing_archive_content.split('\n') if line.strip().startswith('1. [')]
        for search_item in searches:
            print(searches)
            search_str = '1. [{}]'.format(search_item['desc'])
            if search_str not in existing_archive_search_items:
                #print(search_item)
                new_archive_search_items.append(search_item)
    else:
        new_archive_search_items = searches

    # 生成更新后的归档md内容
    archiveMd = generate_archive_md(new_archive_search_items)
    save_archive_md(archiveMd)
    



if __name__ == "__main__":
    run()
    
