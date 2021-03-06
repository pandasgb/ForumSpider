import requests
import lxml.html
import pandas as pd
import time


def run(kww):
    # keywords = kww
    # keywordstoutf8 = str(keywords.encode("utf-8"))[1:].replace('\\x','%').replace('\'','').upper()
    keywords = kww
    keywordUrl = get_keywordUrl(keywords)
    df = get_comment(keywordUrl)
    df.to_csv('C:/Users/Administrator/Desktop/oppoForum-'+keywords+'.csv',encoding='utf-8-sig',index=False)


def get_keywordUrl(srchtxt):
    srchtxt = srchtxt
    initUrl = 'https://bbs.coloros.com/search.php?mod=forum'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    initRes = requests.get(initUrl,headers=headers)
    initHtml = lxml.html.fromstring(initRes.text)
    formhash = initHtml.xpath('//input[@name="formhash"]/@value')[0]
    data = {'formhash':formhash,
            'srchtxt':srchtxt,
            'searchsubmit':'yes'}
    searchContentPage = requests.post(initUrl,data=data,headers=headers)
    searchContentPageHtml = lxml.html.fromstring(searchContentPage.text)
    keywordUrl = searchContentPageHtml.xpath('//div[@class="pg"]/a/@href')[0].split('page=')[0]+'page='
    keywordUrl = 'https://bbs.coloros.com/' + keywordUrl
    # print(keywordUrl+str(2))
    return keywordUrl


def get_comment(keywordUrl):
    page = 1
    contentall = []
    while 1:
        time.sleep(0.5)
        url = keywordUrl +str(page)
        # url = 'https://bbs.coloros.com/search.php?mod=forum&searchid=282&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw='+keywordstoutf8+'&page='+str(page)
        # url = 'http://bbs.vivo.com.cn/search.php?mod=forum&srchtxt=' + keywordstoutf8 + '&orderby=lastpost&ascdesc=desc&searchsubmit=yes&page='+str(page)
        # url = 'https://bbs.nubia.cn/search.php?mod=forum&searchid=2938&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw='+ keywordstoutf8+'&page='+str(page)
        page += 1
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        pagecontent = requests.get(url,headers=headers)
        print(url,pagecontent)
        if '没有找到匹配结果' in pagecontent.text:
            print('to the end')
            break
        html = lxml.html.fromstring(pagecontent.text)
        tieList = html.xpath('//ul/li[@class="pbw"]')
        for tie in tieList:
            tid = tie.xpath('./@id')[0]
            tidurl = 'https://bbs.coloros.com/forum.php?mod=viewthread&tid=' + str(tid)
            title = tie.xpath('./h3/a//text()')
            title = ''.join(title)
            check = tie.xpath('./p')[0].xpath('./text()')[0]
            check1 = check.split('-')[0]
            check2 = check.split('-')[1]
            content = tie.xpath('./p')[1].xpath('.//text()') if tie.xpath('./p')[1].xpath('./text()') else ''
            content = ''.join(content).replace('\r\n', '').replace(' ', '')
            frominfo = tie.xpath('./p')[2].xpath('./span//text()')
            fromtime = frominfo[0]
            fromname = frominfo[2]
            frombq = frominfo[4]
            contentall.append([title,check1,check2,content,fromtime,fromname,frombq,tidurl])
            # print(title,check,content,fromtime,fromname,frombq)
    df = pd.DataFrame(contentall,columns=['标题','回复','查看','内容','发帖时间','用户名','板块','链接'])
    return df


if __name__=="__main__":
    kw = '智慧识屏'
    run(kw)
