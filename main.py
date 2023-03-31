from functions import *



#Files
@app.route('/favicon.ico')
def favicon():  return url_for('static', filename='favicon.ico')
@app.route('/python.ico')
def ico_2():  return url_for('static', filename='python.ico')
@app.route('/jar.ico')
def ico_3():  return url_for('static', filename='jar.ico')
@app.route('/exe.ico')
def ico_4():  return url_for('static', filename='exe.ico')
@app.route('/archives.ico')
def ico_5():  return url_for('static', filename='archives.ico')
@app.route('/img.ico')
def ico_6():  return url_for('static', filename='img.ico')
@app.route('/txt.ico')
def ico_7():  return url_for('static', filename='txt.ico')
@app.route('/gif.ico')
def ico_8():  return url_for('static', filename='gif.ico')
@app.route('/mp3.ico')
def ico_9():  return url_for('static', filename='mp3.ico')
@app.route('/mp4.ico')
def ico_10():  return url_for('static', filename='mp4.ico')
@app.route('/ogg.ico')
def ico_11():  return url_for('static', filename='ogg.ico')
@app.route('/pdf.ico')
def ico_12():  return url_for('static', filename='pdf.ico')
@app.route('/webp.ico')
def ico_13():  return url_for('static', filename='webp.ico')
@app.route('/master-card.ico')
def ico_14():  return url_for('static', filename='master-card.ico')
@app.route('/vis-master-shi.svg')
def ico_15():  return url_for('static', filename='vis-master-shi.svg')



#pages

@app.errorhandler(404)
def page_not_found(e):
	# note that we set the 404 status explicitly
	return render_template('404.html'), 404

@app.errorhandler(403)
def page_access_denied(e):
	# note that we set the 404 status explicitly
	return render_template('403.html'), 403

@app.route('/', methods=['GET', 'POST'])
def index():
	hash_ = request.cookies.get('hash')
	user = get_by_hash(hash_,users)
	if user == False:
		return redirect('login')
	return make_response(render_template('index.html',username=user,phone=users[user]['phone'],fio=users[user]['fio']))


@app.route('/chat')
def chat():
	hash_ = request.cookies.get('hash')
	user = get_by_hash(hash_,users)
	if user == False:
		return redirect('login')
	return render_template('index_chat.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if 'file' in request.files and file.filename != '' and allowed_file(file.filename):
			request.files['file'].save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
			return redirect(url_for('localfiles'))
		else:
			return page_access_denied('Access to load Denied')
	else:
		return page_not_found('File Not Found')


@app.route('/local')
def localfiles():
	return render_template('files.html')

@app.route('/donate')
def donatetempl():
	return render_template(redirect(url_for('paymenttemplate')))

@app.route('/payment')
def paymenttemplate():
	return render_template('paymet.html')


#events

@socketio.on('payment_set')
def payment_set():
	join_room('paymenttemplate')
	emit('set_name',{"name":"Donate","prod":"Donate","price":'10+'},broadcast=False,room='paymenttemplate')

@socketio.on('send_payment_key')
def send_payment_key(message):
	if message == 'test':
		emit('set_name',{"name":"Test","prod":"Мозги","price":120},broadcast=False,room='paymenttemplate')

@socketio.on('set_text')
def set_text(message):
	
	if message == 'card':  method_pay = '2200 2407 5558 8684'
	elif message == 'qiwi':  method_pay = '+79271959406'
	elif message == 'ymoney':  method_pay = '2204 3101 1699 9643'
	emit('set_text',{"data":method_pay,"id":message},broadcast=False,room='paymenttemplate')

@socketio.on('getfiles')
def get_files():
	join_room('localfiles')
	print('Y?')
	data = [allowed_file(i,sp=1) for i in os.listdir(app.config['UPLOAD_FOLDER'])]
	if len(data) > 1: 
		emit('echofiles',{"data":data},broadcast=False,room='localfiles')
	else:
		print(data)

@socketio.on('connect')
def on_connect():
	if getbyip(str(request.remote_addr)).get("nick") == 'Noname: ':
		fusers.append({"ip":str(request.remote_addr),"nick": generate_nick()})
		emit('message', {"admin":adm(str(request.remote_addr)),"Sid":rchar()+str(random.randint(12,999999)+random.randint(0,len(getbyip(str(request.remote_addr)).get("nick")))), "data":f'New User ({getbyip(str(request.remote_addr)).get("nick")}) connect to server'}, broadcast=True)
	writemessage('c_o_nnIcT')

@socketio.on('disconnect')
def on_disconnect():
	emit('wridel',getbyip(str(request.remote_addr)).get("nick"))

@socketio.on('message')
def handle_message(message):
	nick = getbyip(str(request.remote_addr))
	Sid=rchar()+str(random.randint(12,999999)+random.randint(0,len(nick.get("nick"))))
	message_l = message.lower()
	if '!any-manga ' in message_l and len(message_l) > len('!any-manga '):
		return emit('message',{"admin":adm(str(request.remote_addr)),"data":'<li><b style="color:#33bf79;">'+manga.read(message_l.split(' ')[1])+'</b></li>',"Sid":Sid }, broadcast=True)
	
	elif '!any-more ' in message_l and len(message_l) > len('!any-more ') and '|' in message_l:
		mt = manga.take(message_l.split(' ')[1].split('|')[0],message_l.split('|')[1])
		return emit('message',{"admin":adm(str(request.remote_addr)),"data":'<li><b style="color:#33bf79;">'+mt[1]+'</b></li>'+mt[0],"Sid":Sid }, broadcast=True)

	elif 'on' in message_l and '<' in message_l and '"' in message_l:
		message = f'<div class="hack"><h1>В этом сообщении скрипт, нажмите на него только если ему доверяете!</h1>{message}</div>'
	#print(f'\n---------------------\n{nick}  : {message}\n---------------------') Logistick on debug version
	
	if message == 'U_p_l_D_r_0':
		writemessage(message)
		return emit('message', {"admin":adm(str(request.remote_addr)),"data":'<center><a href="#popup" class="button">Загрузить файл</a></center><div class="-"><div class="popup" id="popup"><div class="popup-inner"><div class="popupphoto"><img src="/static/header.jpg" alt="Atomic Heart Dance Robots"></div><div class="popuptext"><h1>Загрузите файл</h1><form action = "/uploader" method = "POST" enctype = "multipart/form-data"><input name="Sid" value="'+Sid+'" style="display:none;"><input type = "file" name="file" /><input type="submit"/></form></div><a class="closepopup" href="#">X</a></div></div></div>',"Sid":Sid});
	elif len(message_l) > 0 and check(message_l):
		emit('message', {"admin":adm(str(request.remote_addr)),"data":'<b style="color:#55E19D;">'+nick.get("nick")+'</b>'+message,"Sid":Sid}, broadcast=True)
	
		
@socketio.on('messageotv')
def handle_messageotv(message,Sid):
	message_l = message.lower()
	if 'on' in message_l and '<' in message_l and '"' in message_l:
		message = f'<div class="hack"><h1>В этом сообщении скрипт, нажмите на него только если ему доверяете!</h1>{message}</div>'
	
	if len(message_l) > 0 and check(message_l):
		emit('messageotv',{"admin":adm(str(request.remote_addr)),"data":'<li><b style="color:#33bf79;">'+getbyip(str(request.remote_addr)).get("nick")+'</b>'+message+'</li>',"Sid":Sid}, broadcast=True)
		
@socketio.on('writemessage')
def writemessage(key):
	if key == 'Backspace':
		tex = '<b style="color:#55E19D;">'+random.choice(['🔏','📝'])+getbyip(str(request.remote_addr)).get("nick")+'</b>стирает сообщение.'
	elif key == 'U_p_l_D_r_0':
		tex = '<b style="color:#55E19D;">'+random.choice(['📄','🖼'])+getbyip(str(request.remote_addr)).get("nick")+'</b>отправляет файл.'
	elif key == 'c_o_nnIcT':
		tex = '<b style="color:#55E19D;">'+getbyip(str(request.remote_addr)).get("nick")+'</b>В чатике.'
	else:
		tex = '<b style="color:#55E19D;">'+random.choice(['✍️','🖋'])+getbyip(str(request.remote_addr)).get("nick")+'</b>набирает сообщение.'
	emit('writemessage',{"tex":tex,"nick":getbyip(str(request.remote_addr)).get("nick")}, broadcast=True)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	response = make_response(redirect(url_for('login')))
	response.set_cookie('hash', '', expires=datetime.now() - timedelta(days=1))
	return response

@app.route('/edit', methods=['GET', 'POST'])
def edit_index():
	hash_ = request.cookies.get('hash')
	user = get_by_hash(hash_,users)
	if user == False:
		return redirect('login')

	if request.method == 'POST':
		phone = request.form['phone']
		fi = request.form['last_name'].strip()
		ii = request.form['first_name'].strip()
		oi = request.form['patronymic'].strip()
		snils = request.form['snils']
		passport_series = request.form['passport_series']
		birthdate = request.form['birthdate']
		citizenship = request.form['citizenship']
		fio = fi+' '+ii+' '+oi
		users[user]['snils'] = snils;change_per_base(hash_,5,snils)
		users[user]['passport_series'] = passport_series;change_per_base(hash_,6,passport_series)
		users[user]['birthdate'] = birthdate;change_per_base(hash_,7,birthdate)
		users[user]['citizenship'] = citizenship;change_per_base(hash_,8,citizenship)
		users[user]['phone'] = phone;change_per_base(hash_,2,phone)
		if fio != users[user]['fio']:
			users[user]['fio'] = fio
			change_per_base(hash_,3,fio)
		return redirect('/')

	return make_response(render_template('edit_index.html',
		username=user,phone=users[user]['phone'],
		fi=users[user]['fio'].split(' ')[0],
		ii=users[user]['fio'].split(' ')[1],
		oi=users[user]['fio'].split(' ')[2],
		snils=users[user]['snils'],
		passport_series=users[user]['passport_series'],
		birthdate=users[user]['birthdate'],
		citizenship=users[user]['citizenship']))

@app.route('/index_files/<path:path>')
def index_files(path):
	return send_from_directory('templates/index_files/', path)

@app.route('/edit_index_files/<path:path>')
def edit_index_files(path):
	return send_from_directory('templates/index_files/', path)

@app.route('/register', methods=['GET', 'POST'])
def register():
	global username
	if request.method == 'POST':
		username = request.form['username']
		if username == 'None':
			return render_template('registration.html', message='Username already exists')
		password = request.form['password']
		phone = request.form['phone']
		fio = request.form['fio']
		if username not in users:
			hash_ = generate_hash()
			add_to_base(username, password, phone, fio, hash_)
			users[username] = {'password': password,'phone':phone,'fio':fio, 'hash': hash_,'snils':'','passport_series':'', 'birthdate':'','citizenship':''}
			resp = make_response(render_template('registration.html', message='Registration successful'))
			resp.set_cookie('hash', hash_)
			return resp
		else:
			return render_template('registration.html', message='Username already exists')
	else:
		return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	global username

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username in users and password == users[username]['password']:
			resp = make_response(redirect('/'))
			resp.set_cookie('hash', users[username]['hash'])
			return resp
		else:
			return render_template('login.html', message=Markup('<script>alert("Invalid username or password");</script>'))
	else:
		response = make_response(render_template('login.html'))
		#response.set_cookie('my_cookie', '', expires=datetime.now() - timedelta(days=1))
		return render_template('login.html')