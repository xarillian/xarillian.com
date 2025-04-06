import shutil
from ssg.blog import Blog
from ssg.bundle_css import bundle_css
from ssg.config import CONTENT_DIR, DOCS_DIR, MAX_POSTS_PER_PAGE, POSTS_DIR, QUOTES
from ssg.render import render_template


def generate_blog(blog: Blog):
  print("Generating blog posts...")
  print(f"Found {len(blog.posts)} posts to render.")
  for post in blog.posts:
    rendered_content = post.render_content()
    slug = post.slug
    output_path = POSTS_DIR / f"{slug}.html"
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    with output_path.open('w', encoding='utf-8') as file:
        file.write(render_template("post.html", post=rendered_content))

  print("Generating blog index...")
  for page in range(1, (len(blog.posts) + MAX_POSTS_PER_PAGE - 1) // MAX_POSTS_PER_PAGE + 1):
    paginated_posts = blog.get_paginated_posts(page)
    output_path = DOCS_DIR / f"blog_page_{page}.html"
    with output_path.open('w', encoding='utf-8') as file:
        file.write(render_template("blog.html", **paginated_posts))


def generate_tags(blog: Blog):
  print("Generating tags...")
  print(f"Found {len(blog.get_all_tags())} tags to render.")
  tags = blog.get_all_tags()
  tag_sizes = {
    tag: round(1 + 2 * (count - min(tags.values())) / max(1, max(tags.values()) - min(tags.values())), 1)
    for tag, count in tags.items()
  }
  with (DOCS_DIR / "tags.html").open('w', encoding='utf-8') as file:
    file.write(render_template("tags.html", tag_sizes=tag_sizes), encoding="utf-8")

  for tag in tags:
    posts = blog.get_posts_by_tag(tag)
    output_path = DOCS_DIR / f"tag_{tag}.html"
    output_path.write_text(render_template("tagged_posts.html", tag=tag, posts=posts), encoding="utf-8")


def generate_site():
  print("Starting site generation...")

  bundle_css()

  DOCS_DIR.mkdir(exist_ok=True)

  shutil.copytree("static/styles", DOCS_DIR / "styles", dirs_exist_ok=True)
  shutil.copytree("static/images", DOCS_DIR / "images", dirs_exist_ok=True)
  shutil.copy("static/favicon.png", DOCS_DIR / "favicon.png")
  shutil.copy("static/sitemap.xml", DOCS_DIR / "sitemap.xml")
  shutil.copy("robots.txt", DOCS_DIR / "robots.txt")

  blog = Blog(CONTENT_DIR, MAX_POSTS_PER_PAGE)

  generate_blog(blog)
  generate_tags(blog)

  index = render_template("about.html", quotes=QUOTES)
  with (DOCS_DIR / "index.html").open('w', encoding='utf-8') as file:
    file.write(index, encoding="utf-8")

  page_404 = render_template("404.html")
  with (DOCS_DIR / "404.html").open('w', encoding='utf-8') as file:
    file.write(page_404, encoding="utf-8")

  print(f"Site generated to {DOCS_DIR}")


if __name__ == "__main__":
  generate_site()
