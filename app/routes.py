import random
from flask import Blueprint, redirect, request, render_template, url_for, send_from_directory

from app.blog import Blog, render_blog_template, view_post
from app.consts import POSTS_DIR, QUOTES, RAW_POSTS_DIR


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


@main.route('/tags')
def tags():
  if is_using_static_blog():
    return send_from_directory(POSTS_DIR, 'tags.html')

  blog_obj = Blog(RAW_POSTS_DIR)
  tag_counts = blog_obj.get_all_tags()
  max_count = max(tag_counts.values()) if tag_counts else 1
  min_count = min(tag_counts.values()) if tag_counts else 1

  tag_sizes = {}
  for tag, count in tag_counts.items():
    if max_count == min_count:
      tag_sizes[tag] = 2
    else:
      # Scale between 1 and 3em
      size = 1 + 2 * (count - min_count) / (max_count - min_count)
      tag_sizes[tag] = round(size, 1)

  return render_template('tags.html', tag_sizes=tag_sizes)


@main.route('/tags/<tag>')
def tagged_posts(tag):
  if is_using_static_blog():
    return send_from_directory(POSTS_DIR, f'tag_{tag}.html')

  blog_obj = Blog(RAW_POSTS_DIR)
  posts = blog_obj.get_posts_by_tag(tag)
  return render_template('tagged_posts.html', tag=tag, posts=posts)



@main.route('/about')
def about_me():
  return render_template('about.html')


@main.route('/random-quote')
def random_quote():
  return random.choice(QUOTES)
