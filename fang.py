# -*- coding: utf-8 -*-
import requests,MySQLdb,re
from bs4 import BeautifulSoup

BASE_URLS =[
    "http://shanghai.anjuke.com/community/W0QQpZ"
]


HOST = '127.0.0.1'
USER = 'root'
PASSWD = '811107'
DB = 'hfhfs'
PORT = 3306
#xiaoqu_count,xiaoqu_add_count
xqc = 0
xqac = 0
#xiaoqumain_count,xiaoqumain_add_count
xqmc = 0
xqmad = 0
result = []

#for url in BASE_URLS :
#	print url
conn = MySQLdb.connect(HOST,USER,PASSWD,DB,PORT)
conn.set_character_set('utf8')

cur = conn.cursor()
cur.execute('SET NAMES utf8')
cur.execute('SET CHARACTER SET utf8')
cur.execute('set character_set_connection=utf8')

def get_detail ( url ):
	result = []
	print url
	detailReq = requests.get(url)
	detailSoup = BeautifulSoup(detailReq.text)
	xqName = detailSoup.find("div","comm-cont").find("h1")
	#print xqName.get_text()
	#xqDetail = detailSoup.find("div","comm-list").findAll("dt")
	#print type(xqDetail)
	xqDetail = detailSoup.find("div","comm-list").findAll("dd")
	i = 0
	result.append(url)
	result.append(re.findall(r'view/\w+',url)[0])
	for a in xqDetail :
		if i in (0,1,2,5,8,9) :
			result.append(a.get_text())
		i = i + 1
	print result
	arealist = result(3).split(" ")
	for area in arealist :
		result.append(area)
	del result[3]
	for r in result :
		print r
		#elif i == 
		#print a.get_text()

for url in BASE_URLS :
	listReq = requests.get(url)
	listSoup = BeautifulSoup(listReq.text)
	xqlist = listSoup.findAll(id = re.compile("comm_name_qt_apf_id\d*"))
	for xq in xqlist :
		name = xq.get_text()
		url = xq.get('href')
		get_detail ( url )
		#try:
		#	n = cur.execute('select * from xiaoqu where url =  \'%s\''%url)
		#	#not found xiaoqu data
		#	if n == 0 :
		#		xqac = xqac + 1
		#		sql = "insert into xiaoqu(name,url,create_date) values ('%s','%s',now())"%(name,url)
		#		#print sql
		#		cur.execute(sql)
		#		conn.commit()
		#	else :
		#		print "find data %s:%s"%(name,url)
		#except Exception,e:
		#	print str(e)
		#	conn.rollback()
print "-------------find xiaoqu : %s" % xqc + "       add xiaoqu: %s -------------" % xqac
