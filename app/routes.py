import random
from flask import Blueprint, redirect, request, render_template, url_for, send_from_directory

from app.blog import render_blog_template, view_post
from app.consts import POSTS_DIR, QUOTES


main = Blueprint('main', __name__)


def is_using_static_blog():
  return POSTS_DIR.exists() and any(POSTS_DIR.iterdir())


@main.route('/')
def home():
  return redirect(url_for('main.about_me'))


@main.route('/blog')
def blog():
  page = request.args.get('page', 1, type=int)
  if is_using_static_blog():
    html_file = f'blog_page_{page}.html'
    if (POSTS_DIR / html_file).exists():
      return send_from_directory(POSTS_DIR, html_file)

  # TODO warning message
  return render_blog_template(page)


@main.route('/blog/<slug>')
def blog_post(slug):
  if is_using_static_blog():
    return send_from_directory(POSTS_DIR, f"{slug}.html")

  # TODO warning message
  return view_post(slug)


@main.route('/about')
def about_me():
  return render_template('about.html')


@main.route('/random-quote')
def random_quote():
  return random.choice(QUOTES)
