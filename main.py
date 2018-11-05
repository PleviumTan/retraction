import re
import requests
import bs4
import json

alist = []
path = 'r1.html'
f = open(path, 'r', encoding = 'utf-8')
htmlFile = f.read()


soup = bs4.BeautifulSoup(htmlFile,'html.parser')
#(soup.prettify())
alist
for tr in soup.find(id = 'grdRetraction').children:
    if isinstance(tr,bs4.element.Tag):
        tmpdict = {}
        #檢測tr的類型 如果不是tag，過濾掉
        tds = tr('td')
        #提取文档编号
        tmpdict['num'] = tds[0].string
        #提取文档标题
        tmpdict['title'] = tds[1].find('span','rTitle').string
        alist.append(tmpdict)
        #提取文档主题词
        subject = tds[1].find('span','rSubject').string.strip().split(';')
        tmpdict['subject'] = [sub for sub in subject if sub ]
        #提取期刊名
        journal = tds[1].find('span','rJournal')
        journalname = journal.find('span','rJournal').string
        journalname = re.sub('---','',journalname)#换掉 ---
        tmpdict['journalname'] = journalname
        tmpdict['journalpublisher'] = journal.find('span','rPublisher').string
        #提取机构名
        institutions = tds[1].find_all('span','rInstitution')
        tmpdict['institution'] = [re.sub('\n','',ins.string) for ins in institutions if ins.string ]
        #提取原因名
        reasons = tds[2].find_all('div','rReason')
        tmpdict['reason'] = [reason.string for reason in reasons if reason.string ]
        #提取作者名
        authors = tds[3].find_all('a','authorLink')
        tmpdict['author'] = [au.string for au in authors if au.string ]

#for article in alist:
    #print(article)

with open('testOutPut.json', 'w') as f:
    f.write(json.dumps(alist))

