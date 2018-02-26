import json
import urllib.request
import requests
#data = { 'grid': ['O','O',' ','X',' ',' ',' ','X','X'],'winner':' '}

data2 = {'username':'b','password':'1234','email':'zouzhi96@gmail.com'}
req = urllib.request.Request('http://127.0.0.1:8000/ttt/adduser/')
req.add_header('Content-Type','application/json')

response = urllib.request.urlopen(req, json.dumps(data2).encode('utf8'))
# #print(response.read().decode('utf-8'))

data2 = {'email':'zouzhi96@gmail.com','key':'abracadabra'}
req = urllib.request.Request('http://127.0.0.1:8000/ttt/verify/')
req.add_header('Content-Type','application/json')

response = urllib.request.urlopen(req, json.dumps(data2).encode('utf8'))


#test login
# data = {'username':'a','password':'1234'}
# req = urllib.request.Request('http://127.0.0.1:8000/ttt/login/')
# req.add_header('Content-Type','application/json')
# response = urllib.request.urlopen(req, json.dumps(data).encode('utf8'))

# print(response.read().decode('utf-8'))
# print(response.cookies)

# headers = {'content-type': 'application/json'}
# data = {'username':'a','password':'1234'}
# r = requests.post('http://127.0.0.1:8000/ttt/login/', data=json.dumps(data), headers=headers)
# for cookie in r.cookies:
# 	print(r.cookies['SESSION'])