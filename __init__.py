#from's
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, session, send_from_directory, redirect, url_for, make_response
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime, timedelta

#import's
import random,os,requests


#Flask static per

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'static'
app.debug = False
socketio = SocketIO(app)

#static per

host = input("Enter your domain: ")
fusers = []
users = {
}
lock_word = ['script','style','iframe','button','href','javascript']
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3','mp4','svg','ico','webp','exe','py','jar','cpp','zip','rar','ogg','waw'}
ALLOWED_EXTENSIONS_Type = {
	'media':['png', 'jpg', 'jpeg', 'gif','svg','ico','webp'], #jpg jpeg svg ico waw (rar zip archives)
	'music': ['mp3','wav','ogg','m4a'],
	'other': ['rar','zip','cpp','py','jar','exe','pdf','txt','msi','mp4']
}

