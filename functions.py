from __init__ import *

def getbyip(ip):
	for i in fusers:
		if i.get('ip') == str(ip):
			return i
	return {"ip":ip,"nick":"Noname: "}

def getbynick(nick):
	for i in fusers:
		if i.get('nick') == str(nick):
			return i
	return {"ip":"NotIp","nick":nick}

def generate_nick(): 
	with open('nicks.txt','r',encoding='UTF-8') as base: 
		base = [i.strip()+' : ' for i in base.read().split('\n')]
	return base[random.randint(0,len(base)-1)]

def check(msg):
	msg.lower()
	for i in lock_word:
		if i in msg and '<' in msg:
			return False
		if 'mouse' in msg or 'DOM' in msg:
			return False
	return True

def rchar():
	return random.choice(list('qwert8yui7opasdfghjkl1zxcv5b6nm_$QWERT4YUIO23PASD9FGHJK0LZXCVBNM'))

def generate_hash(len_=39):
	word = ''
	for i in range(0,len_):
		word += str(rchar())
	return word

def get_by_hash(hash_,users):
	for i in users:
		if users[i]['hash'] == hash_:
			return i
	return False

def adm(ip):
	if ip == host:  return 0
	else:  return 1

def typi(exist):
	if exist in ALLOWED_EXTENSIONS_Type['media']:  return 'media'
	elif exist in ALLOWED_EXTENSIONS_Type['music']:  return 'music'
	else:  return 'other'

def allowed_file(filename,sp=0):
	ti = filename.rsplit('.')[-1].lower()
	if ti in ALLOWED_EXTENSIONS_Type['media'] or ti in ALLOWED_EXTENSIONS_Type['music'] or ti in ALLOWED_EXTENSIONS_Type['other']:
		if sp == 0:  return True
		else:  return {"file_type": os.path.splitext(filename)[1][1:], "file_name":filename,"type":typi(ti)}


def send_message(chat_id, message):
	url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
	payload = {'chat_id': chat_id, 'text': message}
	requests.post(url, json=payload)

def change_base(hash_,name,per):
	cursor.execute(f"UPDATE users SET {name} = ? WHERE hash = ?", (per, hash_))
	conn.commit()

def change_per_base(hash_,pers,per):
	change_base(hash_,db_pers_num[int(pers)],per)

def add_to_base(username, password, phone, fio, hash_, snils='', passport_series='', birthdate='', citizenship='', male_female='', friends='', mailTo=''):
	cursor.execute('''
	INSERT INTO users (username, password, phone, fio, hash, snils, passport_series, birthdate, citizenship, male_female, friends, mailTo)
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (username, password, phone, fio, hash_, snils, passport_series, birthdate, citizenship, male_female, friends, mailTo))
	conn.commit()


def to_json():
    global users
    global db_pers_num
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    db_users = cursor.fetchall()
    for user in db_users:
        users[user[1]] = {
            "password": user[2],
            "phone": user[3],
            "fio": user[4],
            "hash": user[5],
            "snils": user[6],
            "passport_series": user[7],
            "birthdate": user[8],
            "citizenship": user[9],
            "male_female": user[10],
            "friends": user[11],
            "mailTo": user[12]
        }

    cursor.execute('SELECT * FROM users LIMIT 1')
    db_pers_num = [description[0] for description in cursor.description][1:];print(db_pers_num)
    conn.commit()


to_json()