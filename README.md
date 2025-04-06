# xarillian.com

xarillian.com is my personal website. I built it for fun, but I also built it to showcase my work, give a space for my
writing and to tell my story on the web. It is a dissolution of my privacy on the web, as well; a functional self-dox
of everything I've been up to for the past two decades. I just think it should be free.

Built with Flask and HTMX, as I'm trying to be minimal and extra at the same time.

## Setup Instructions
1. Clone the repository:

```
git clone https://github.com/xarillian/xarillian.com.git
cd xarillian.com
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the development server:

```bash
flask run
```

...or just access it at https://xarillian.com

## Adding Blog Posts

Blog posts should be added to the `app/static/raw_posts` directory as Markdown files with frontmatter. Example format:

```markdown
---
title: My Blog Post
date: 2024-03-21
summary: A short summary of the post
tags: personal, technology
toc: true
---

[Blog content goes here]
```

After adding new posts, run `python -m app.buld.build_blog` to regenerate the static files.

## Deployment

The site includes deployment scripts for setting up on a Ubuntu server:

- `install_application.sh` - Sets up dependencies and creates the initial environment
- `start_application.sh` - Starts the Gunicorn server
- `stop_application.sh` - Stops the running server

The application is designed to serve static pre-rendered blog posts in production for optimal performance.