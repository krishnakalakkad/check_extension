from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import json
from wordParse import main

app = Flask(__name__, static_url_path='')
CORS(app)


@app.route('/')

def root():
   return 'Hello World'

@app.route('/user/<username>/')
def welcome(username):
   return 'Welcome to hello world, you stupid bitch........'+username

@app.route('/tweet/', defaults={'name' : 'No val entered'})

@app.route('/tweet/<string:tweet>/')
def parse(tweet):
   listoflinks = main(tweet)
   """print(listoflinks)
   return render_template("show_queries.html", data=listoflinks)
   """
   return json.dumps(listoflinks)

if __name__ == "__main__":
   app.run()
