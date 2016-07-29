#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pyquery import PyQuery as pq
import requests
import codecs
import json
import time
import datetime
import urllib
#translate timestamp to normal date format
def ttd(timestamp):
    timeStr=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    return timeStr
f=codecs.open('/home/allen/projects/sjtu_news/data_wechat_primary.csv','w','utf-8')
fs=codecs.open('/home/allen/projects/sjtu_news/data_wechat_secondary.csv','w','utf-8')
url_initial='https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzAxNTE2MjgyNw==&uin=MjMzNTA3MjQw&key=8dcebf9e179c9f3af3efdc3f2d9ce1996e5e140509deeb3ee66fc13cb5c71843ee3c7098c5355e04a0a1eb82fbe4b232&f=json&frommsgid=1000000037&count=10&uin=MjMzNTA3MjQw&key=8dcebf9e179c9f3af3efdc3f2d9ce1996e5e140509deeb3ee66fc13cb5c71843ee3c7098c5355e04a0a1eb82fbe4b232&pass_ticket=wIn111ZTF4N%25252Fx%25252F5Jt1dpN%25252BWKZIoKV4cmop0CfCLf7Bo%25253D&wxtoken=&x5=0'
url_head=url_initial[0:url_initial.index('frommsgid=')+len('frommsgid=')]
url_tail=url_initial[url_initial.index('&count='):]
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17"}
def get_counts(url):
    data=data={'article_url': url}
    counts=requests.get('http://localhost/wechat/demo.php?'+urllib.urlencode(data))
    counts=json.loads(counts.text)
    return counts
def run(url_initial):
    page=requests.get(url_initial)
    page.encoding='utf-8'
    page_json=json.loads(page.text)
    general_msg_list=page_json['general_msg_list']
    general_msg_list=json.loads(general_msg_list)
    lists=general_msg_list['list']
    list_length=len(lists)
    try:
        last_id=general_msg_list['list'][9]['comm_msg_info']['id']
    except:
        print "this must be the final set"
        last_id=-1
    hrefs=[general_msg_list['list'][i]['app_msg_ext_info']['content_url'].replace('amp;','') for i in range(list_length)]
    main_title=[]
    for i in range(list_length):
        try:
            main_title.append(general_msg_list['list'][i]['app_msg_ext_info']['title'])
        except:
            main_title.append(general_msg_list['list'][i]['comm_msg_info']['content'])
    datetime=[general_msg_list['list'][i]['comm_msg_info']['datetime'] for i in range(list_length)]
    multi_msg=[]
    for i in range(list_length):
        try:
            multi_msg.append(general_msg_list['list'][i]['app_msg_ext_info']['multi_app_msg_item_list'])
        except:
            multi_msg.append([])
    #print to file_primary
    for i in range(list_length):
        try:
            f.write(str(ttd(datetime[i]))+'\t')
            f.write(main_title[i].replace('\t',' ').replace('&quot','"')+'\t')
            f.write(hrefs[i]+'\t')
            counts=get_counts(hrefs[i])
            f.write(str(counts['data']['read_num'])+'\t'+str(counts['data']['like_num'])+'\t'+str(counts['data']['real_read_num'])+'\t')
        except Exception as e:
            print e
            f.write('\n')
        finally:
            f.write('\n')
    #print to file_secondary
    nt=0
    for j in multi_msg:
        time=str(ttd(datetime[nt]))
        for k in j:
            try:
                fs.write(time+'\t')
                fs.write(k['title'].replace('\t',' ').replace('&quot','’')+'\t')
                url=k['content_url'].replace('amp;','')
                fs.write(url+'\t')
                counts=get_counts(url)
                fs.write(str(counts['data']['read_num'])+'\t'+str(counts['data']['like_num'])+'\t'+str(counts['data']['real_read_num'])+'\t')
            except Exception as e:
                print e
                fs.write('\n')
            finally:
                fs.write('\n')
    return last_id

for i in range(2000):
        rv=run(url_initial)
        if rv!=-1:
            print rv
        else:
            print 'finished'
            exit()
        time.sleep(5)
        url_initial=url_head+str(rv)+url_tail
