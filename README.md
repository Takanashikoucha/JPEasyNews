# JPEasyNews

从HNK简易新闻生成各种语言学习用材料

HNK Easy Newsからさまざまな言語学習教材を生成する

Generate various language learning materials from HNK Easy News

------
## 依赖：
[google-fire](https://github.com/google/python-fire)
[selenium](https://selenium.dev/)
[chromedriver](https://chromedriver.chromium.org/)

------
## 功能：

```bash
# 下载id为xxxxxxxxxxxx的新闻文件到工作目录下的download文件夹下
python ./JPEasyNews.py download --id=xxxxxxxxxxxx
# 从工作目录下的某个文件中按行读取id并下载
python ./JpEasyNews.py dfl filename.txt
# 生成一个首页上所有id的list文件到工作目录下的download文件夹中
python ./JPEasyNews.py genlist
```
