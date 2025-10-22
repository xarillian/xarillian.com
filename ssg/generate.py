import shutil
from ssg.bundle_css import bundle_css
from ssg.blog import Blog, BlogPost
from ssg.config import BLOG_DIR, DOCS_DIR, MAX_POSTS_PER_PAGE, PAGES_DIR, POSTS_DIR
from ssg.render import render_template


def generate_blog(blog: Blog):
  print("Generating blog posts...")
  print(f"Found {len(blog.posts)} posts to render.")

  POSTS_DIR.mkdir(parents=True, exist_ok=True)
  (DOCS_DIR / "blog").mkdir(exist_ok=True)

  for post in blog.posts:
    rendered_content = post.render_content()
    post_dir = POSTS_DIR / post.slug
    post_dir.mkdir(parents=True, exist_ok=True)
    output_path = post_dir / "index.html"
    with output_path.open('w', encoding='utf-8') as file:
      file.write(render_template("post.html", post=rendered_content))

  print("Generating blog index...")
  total_pages = (len(blog.posts) + MAX_POSTS_PER_PAGE - 1) // MAX_POSTS_PER_PAGE + 1
  for page in range(1, total_pages):
    paginated_posts = blog.get_paginated_posts(page)
    if page == 1:
      output_path_main = DOCS_DIR / "blog" / "index.html"
      output_path_page_1 = DOCS_DIR / "blog" / "page" / "1" / "index.html"
      output_path_page_1.parent.mkdir(parents=True, exist_ok=True)

      html = render_template(
        "blog.html",
        posts=paginated_posts["posts"],
        current_page=paginated_posts["page"],
        total_pages=paginated_posts["pages"],
      )

      output_path_main.parent.mkdir(parents=True, exist_ok=True)
      output_path_main.write_text(html, encoding='utf-8')
      output_path_page_1.write_text(html, encoding='utf-8')
    else:
      output_path = DOCS_DIR / "blog" / "page" / str(page) / "index.html"
      output_path.parent.mkdir(parents=True, exist_ok=True)
      with output_path.open('w', encoding='utf-8') as file:
        file.write(render_template(
          "blog.html",
          posts=paginated_posts["posts"],
          current_page=paginated_posts["page"],
          total_pages=paginated_posts["pages"],
        ))


def generate_page(markdown_file, output_name: str):    
    page = BlogPost.from_file(markdown_file).render_content()
    html = render_template("post.html", post=page)
    
    (DOCS_DIR / f"{output_name}.html").write_text(html, encoding="utf-8")
    output_dir = DOCS_DIR / output_name
    output_dir.mkdir(exist_ok=True)
    (output_dir / "index.html").write_text(html, encoding="utf-8")


def generate_tags(blog: Blog):
  print("Generating tags...")
  tags = blog.get_all_tags()
  print(f"Found {len(tags)} tags to render.")

  tag_sizes = {
    tag: round(1 + 1 * (count - min(tags.values())) / max(1, max(tags.values()) - min(tags.values())), 1)
    for tag, count in tags.items()
  }

  tags_dir = DOCS_DIR / "tags"
  tags_dir.mkdir(parents=True, exist_ok=True)

  with (tags_dir / "index.html").open('w', encoding='utf-8') as file:
    file.write(render_template("tags.html", tag_sizes=tag_sizes, tag_counts=tags))

  for tag in tags:
    tag_dir = tags_dir / tag
    tag_dir.mkdir(parents=True, exist_ok=True)
    tag_file = tag_dir / "index.html"
    posts = blog.get_posts_by_tag(tag)
    tag_file.write_text(render_template(
      "tagged_posts.html", 
      tag=tag, 
      posts=posts,
      total_pages=0,
      current_page=1
    ), encoding="utf-8")

def generate_site():
  print("Starting site generation...")

  directory_listing = (
    f"Docs Directory: {DOCS_DIR}, ",
    f"Content Directory: {BLOG_DIR}, "
    f"Posts Directory: {POSTS_DIR}, "
  )

  print(directory_listing)

  bundle_css()

  if DOCS_DIR.exists():
    shutil.rmtree(DOCS_DIR)
  DOCS_DIR.mkdir(exist_ok=True)

  shutil.copytree("static/styles", DOCS_DIR / "styles", dirs_exist_ok=True)
  shutil.copytree("static/images", DOCS_DIR / "images", dirs_exist_ok=True)
  shutil.copy("static/favicon.png", DOCS_DIR / "favicon.png")
  shutil.copy("static/sitemap.xml", DOCS_DIR / "sitemap.xml")
  shutil.copy("robots.txt", DOCS_DIR / "robots.txt")

  blog = Blog(BLOG_DIR, MAX_POSTS_PER_PAGE)

  generate_blog(blog)
  generate_tags(blog)

  generate_page(PAGES_DIR / "about.md", "about")
  shutil.copy(DOCS_DIR / "about.html", DOCS_DIR / "index.html")
  print("Index page generated!")

  page_404 = render_template("404.html")
  (DOCS_DIR / "404.html").write_text(page_404, encoding="utf-8")
  print("404 page generated.")

  (DOCS_DIR / ".nojekyll").touch()
  print("Jekyll bypass file created.")

  (DOCS_DIR / "CNAME").write_text("xarillian.com", encoding="utf-8")

  print(f"Site generated to {DOCS_DIR}")


if __name__ == "__main__":
  generate_site()
