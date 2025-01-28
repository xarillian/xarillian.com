import random
from flask import Blueprint, redirect, render_template, url_for

from app.blog import render_blog_template, view_post
from .utils import QUOTES


main = Blueprint('main', __name__)


@main.route('/')
def home():
  return redirect(url_for('main.about_me'))


@main.route('/blog')
@main.route('/blog/page/<int:page_index>')
def blog(page_index: int = 1):
  return render_blog_template(page_index)


@main.route('/blog/<slug>')
def blog_post(slug):
    return view_post(slug)


@main.route('/about')
def about_me():
  return render_template('about.html')


@main.route('/random-quote')
def random_quote():
  return random.choice(QUOTES)
