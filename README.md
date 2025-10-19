# xarillian.com

xarillian.com is my personal website. I built it for fun, but I also built it to showcase my work, give a space for my writing, and to tell my story on the web. 

Built with Python on top of Jinja2 for templating. Uses a custom static-site generator.

## Setup Instructions

```bash
git clone https://github.com/xarillian/xarillian.com.git
cd xarillian.com
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m ssg.generate
python -m http.server --directory docs
```

...or just access it at https://xarillian.com

## Adding Blog Posts

Blog posts should be added to the `content` directory as Markdown files with frontmatter. Example format:

```markdown
---
title: My Blog Post
date: 2024-03-21
summary: A short summary of the post
tags: personal,technology
toc: true
---

[Blog content goes here]
```

After adding a post, the site can be regenerated:

```bash
python -m ssg.generate
```
