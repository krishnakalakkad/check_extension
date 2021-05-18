from flask import Flask, request, jsonify, send_file, render_template
from wordParse import main

app = Flask(__name__, static_url_path='')

@app.route('/')

def root():
   return 'Hello World'

@app.route('/user/<username>/')
def welcome(username):
   return 'Welcome to hello world, you stupid bitch........'+username

@app.route('/tweet/', defaults={'name' : 'No val entered'})

@app.route('/tweet/<string:tweet>/')
def parse(tweet):
   listofqry = main(tweet)

   return listofqry[0]



if __name__ == "__main__":
   app.run()
