from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import markdown2
from flask import render_template, abort
from markupsafe import Markup

from app.frontmatter import FrontmatterException, frontmatter


MAX_PER_PAGE = 7


@dataclass
class BlogPost:
  """Dataclass describing the content and metadata of a blog post."""
  title: str
  date: datetime
  content: str
  url: str
  summary: Optional[str] = None
  tagline: Optional[str] = None
  toc: bool = False
  toc_html: Optional[str] = None
  tags: List[str] = field(default_factory=list)

  @classmethod
  def from_file(cls, file_path: Path) -> "BlogPost":
    """Create a BlogPost instance from a markdown file."""
    content = frontmatter(file_path.read_text(encoding='utf-8'))

    return cls(
      title=content.metadata.get('title', ''),
      date=content.metadata.get('date', datetime(1996, 5, 18)),
      content=content.content,
      summary=content.metadata.get('summary'),
      tagline=content.metadata.get('tagline'),
      url=f"/blog/{file_path.stem}",
      toc=content.metadata.get('toc', False),
      tags=content.metadata.get('tags', []),
    )

  def render_content(self, markdown_extras: Optional[list] = None) -> "BlogPost":
    """Render markdown content to HTML and return a new BlogPost instance."""
    if markdown_extras is None:
      markdown_extras = ['fenced-code-blocks', 'tables', 'break-on-newline']
    if self.toc:
      markdown_extras.extend(['toc', 'header-ids'])

    rendered = markdown2.markdown(self.content, extras=markdown_extras)

    return BlogPost(
        title=self.title,
        date=self.date,
        content=Markup(rendered),
        url=self.url,
        summary=self.summary,
        tagline=self.tagline,
        toc=self.toc,
        toc_html=Markup(rendered.toc_html) if self.toc else None,
        tags=self.tags,
    )


class Blog:
  """Handles loading and pagination of blog posts."""
  def __init__(self, posts_dir: Path):
    self.posts_dir = posts_dir
    self.max_per_page = MAX_PER_PAGE
    self._posts = None

  @property
  def posts(self):
    """Lazy load and cache posts."""
    if self._posts is None:
      self._posts = self._load_all_posts()
    return self._posts

  def _load_all_posts(self) -> list[BlogPost]:
    posts = []
    for post_file in self.posts_dir.glob('*.md'):
      try:
        posts.append(BlogPost.from_file(post_file))
      except FrontmatterException as ex:
        print(f"Error loading post {post_file}: {ex}")
    return sorted(posts, key=lambda p: p.date, reverse=True)

  def get_paginated_posts(self, page: int = 1) -> dict:
    start = (page - 1) * self.max_per_page
    end = start + self.max_per_page

    return {
      'posts': self.posts[start:end],
      'total': len(self.posts),
      'page': page,
      'pages': (len(self.posts) + self.max_per_page - 1) // self.max_per_page
    }

  def get_post(self, slug: str) -> Optional[BlogPost]:
    post_file = self.posts_dir / f"{slug}.md"
    if not post_file.exists():
      return None

    return BlogPost.from_file(post_file).render_content()


blog = Blog(Path('app/static/posts'))


def render_blog_template(page_index: int = 1):
  """Render the blog listing page."""
  result = blog.get_paginated_posts(page_index)
  return render_template(
    'blog.html',
    posts=result['posts'],
    current_page=result['page'],
    total_pages=result['pages'],
  )

def view_post(slug: str):
  """Render a single blog post."""
  post = blog.get_post(slug)
  if post is None:
    abort(404)
  return render_template('post.html', post=post)
