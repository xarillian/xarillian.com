import random
import os
from flask import (
  Flask,
  render_template,
  render_template_string,
  request,
  session,
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
    if request.headers.get('HX-Request') == 'true':
      session['menu_visible'] = not session.get('menu_visible', False)
    is_visible = session.get('menu_visible', True)

    menu_items = [
        {'link': 'https://github.com/xarillian', 'display': 'github'},
    ]

    menu_html = render_template_string(
      """
        <ul>
        {% for item in menu_items %}
            <li><a href="{{ item.link }}" target="_blank">{{ item.display }}</a></li>
        {% endfor %}
        </ul>
      """,
      menu_items=menu_items,
      is_visible=is_visible
    )

    return menu_html


if __name__ == '__main__':
  app.run(debug=True)
