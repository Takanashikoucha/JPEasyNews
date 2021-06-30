# -*- coding: utf8 -*-
# @LastAuthor: TakanashiKoucha
# @Date: 2021-06-30 09:27:46
import os
import re
import time

import fire
import pycurl
from selenium import webdriver

# 创建浏览器对象
driver = webdriver.Safari()

# 设定大小为1280*2048
driver.set_window_size(1280, 2048)

# 使用提示
print('''
    加载网页需要时间，默认预留时间为2s，可按需修改。
    请勿用于违反NHK著作许可的用途！
                    ----Takanashi・Koucha
    ''')

# 更改工作目录
try:
    os.chdir(os.getcwd() + r"/downloads/img")
    os.chdir("..")
    print("工作目录为：  "+os.getcwd())
except Exception as e:
    print("未发现下载目录，开始创建")
    try:
        os.mkdir(os.getcwd() + r"/downloads/")
    except:
        pass
    os.mkdir(os.getcwd() + r"/downloads/img")
    print("新创建下载目录结束")
    os.chdir(os.getcwd() + r"/downloads/")
else:
    print("已存在下载目录")


def download(id=""):
    # 获取网页并等待2s
    driver.get("https://www3.nhk.or.jp/news/easy/" + id + "/" + id + ".html")
    time.sleep(2)
    # 消除注音并找到标题
    driver.find_element_by_xpath(
        '''//*[@id="easy-wrapper"]/div[2]/main/article/div[1]/div[1]/a[2]'''
    ).click()
    title = driver.find_element_by_xpath(
        '''//*[@id="easy-wrapper"]/div[2]/main/article/h1''').text.replace(
            "\n", "")
    print("新闻标题为： " + title)
    # 找到不带注音正文
    content_without_hiragana = driver.find_element_by_xpath(
        '''//*[@id="easy-wrapper"]/div[2]/main/article''')
    os.chdir(os.getcwd() + r"/img")
    content_without_hiragana.screenshot(title + ".png")
    # 添加注音并找到带注音正文
    driver.find_element_by_xpath(
        '''//*[@id="easy-wrapper"]/div[2]/main/article/div[1]/div[1]/a[2]'''
    ).click()
    content_without_hiragana = driver.find_element_by_xpath(
        '''//*[@id="easy-wrapper"]/div[2]/main/article''')
    content_without_hiragana.screenshot("（読み方付き）" + title + ".png")
    print("内容已保存为图片")
    os.chdir("..")
    # 获取m3u8文件
    m3u8_url = "https://nhks-vh.akamaihd.net/i/news/easy/" + id + ".mp4/master.m3u8"
    with open('master.m3u8', 'wb') as f:
        c = pycurl.Curl()
        c.setopt(c.URL, m3u8_url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()
    time.sleep(2)
    src_file = "master.m3u8"
    dst_file = title + ".m3u8"
    try:
        os.rename(src_file, dst_file)
    except Exception as e:
        print(e)
        print("重命名失败")
    else:
        print("重命名成功")
    print("请检查m3u8文件")


def dfl(file):
    i = 0
    with open(file, "r") as file:
        for line in file.readlines():
            i = i + 1
            try:
                line = line.replace("\n", "")
                download(line)
                print("下载成功，当前  " + str(i))
            except:
                print("下载失败，当前  " + str(i))
    # 退出浏览器
    driver.quit()


def genlist():
    driver.get("https://www3.nhk.or.jp/news/easy/")
    time.sleep(2)
    page = driver.page_source
    pattern = re.compile('''k[0-9]{2,}''')
    id_lists = pattern.findall(page)
    id_list = list(set(id_lists))
    print(id_list)
    with open("list.txt", "w+") as file:
        for id in id_list:
            file.write(id + "\r\n")
    # 退出浏览器
    driver.quit()


if __name__ == '__main__':
    fire.Fire()
