import random
from flask import Flask, render_template

from const import QUOTES

app = Flask(__name__)


@app.route('/')
def home():
  return render_template('index.html')

@app.route('/random-quote')
def random_quote():
  return random.choice(QUOTES)

if __name__ == '__main__':
  app.run(debug=True)
