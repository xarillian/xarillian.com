import random
import os
from flask import (
  Flask,
  render_template,
  render_template_string,
)

from const import QUOTES

app = Flask(__name__)

app.secret_key = os.urandom(24)
if not app.secret_key:
    raise ValueError("No SECRET_KEY set for Flask application")


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/random-quote')
def random_quote():
  return random.choice(QUOTES)


@app.route('/menu')
def menu():
    menu_items = [
        {'link': 'https://github.com/xarillian', 'display': 'github', 'icon': 'fab fa-github' },
        {'link': 'https://www.linkedin.com/in/austin-heinrich/', 'display': 'linkedin', 'icon': 'fab fa-linkedin'},
    ]

    menu_html = render_template_string(
      """
        <ul>
        {% for item in menu_items %}
            <a href="{{ item.link }}" target="_blank">
              <li><p><i class="{{ item.icon }}"></i> {{ item.display }}</p></li>
            </a>
        {% endfor %}
        </ul>
      """,
      menu_items=menu_items,
    )

    return menu_html


if __name__ == '__main__':
  app.run(debug=True)
