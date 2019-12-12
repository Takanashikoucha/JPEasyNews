# -*- coding: UTF-8 -*-
# @LastAuthor: TakanashiKoucha
# @Date: 2019-12-12 18:48:22
import os
import time

import fire
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# 创建chrome启动选项
chrome_options = webdriver.ChromeOptions()

# 指定chrome启动类型为headless 并且禁用gpu
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("log-level=3")
prefs = {
    'profile.default_content_settings.popups': 0,
    'download.default_directory': os.getcwd() + "\\download\\"
}
chrome_options.add_experimental_option('prefs', prefs)

# 调用环境变量指定的chrome浏览器创建浏览器对象
driver = webdriver.Chrome(chrome_options=chrome_options)

# 设定大小为1280*2048
driver.set_window_size(1280, 2048)

# 更改工作目录
try:
    os.chdir(os.getcwd() + "\\download\\")
except Exception as e:
    print(e)
    os.mkdir(os.getcwd() + "\\download\\")
    print("新创建下载目录")
    os.chdir(os.getcwd() + "\\download\\")
else:
    print("已存在下载目录")


def download(id=""):
    # 使用提示
    print('''
        加载网页需要时间，默认预留时间为2s，可按需修改。
        请勿用于违反NHK著作许可的用途！
                        ----Takanashi・Koucha
        ''')
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
    content_without_hiragana.screenshot(title + ".png")
    # 添加注音并找到带注音正文
    driver.find_element_by_xpath(
        '''//*[@id="easy-wrapper"]/div[2]/main/article/div[1]/div[1]/a[2]'''
    ).click()
    content_without_hiragana = driver.find_element_by_xpath(
        '''//*[@id="easy-wrapper"]/div[2]/main/article''')
    content_without_hiragana.screenshot("（読み方付き）" + title + ".png")
    print("内容已保存为图片")
    # 获取m3u8文件
    m3u8_url = "https://nhks-vh.akamaihd.net/i/news/easy/" + id + ".mp4/master.m3u8"
    driver.get(m3u8_url)
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


if __name__ == '__main__':
    fire.Fire(download)
    #退出浏览器
    driver.quit()
