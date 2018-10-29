
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re,os
import time
from pyquery import PyQuery as pq



def get_page(url):      #request获取网页文本，注意网页编码格式

    try:
        headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
            }
        response = requests.get(url=url, headers=headers)

        """
        if response.status_code == 200:
            return response.content

        return None
        """
        if response.status_code == 200:
            global encode_content
            encode_content = response.text
            # =======================================
            if response.encoding == 'ISO-8859-1':
                encodings = requests.utils.get_encodings_from_content(response.text)
                if encodings:
                    encoding = encodings[0]
                else:
                    encoding = response.apparent_encoding

                # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
                encode_content = response.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符
            return encode_content
        return None
    except RequestException:
        return None


def get_img(url):   #访问图片页面，写文件时要用byte类型，所以网页返回content

    try:
        headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
            }
        response = requests.get(url=url, headers=headers)


        if response.status_code == 200:
            return response.content

        return None
    except RequestException:
        return None

def get_image(items):     #解析各个标题下的二级网页
    url_2="https://m.hupu.com/bbs/"+str(items[0])
    print(url_2)

    html_2 = get_page(url_2)
    #print(html_2)
    #return html_2
    doc = pq(html_2)
    items_ = doc('.article-content img')  #pyquery解析class=article-content下的img标签
    arr=[]
    for item_ in items_.items():  #对每个img标签返回src属性值并保存到数组中
        item_=item_.attr('src')
        #print(item_)
        #
        arr.append(item_)
    #print(arr)
    return arr,url_2



def soup():  #定义主函数
    url = "https://bbs.hupu.com/selfie"
    html = get_page(url)
    soup=BeautifulSoup(html,"lxml")   #beautiful解析div标签下的class=truetit内容
    items=soup.select('div .truetit')
    #print(items)
    if not os.path.exists('image'):   #创建image文件夹用来保存图片
        os.mkdir('image')
    for i in items[1:]:
        i=str(i)
        pattern_1=re.compile('href="/(.*?)"')  #正则表达式解析图片地址
        item_1=re.findall(pattern_1,i)

        pattern_2=re.compile('[\u4e00-\u9fa5]')#正则表达式解析标题
        item_2 = re.findall(pattern_2, i)
        title="".join(item_2)
        print(title)
        path=os.path.abspath('.')+'/'+"/image/"+title #在image目录下根据标题创建二级目录

        if not os.path.exists(path):
            os.mkdir(path)

        # print(item_1)
        # print(type(item_1))
        # a=get_image(item_1)
        # print(a)
        # write_to_file(a)
        a,b = get_image(item_1)
        print(a)
        count = 1
        print(str(b) + "共有" + str(len(a)) + "张图片")
        if len(a)==0:
            print("该页面没有图片")
        for img_url in a:
            if len(a)!=0:
                img = get_img(img_url)

                if img_url[-3:] == 'jpg':
                    if not os.path.exists(path):

                        with open(path+"/"+str(count)+".jpg",'wb') as f:
                            f.write(img)
                else:
                    if not os.path.exists(path):
                        with open(path+"/"+str(count)+"."+img_url[-3:],'wb') as f:
                            f.write(img)

                print("正在从"+title+"下载第"+str(count)+"张图片")

                count=count+1
                time.sleep(1)
        print("=====================================================")
        print()



if __name__ == '__main__':
    soup()
    time.sleep(10)

