from flask import Flask, redirect, render_template, request

import redis

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

redisdb = redis.Redis(host='redis', port=6379, db=0)

@app.route('/')
def index():
	shoppinglist = redisdb.lrange("list", 0, -1)
	return render_template('index.html', shoppinglist_formatted=list(shoppinglist))

@app.route('/addvalue', methods=['POST'])
def add_value():
	value = request.form['value']
	app.logger.info("Received entry " + value + ", adding to shopping list... TEST")
	print("Received entry " + value + ", adding to shopping list... TEST")
	redisdb.rpush("list", value)
	return redirect("/", code=302)

@app.route('/removevalue', methods=['POST'])
def remove_value():
	value = request.form['value']
	app.logger.info("Received entry " + value + ", removing from shopping list... TEST")
	print("Received entry " + value + ", removing from shopping list... TEST")
	redisdb.lrem("list", 0, value)
	return redirect("/", code=302)

if __name__ == '__main__':
	handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	app.run(host="0.0.0.0", port=8000)