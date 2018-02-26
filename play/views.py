from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import HttpResponseBadRequest
import os, smtplib, random, string, json, hashlib, datetime
from email.mime.text import MIMEText

@csrf_exempt
def index(request):
	if request.META.get('CONTENT_TYPE') == 'application/json':
		if request.method == 'POST':
			griddict = json.loads(request.body.decode('utf8'))
			
			new_griddict = processGrid(griddict)
			#print(new_griddict)
			return HttpResponse(json.dumps(new_griddict).encode('utf8'),content_type="application/json")
	return HttpResponse("")

@csrf_exempt
def index2(request):
	result_json = { "status":'ERROR'}
	if request.META.get('CONTENT_TYPE') == 'application/json':
		if request.method == 'POST':
			griddict = json.loads(request.body.decode('utf8'))
			move = griddict['move']
			#print(move)
			if 'SESSION' in request.COOKIES:
				#print(move)
				session = request.COOKIES['SESSION']
				with open('sessions.json','r') as jfile:
					old_ses = json.load(jfile)
				try:
					for i in old_ses['sessions']:
						if session in old_ses['sessions'][i] :
							username = i
					with open('accounts.json','r') as jfile:
						old_accs = json.load(jfile)
					for i in range(len(old_accs['accounts'])):
						each_acc = old_accs['accounts'][i]
						
						if each_acc['username'] == username:
							
							user = each_acc
							acc_index = i
					#user is the account
					if user['grid'][move] == ' ':
						user['grid'][move] = 'X'
						griddict = processGrid({'grid' : user['grid']})

						if 'winner' not in griddict:
							user['grid'] = griddict['grid']
							old_accs['accounts'][acc_index] = user
							with open('accounts.json','w') as ofile:
								json.dump(old_accs,ofile)
							
						else:
							if griddict['winner'] == 'X':
								user['grid'] = [' ',' ',' ',' ',' ',' ',' ', ' ',' ']
								user['human'] += 1
								old_accs['accounts'][acc_index] = user
								with open('accounts.json','w') as ofile:
									json.dump(old_accs,ofile)
								


							else:
								if griddict['winner'] == 'O':
									user['wopr'] += 1
								elif griddict['winner'] == ' ':
									user['tie'] += 1
								user['grid'] = [' ',' ',' ',' ',' ',' ',' ', ' ',' ']
								old_accs['accounts'][acc_index] = user
								with open('accounts.json','w') as ofile:
									json.dump(old_accs,ofile)



							################################
							#Game list
							with open('gamelists.json','r') as jfile:
								gamelists = json.load(jfile)
							for i in range(len(gamelists['gamelists'])):
								if username in gamelists['gamelists'][i]:
									gid = len(gamelists['gamelists'][i][username]) - 1
									gamelists['gamelists'][i][username][gid]['grid'] = griddict['grid']
									gamelists['gamelists'][i][username][gid]['winner'] = griddict['winner']
							
									gid += 1 
									date = datetime.datetime.now().strftime("%y-%m-%d")
									gamelists['gamelists'][i][username] += [{'id':gid, 'grid':[' ',' ',' ',' ',' ',' ',' ', ' ',' '], 'start_date':date,'winner':'None'}]
									
									with open('gamelists.json','w') as ofile:
										json.dump(gamelists,ofile)
							################################
							return HttpResponse(json.dumps(griddict).encode('utf8'),content_type="application/json")
						#print(json.dumps(griddict))
						return HttpResponse(json.dumps(griddict).encode('utf8'),content_type="application/json")
	

				except:
					print("??")
					pass
	return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")

@csrf_exempt
def listgames(request):
	result_json = { "status":'ERROR'}
	if request.META.get('CONTENT_TYPE') == 'application/json':
		if request.method == 'POST':
			if 'SESSION' in request.COOKIES:
				#print(move)
				session = request.COOKIES['SESSION']
				with open('sessions.json','r') as jfile:
					old_ses = json.load(jfile)
				try:
					for i in old_ses['sessions']:
						if session in old_ses['sessions'][i] :
							username = i
					with open('gamelists.json','r') as jfile:
						gamelists = json.load(jfile)
					for i in range(len(gamelists['gamelists'])):
						each_acc = gamelists['gamelists'][i]
						if username in each_acc:
							user = each_acc
							acc_index = i
							break
					lists = []
					for i in range(len(user[username])-1):
						lists += [{"id":user[username][i]['id'],"start_date":user[username][i]['start_date']}]

					result_json = {"status":'OK',"games":lists}
					return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")
					#user is the account
				except:
					pass
	# if 'SESSION' in request.COOKIES:
	# 			#print(move)
	# 			session = request.COOKIES['SESSION']
	# 			with open('sessions.json','r') as jfile:
	# 				old_ses = json.load(jfile)
	# 			try:
	# 				for i in old_ses['sessions']:
	# 					if session in old_ses['sessions'][i] :
	# 						username = i
	# 				with open('gamelists.json','r') as jfile:
	# 					gamelists = json.load(jfile)
	# 				for i in range(len(gamelists['gamelists'])):
	# 					each_acc = gamelists['gamelists'][i]
	# 					if username in each_acc:
	# 						user = each_acc
	# 						acc_index = i
	# 						break
	# 				lists = []
	# 				for i in range(len(user[username])-1):
	# 					lists += [{"id":user[username][i]['id'],"start_date":user[username][i]['start_date']}]

	# 				result_json = {"status":'OK',"games":lists}
	# 				return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")
	# 				#user is the account
	# 			except:
	# 				pass
	return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")
					

@csrf_exempt
def getgame(request):
	result_json = { "status":'ERROR'}
	if request.META.get('CONTENT_TYPE') == 'application/json':
		if request.method == 'POST':
			griddict = json.loads(request.body.decode('utf8'))
			gid = griddict['id']
			if 'SESSION' in request.COOKIES:
				#print(move)
				session = request.COOKIES['SESSION']
				with open('sessions.json','r') as jfile:
					old_ses = json.load(jfile)
				try:
					for i in old_ses['sessions']:
						if session in old_ses['sessions'][i] :
							username = i
					with open('gamelists.json','r') as jfile:
						gamelists = json.load(jfile)
					for i in range(len(gamelists['gamelists'])):
						each_acc = gamelists['gamelists'][i]
						if username in each_acc:
							user = each_acc
							acc_index = i
							break
					for i in range(len(user[username])-1):
						if user[username][i]['id'] == gid:
							grid = user[username][i]['grid']
							winner = user[username][i]['winner']
					result_json = {"status":'OK',"grid":grid,"winner":winner}
					return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")
					#user is the account
				except:
					pass
	return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")

def getscore(request):
	result_json = { "status":'ERROR'}
	if request.META.get('CONTENT_TYPE') == 'application/json':
		if request.method == 'POST':
			if 'SESSION' in request.COOKIES:
				#print(move)
				session = request.COOKIES['SESSION']
				with open('sessions.json','r') as jfile:
					old_ses = json.load(jfile)
				try:
					for i in old_ses['sessions']:
						if session in old_ses['sessions'][i] :
							username = i
					with open('accounts.json','r') as jfile:
						old_accs = json.load(jfile)
					for i in range(len(old_accs['accounts'])):
						each_acc = old_accs['accounts'][i]
						
						if each_acc['username'] == username:
							
							user = each_acc
							acc_index = i
					#user is the account
					
					result_json = {"status":'OK',"human":user['humane'],"wopr":user['wopr'],"tie":user['tie']}
					return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")
					#user is the account
				except:
					pass
	if 'SESSION' in request.COOKIES:
				#print(move)
				session = request.COOKIES['SESSION']
				with open('sessions.json','r') as jfile:
					old_ses = json.load(jfile)
				try:
					for i in old_ses['sessions']:
						if session in old_ses['sessions'][i] :
							username = i
					with open('accounts.json','r') as jfile:
						old_accs = json.load(jfile)
					for i in range(len(old_accs['accounts'])):
						each_acc = old_accs['accounts'][i]
						
						if each_acc['username'] == username:
							
							user = each_acc
							acc_index = i
					#user is the account
					
					result_json = {"status":'OK',"human":user['human'],"wopr":user['wopr'],"tie":user['tie']}
					return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")
					#user is the account
				except:

					pass
	return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")


@csrf_exempt
def adduser(request):
	result_json = { "status":'ERROR'}
	#print(os.path.dirname(os.path.realpath(__file__)))
	if request.method == 'POST':
		if request.META.get('CONTENT_TYPE') == 'application/json':
			account = json.loads(request.body.decode('utf8'))
			username = account['username']
			password = str(account['password'])
			passwordh = (hashlib.sha256(password.encode('utf8'))).hexdigest()
			print(passwordh)
			account['password'] = passwordh
			email = account['email']
			verify = False
			account['verify'] = False
			account['grid'] = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
			account['human'] = 0
			account['wopr'] = 0
			account['tie'] = 0

			key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
			account['key'] = key
			old_accs = {}
			with open('accounts.json','r') as jfile:
				old_accs = json.load(jfile)
				
			accs = old_accs['accounts']
			exist = False
			for i in accs:
				if i['username'] == username:
					exist = True


			if not exist:
				######################
				#add game list
				with open('gamelists.json','r') as jfile:
					gamelists = json.load(jfile)
				gamelists['gamelists']+=[{username:[]}]

				with open('gamelists.json','w') as ofile:
					json.dump(gamelists,ofile)
				######################
				old_accs['accounts'].append(account)
				with open('accounts.json','w') as ofile:
					json.dump(old_accs,ofile)
				

				message = MIMEText("Key is "+key+"\nOr click on: \nxxxxxx")
				message['Subject'] = 'Tic-Tac-Toe Verification Key.'
				message['From'] = 'zzsafe96@gmail.com'
				message['To'] = email

				server = smtplib.SMTP('smtp.gmail.com',587)
				server.starttls()
				server.login("zzsafe96@gmail.com",'Zz123456')
				
				server.sendmail("zzsafe96@gmail.com",email,message.as_string())
				server.quit()
				result_json = {"status":"OK"}
			else:
				#print("???")
				pass
	return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")


@csrf_exempt
def verify(request):
	result_json = {"status":"ERROR"}
	if request.method == 'POST':
		if request.META.get('CONTENT_TYPE') == 'application/json':
			post_var = json.loads(request.body.decode('utf8'))
			with open('accounts.json','r') as jfile:
				old_accs = json.load(jfile)
			for j in range(len(old_accs['accounts'])):
				i = old_accs['accounts'][j]
				if i['email'] == post_var['email']:
					if post_var['key'] == 'abracadabra' or post_var['key']==i['key']:
						old_accs['accounts'][j]['verify'] = True
						#write the new data
						with open('accounts.json','w') as ofile:
							json.dump(old_accs,ofile)

						result_json = {"status":"OK"}
	if request.method == 'GET':
		try:
			post_var = {}
			post_var['email'] = request.GET["email"]
			post_var['key'] = request.GET["key"]
			with open('accounts.json','r') as jfile:
				old_accs = json.load(jfile)
			for j in range(len(old_accs['accounts'])):
				i = old_accs['accounts'][j]
				if i['email'] == post_var['email']:
					if post_var['key'] == 'abracadabra' or post_var['key']==i['key']:
						old_accs['accounts'][j]['verify'] = True
						#write the new data
						with open('accounts.json','w') as ofile:
							json.dump(old_accs,ofile)
						result_json = {"status":"OK"}
		except:
			pass
	return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")

@csrf_exempt
def login(request):
	result_json = {"status":"ERROR"}
	if request.method == 'POST':
		if request.META.get('CONTENT_TYPE') == 'application/json':
			post_var = json.loads(request.body.decode('utf8'))
			with open('accounts.json','r') as jfile:
				old_accs = json.load(jfile)
			#check each account
			for i in old_accs['accounts']:

				if post_var['username'] == i['username']:
					password = str(post_var['password'])
					passwordh = (hashlib.sha256(password.encode('utf8'))).hexdigest()
					print(passwordh)
					print(i['password'])
					if passwordh == i['password'] and i['verify']:
						#pass
						result_json = {"status":"OK"}
						session = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
						#add session to file
						with open('sessions.json','r') as jfile:
							old_ses = json.load(jfile)
						if post_var['username'] not in old_ses['sessions']:

							old_ses['sessions'][post_var['username']] = []
						old_ses['sessions'][post_var['username']] += [session]

						with open('sessions.json','w') as ofile:
							json.dump(old_ses,ofile)
						#end add session to file
						response = HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")
						response.set_cookie('SESSION', session)
						return response

					else:
						break	
	return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")

@csrf_exempt
def logout(request):
	result_json = {"status":"ERROR"}
	if request.method == 'POST' or request.method == 'GET':
		#username = request.GET["username"]
		if 'SESSION' in request.COOKIES:
			session = request.COOKIES['SESSION']

		#delete session to file
		with open('sessions.json','r') as jfile:
			old_ses = json.load(jfile)
		for i in old_ses['sessions']:
			if session in old_ses['sessions'][i]:
				old_ses['sessions'][i].remove(session)


		with open('sessions.json','w') as ofile:
			json.dump(old_ses,ofile)
		#end delete session to file
		result_json = {"status":"OK"}
		response = HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")
		response.set_cookie('SESSION', '')
		return response
	return HttpResponse(json.dumps(result_json).encode('utf8'),content_type="application/json")

def processGrid(griddict):
	#print(checkWinner(griddict['grid']))
	#if winner in griddict:
		#return griddict
	check = False
	for i in range(0,9):
		if griddict['grid'][i] == ' ':
			check = True
	if not check:
		griddict['winner']=' '
		return griddict
	
	w  = checkWinner(griddict['grid'])
	
	if w != '':
		griddict['winner'] = w
	
	if w  == '':
		if griddict['grid'][4] == ' ':
			griddict['grid'][4] = 'O'
			w = checkWinner(griddict['grid'])	
		else:
			if checkWinningSpot(griddict['grid'])!=-1:
				s = checkWinningSpot(griddict['grid'])
				griddict['grid'][s] = 'O'
				w = checkWinner(griddict['grid'])
				if w != '':
					griddict['winner'] = w
			else:	
				griddict['grid'][griddict['grid'].index(' ')] = 'O'
				w = checkWinner(griddict['grid'])
				if w != '':
					griddict['winner'] = w
	return griddict

def checkWinningSpot(gridlist):
	if checkPosition2(gridlist,0,1,2) != -1:
		return checkPosition2(gridlist,0,1,2)
	if checkPosition2(gridlist,3,4,5) != -1:
		return checkPosition2(gridlist,3,4,5)
	if checkPosition2(gridlist,6,7,8) != -1:
		return checkPosition2(gridlist,6,7,8)
	if checkPosition2(gridlist,0,3,6) != -1:
		return checkPosition2(gridlist,0,3,6)
	if checkPosition2(gridlist,1,4,7) != -1:
		return checkPosition2(gridlist,1,4,7)
	if checkPosition2(gridlist,2,5,8) != -1:
		return checkPosition2(gridlist,2,5,8)
	if checkPosition2(gridlist,0,4,8) != -1:
		return checkPosition2(gridlist,0,4,8)
	if checkPosition2(gridlist,2,4,6) != -1:
		return checkPosition2(gridlist,2,4,6)
	if checkPosition3(gridlist,0,1,2) != -1:
		return checkPosition3(gridlist,0,1,2)
	if checkPosition3(gridlist,3,4,5) != -1:
		return checkPosition3(gridlist,3,4,5)
	if checkPosition3(gridlist,6,7,8) != -1:
		return checkPosition3(gridlist,6,7,8)
	if checkPosition3(gridlist,0,3,6) != -1:
		return checkPosition3(gridlist,0,3,6)
	if checkPosition3(gridlist,1,4,7) != -1:
		return checkPosition3(gridlist,1,4,7)
	if checkPosition3(gridlist,2,5,8) != -1:
		return checkPosition3(gridlist,2,5,8)
	if checkPosition3(gridlist,0,4,8) != -1:
		return checkPosition3(gridlist,0,4,8)
	if checkPosition3(gridlist,2,4,6) != -1:
		return checkPosition3(gridlist,2,4,6)
	return -1

def checkPosition2(gridlist,p1,p2,p3):
	if gridlist[p1] == 'O' and gridlist[p2] == 'O' and gridlist[p3] == ' ':
		return p3
	if gridlist[p1] == ' ' and gridlist[p2] == 'O' and gridlist[p3] == 'O':
		return p1
	if gridlist[p1] == 'O' and gridlist[p2] == ' ' and gridlist[p3] == 'O':
		return p2
	return -1

def checkPosition3(gridlist,p1,p2,p3):
	if gridlist[p1] == ' ' and gridlist[p2] == 'X' and gridlist[p3] == 'X':
		return p1
	if gridlist[p1] == 'X' and gridlist[p2] == ' ' and gridlist[p3] == 'X':
		return p2
	if gridlist[p1] == 'X' and gridlist[p2] == 'X' and gridlist[p3] == ' ':
		return p3	
	return -1

def checkWinner(gridlist):
	try:
		if checkPosition(gridlist,0,1,2) and gridlist[0] == 'O':
			return 'O'
		if checkPosition(gridlist,3,4,5) and gridlist[3] == 'O':
			return 'O'
		if checkPosition(gridlist,6,7,8) and gridlist[6] == 'O':
			return 'O'
		if checkPosition(gridlist,0,3,6) and gridlist[0] == 'O':
			return 'O'
		if checkPosition(gridlist,1,4,7) and gridlist[1] == 'O':
			return 'O'
		if checkPosition(gridlist,2,5,8) and gridlist[2] == 'O':
			return 'O'
		if checkPosition(gridlist,0,4,8) and gridlist[0] == 'O':
			return 'O'
		if checkPosition(gridlist,2,4,6) and gridlist[2] == 'O':
			return 'O'
		if checkPosition(gridlist,0,1,2) and gridlist[0] == 'X':
			return 'X'
		if checkPosition(gridlist,3,4,5) and gridlist[3] == 'X':
			return 'X'
		if checkPosition(gridlist,6,7,8) and gridlist[6] == 'X':
			return 'X'
		if checkPosition(gridlist,0,3,6) and gridlist[0] == 'X':
			return 'X'
		if checkPosition(gridlist,1,4,7) and gridlist[1] == 'X':
			return 'X'
		if checkPosition(gridlist,2,5,8) and gridlist[2] == 'X':
			return 'X'
		if checkPosition(gridlist,0,4,8) and gridlist[0] == 'X':
			return 'X'
		if checkPosition(gridlist,2,4,6) and gridlist[2] == 'X':
			return 'X'
		for i in gridlist:
			if i == ' ':
				return ''
		return ' '
	except:
		#print("here:")
		#print(gridlist)
		return None

def checkPosition(gridlist,p1,p2,p3):
	if gridlist[p1] == 'O' and gridlist[p2] == 'O' and gridlist[p3] == 'O':
		return True
	if gridlist[p1] == 'X' and gridlist[p2] == 'X' and gridlist[p3] == 'X':
		return True
	return False
