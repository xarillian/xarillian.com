from flask import render_template

from app import create_app
from app.blog import Blog
from app.consts import POSTS_DIR, RAW_POSTS_DIR, TAGS_FILE, TEMPLATES_DIR


def create_static_blog_files():
  """
  Prebuild script to convert Markdown blog posts to static HTML files.
  This should be run during deployment to generate static files.
  """
  POSTS_DIR.mkdir(parents=True, exist_ok=True)

  app = create_app()

  with app.test_request_context():
    print(f"Starting blog prebuild with templates from {TEMPLATES_DIR}")
    blog = Blog(RAW_POSTS_DIR)

    print(f"Found {len(blog.posts)} blog posts to pre-render.")
    for post in blog.posts:
      rendered_post = post.render_content()
      post_slug = post.url.split('/')[-1]
      post_path = POSTS_DIR / f"{post_slug}.html"

      with post_path.open('w', encoding='utf-8') as file:
        html = render_template('post.html', post=rendered_post)
        file.write(html)

      print(f"Rendered {post_path}.")

    total_posts = len(blog.posts)
    max_per_page = blog.max_per_page
    total_pages = (total_posts + max_per_page - 1) // max_per_page

    for page in range(1, total_pages + 1):
      paginated = blog.get_paginated_posts(page)
      page_path = POSTS_DIR / f'blog_page_{page}.html'

      with page_path.open('w', encoding='utf-8') as file:
        html = render_template(
          'blog.html',
          posts=paginated['posts'],
          current_page=paginated['page'],
          total_pages=paginated['pages'],
        )
        file.write(html)

      print(f"Rendered blog index page {page}/{total_pages}: {page_path}")

    print("Completed creation of static blog files.")

    tag_counts = blog.get_all_tags()
    max_count = max(tag_counts.values()) if tag_counts else 1
    min_count = min(tag_counts.values()) if tag_counts else 1
    tag_sizes = {}

    for tag, count in tag_counts.items():
      if max_count == min_count:
        tag_sizes[tag] = 2
      else:
        size = 1 + 2 * (count - min_count) / (max_count - min_count)
        tag_sizes[tag] = round(size, 1)

    with TAGS_FILE.open('w', encoding='utf-8') as file:
      html = render_template('tags.html', tag_sizes=tag_sizes)
      file.write(html)
    print(f"Rendered tag cloud page: {TAGS_FILE}")

    for tag in tag_counts:
      posts = blog.get_posts_by_tag(tag)
      tag_path = POSTS_DIR / f'tag_{tag}.html'
      with tag_path.open('w', encoding='utf-8') as file:
        html = render_template('tagged_posts.html', tag=tag, posts=posts)
        file.write(html)

      print(f"Rendered tag page for '{tag}': {tag_path}")


if __name__ == '__main__':
  create_static_blog_files()
