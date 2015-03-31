# -*- coding: utf-8 -*-
import requests,MySQLdb,re
from bs4 import BeautifulSoup

BASE_URL = "http://shanghai.anjuke.com/community/W0QQpZ"


HOST = '127.0.0.1'
USER = 'root'
PASSWD = '811107'
DB = 'hfhfs'
PORT = 3306
#total_count,add_count
add_count = 0
total_count = 0
diff_count = 0

conn = MySQLdb.connect(HOST,USER,PASSWD,DB,PORT)
conn.set_character_set('utf8')

def get_detail ( url , address ):
	result = []
	detailReq = requests.get(url)
	detailSoup = BeautifulSoup(detailReq.text)
	xqName = detailSoup.find("div","comm-cont").find("h1")
	xqDetail = detailSoup.find("div","comm-list").findAll("dd")
	i = 0
	result.append(url)
	result.append(re.findall(r'view/(\w+)',url)[0])
	result.append(address)
	for a in xqDetail :
		# 0:name 1:district&area 5:btype 8:totalcount 9:buildtime
		if i in (0,1,5,8,9) :
			result.append(a.get_text())
		i = i + 1
	arealist = re.sub(r'\s+',' ',result[4]).strip(' ').strip('\n').split(" ")
	for area in arealist :
		result.append(area)
	del result[4]
	n = 0
	# result: 0:url 1:id 2:address 3:name 4:btype 5:totalcount 6:buildtime 7:district 8:area(optional)
	#for r in result :
	#	print r
	return result

#add data to xiaoqu
def add_data ( result ):
	global total_count , add_count , diff_count
	cur = conn.cursor()
	cur.execute('SET NAMES utf8')
	cur.execute('SET CHARACTER SET utf8')
	cur.execute('set character_set_connection=utf8')

	print len(result)
	try:
		n = cur.execute('select * from xiaoqu where id = %s'%result[1])
		total_count = total_count + 1
		#not found xiaoqu data
		if n == 0 :
			add_count = add_count + 1
			if len(result) == 9 :
				sql = "insert into xiaoqu(id,name,url,py,ajkid,district,area,address,buildtime,btype,totalcount,create_date) values (%s,'%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s',now())"%(result[1],result[3],result[0],'',result[1],result[7],result[8],result[2],result[6],result[4],result[5])
			else :
				sql = "insert into xiaoqu(id,name,url,py,ajkid,district,area,address,buildtime,btype,totalcount,create_date) values (%s,'%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s',now())"%(result[1],result[3],result[0],'',result[1],result[7],'',result[2],result[6],result[4],result[5])
			print sql
			cur.execute(sql)
			conn.commit()
		else :
			print "find data %s:%s"%(result[3],result[0])
	except Exception,e :
		print str(e)
		conn.rollback()



f = open('log.txt','r')
current_page = f.readline()
f.close()
if not len(current_page) :
	current_page = '1'
for a in range (int(current_page),1976) :
	f = open('log.txt','w')
	f.write(str(a))
	listReq = requests.get(BASE_URL + str(a))
	listSoup = BeautifulSoup(listReq.text)
	xqlist = listSoup.findAll("div",{ "class":"details" })
	for xq in xqlist :
		url = xq.find(id = re.compile("comm_name_qt_apf_id\d*")).get('href')
		address = xq.find("div",{ "class":"t_b"}).next_sibling.next_sibling.get_text()
		result = get_detail ( url,address )
		add_data( result )	
conn.close()
f.close()
print "-------------find xiaoqu : %s" % total_count + "       add xiaoqu: %s -------------" % add_count
