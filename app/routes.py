import random

from flask import Blueprint, redirect, render_template, render_template_string, url_for

from .utils import QUOTES, get_menu_items


main = Blueprint('main', __name__)


@main.route('/')
def home():
    return redirect(url_for('main.about_me'))


@main.route('/about')
def about_me():
    return render_template('about.html')


@main.route('/random-quote')
def random_quote():
    return random.choice(QUOTES)


@main.route('/menu')
def menu():
    # Currently unused (gross)
    menu_items = get_menu_items()
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
