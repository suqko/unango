from bottle import *
import requests
import pymysql
import random
import socket
import json
import threading


@route('/conmysql', method=['POST', 'GET'])
def conmysql():
	# start_response('200 OK', [('Content-Type', 'text/html')])
	db = pymysql.connect(host="", user='cloud', password='!57465248', db='clouddata', port=3306)
	# db= pymysql.connect(user='test1',password='testtest',db='pymysql_db',port=3306)
	cur = db.cursor()
	sql = 'select * from data_test'
	try:
		cur.execute(sql)
		db.commit()
		results = cur.fetchall()
		# print(results)
		le = len(results)
		return str(results[le - 1][2]) + '.' + str(int(random.random() * 10))
	except Exception as e:
		raise e
	finally:
		db.close()


def finmysql():
	db = pymysql.connect(host="", user='cloud', password='!57465248', db='clouddata', port=3306)
	# db= pymysql.connect(user='test1',password='testtest',db='pymysql_db',port=3306)
	cur = db.cursor()
	sql = 'select * from data_test'
	try:
		cur.execute(sql)
		db.commit()
		results = cur.fetchall()
		le = len(results)
		return str(results[le - 1][0] + results[le - 1][1] + results[le - 1][2] + results[le - 1][3])
	except Exception as e:
		raise e
	finally:
		db.close()


@route('/loginapp', method=['POST', 'GET'])
def loginapp():
	data = request.body.readlines()[0]
	dicte = json.loads(str(data))
	state = dicte["CMD"]["value"]
	print(state)
	strr = finmysql()
	if state == '1111':
		conn.sendall(strr + '00')
		# return get_wiki_page(page)
		return '<p>Your start</p>'
	else:
		conn.sendall(strr + '11')
		return '<p>Your stop/p>'


@route('/login', method=['POST', 'GET'])
def login():
	state = request.forms.get('action')
	# state = request.forms.get('HTTP_action')
	# print(state)
	strr = finmysql()
	# print(strr)
	if state == 'open':
		conn.sendall(strr + '00')
		# return get_wiki_page(page)
		return '<p>Your start</p>'
	else:
		conn.sendall(strr + '11')
		return '<p>Your stop/p>'
	# @route('/login', method = 'POST')


def setmysql(str):
	db = pymysql.connect(host="", user='cloud', password='!57465248', db='clouddata', port=3306)
	# db= pymysql.connect(user='test1',password='testtest',db='pymysql_db',port=3306)

	cur = db.cursor()
	sql_insert = """insert into data_test(Head,netAddr,temvalue,tail,led) values"""
	sql = 'select * from test'
	try:
		cur.execute(sql_insert + "('%s','%s','%s','%s','%s')" % (str[0:1], str[1:5], str[5:7], str[7:8], str[8:10]))
		db.commit()
		results = cur.fetchall()
		# print(results)
		# return results
	except Exception as e:
		raise e
	finally:
		db.close()


def udpserver():
	ss = ''
	udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udpSocket.bind(("", 8889))
	print("udp wait...")
	while True:
		recvData = udpSocket.recvfrom(10)
		content, destInfo = recvData
		if ss != content:
			setmysql(content)
			print("udp content is %s" % content.decode("utf-8"))
		ss = content


if __name__ == '__main__':
    ip_port = ('0.0.0.0', 8888)
    
    sk = socket.socket()
    sk.bind(ip_port)
    sk.listen(5)
    print('wait tcp...')
    threads = []
    t1 = threading.Thread(target=udpserver)
    threads.append(t1)
    for t in threads:
      t.setDaemon(True)
      t.start()
    conn, addr = sk.accept()
    print("tcp ok...")
    
    run(host='0.0.0.0', port=8080)
    conn.close()
