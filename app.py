from flask import Flask, request, jsonify, send_file
import json
#import wordParse


app = Flask(__name__, static_url_path='')

@app.route('/')

def root():
   return 'Hello World'

@app.route('/sanfrancisco/')

def location():
   return 'You are in SF, bitchhhhh, lets get some boba tea>?>>>'


@app.route('/user/<username>/')
def welcome(username):
   return 'Welcome to hello world, you stupid bitch........'+username


@app.route('/tweet/<query>/')
def parse(query):
   l = len(query)
   return str(l)



if __name__ == "__main__":
   app.run()
