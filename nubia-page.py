import requests
import lxml.html
import pandas as pd
import re

def run():
    initurl = 'https://bbs.nubia.cn/forum-795-1.html'
    fid = initurl.split('-')[1]
    tidlist = get_tidlist(fid)
    contentall = []
    for tid in tidlist:
        content = get_tie_page(tid)
        contentall.append(content)
    cdf = pd.DataFrame(contentall,columns=['标题','作者','发布时间','回答数','观看人数','内容','地址'])
    cdf.to_csv('C:/Users/Administrator/Desktop/nubiaforum-'+fid+'.csv',encoding='utf-8-sig',index=False)


def get_tidlist(fid):
    page = 1
    tidlist = []
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
    pagelast = 2
    while 1:
        if page > pagelast:
            break
        fpage = 'https://bbs.nubia.cn/forum-'+fid+'-'+str(page)+'.html'

        r = requests.get(fpage,headers=headers)
        print('getting',fpage,r)
        html = lxml.html.fromstring(r.text)
        tids = html.xpath('//tbody[starts-with(@id,"normalthread")]/@id')
        tidid = [x.split('_')[-1] for x in tids]
        tidlist.extend(tidid) if tidid else None
        if page == 1:
            regex = re.compile('\d+')
            pagelast = html.xpath('//div[@class="pg"]/label/text()')[0].strip()
            pagelast = int(re.search(regex,pagelast).group())
            print('lastpage=',pagelast)

        page += 1
    return tidlist


def get_tie_page(tid):
    tid = tid
    pageurl = 'https://bbs.nubia.cn/thread-'+str(tid)+'-1-1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    r2 = requests.get(pageurl, headers=headers)
    print('getting', pageurl, r2)
    html2 = lxml.html.fromstring(r2.text)
    lzt = html2.xpath('//div[@id="sin_post_lz"]')[0]
    title = ''.join(lzt.xpath('.//div[@class="sin_lz_title"]/h1/a/text()'))
    author = ''.join(lzt.xpath('.//div[@class="sin_title_line"]/li[@class="sin_title_icon"]/span')[0].xpath('.//text()')).replace('\r\n','').replace('/','')
    if lzt.xpath('.//div[@class="sin_title_line"]/li[@class="sin_title_icon"]/span')[1].xpath('./span/@title'):

        ttime = lzt.xpath('.//div[@class="sin_title_line"]/li[@class="sin_title_icon"]/span')[1].xpath('./span/@title')[0]
    else:
        ttime = lzt.xpath('.//div[@class="sin_title_line"]/li[@class="sin_title_icon"]/span')[1].xpath('./text()')[0]
    tans = lzt.xpath('.//div[@class="sin_title_line"]/li[@class="sin_title_icon"]/span')[2].xpath('./text()')[0]
    tlook = lzt.xpath('.//div[@class="sin_title_line"]/li[@class="sin_title_icon"]/span')[3].xpath('./text()')[0]
    content = ''.join(lzt.xpath('.//td[@class="t_f"]//text()')).strip().replace('\r\n','').replace(' ','') if lzt.xpath('.//td[@class="t_f"]/text()') else ''
    # print([title,author,ttime,tans,tlook,content])
    return [title,author,ttime,tans,tlook,content,pageurl]


run()
