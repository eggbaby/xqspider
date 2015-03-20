# -*- coding: utf-8 -*-
import requests,MySQLdb,sys
from bs4 import BeautifulSoup

BASE_URLS = [
    "http://shbbs.fang.com/bbs_proj_list_A.htm",
    "http://shbbs.fang.com/bbs_proj_list_B.htm",
    "http://shbbs.fang.com/bbs_proj_list_C.htm",
    "http://shbbs.fang.com/bbs_proj_list_D.htm",
    "http://shbbs.fang.com/bbs_proj_list_E.htm",
    "http://shbbs.fang.com/bbs_proj_list_F.htm",
    "http://shbbs.fang.com/bbs_proj_list_G.htm",
    "http://shbbs.fang.com/bbs_proj_list_H.htm",
    "http://shbbs.fang.com/bbs_proj_list_I.htm",
    "http://shbbs.fang.com/bbs_proj_list_J.htm",
    "http://shbbs.fang.com/bbs_proj_list_K.htm",
    "http://shbbs.fang.com/bbs_proj_list_L.htm",
    "http://shbbs.fang.com/bbs_proj_list_M.htm",
    "http://shbbs.fang.com/bbs_proj_list_N.htm",
    "http://shbbs.fang.com/bbs_proj_list_O.htm",
    "http://shbbs.fang.com/bbs_proj_list_P.htm",
    "http://shbbs.fang.com/bbs_proj_list_Q.htm",
    "http://shbbs.fang.com/bbs_proj_list_R.htm",
    "http://shbbs.fang.com/bbs_proj_list_S.htm",
    "http://shbbs.fang.com/bbs_proj_list_T.htm",
    "http://shbbs.fang.com/bbs_proj_list_U.htm",
    "http://shbbs.fang.com/bbs_proj_list_V.htm",
    "http://shbbs.fang.com/bbs_proj_list_W.htm",
    "http://shbbs.fang.com/bbs_proj_list_X.htm",
    "http://shbbs.fang.com/bbs_proj_list_Y.htm",
    "http://shbbs.fang.com/bbs_proj_list_Z.htm"
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

#for url in BASE_URLS :
#	print url
conn = MySQLdb.connect(HOST,USER,PASSWD,DB,PORT)
conn.set_character_set('utf8')

cur = conn.cursor()
cur.execute('SET NAMES utf8')
cur.execute('SET CHARACTER SET utf8')
cur.execute('set character_set_connection=utf8')

for url in BASE_URLS :
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	ul = soup.findAll(attrs={"class": "z_zmList"})
	for ull in ul :
		li = ull.findAll('li')
		for lii in li :
			xqc = xqc + 1
			name = lii.get_text()
			url = lii.find('a').get('href')
			#print name.join(url)
			try:
				n = cur.execute('select * from xiaoqu where url =  \'%s\''%url)
				#not found xiaoqu data
				if n == 0 :
					xqac = xqac + 1
					sql = "insert into xiaoqu(name,url,create_date) values ('%s','%s',now())"%(name,url)
					#print sql
					cur.execute(sql)
					conn.commit()
				else :
					print "find data %s:%s"%(name,url)
			except Exception,e:
				print str(e)
				conn.rollback()
print "-------------find xiaoqu : %s" % xqc + "       add xiaoqu: %s -------------" % xqac
	#print "----find xiaoqu: ".join(str(xqc)).join("......add xiaoqu: ").join(str(xqac)).join('\n')
			#finally :
			#	conn.close()

