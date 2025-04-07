from pathlib import Path


BASE_SITE = "/xarillian.com"

# Root directory structure
APP_ROOT = Path.cwd()

CONTENT_DIR = APP_ROOT / "content"
DOCS_DIR = APP_ROOT / "docs"
STATIC_DIR = APP_ROOT / "static"
TEMPLATES_DIR = APP_ROOT / "templates"
# Output directories
POSTS_DIR = DOCS_DIR / "blog"
TAGS_FILE = DOCS_DIR / "tags.html"
# CSS directories
CSS_DIR = STATIC_DIR / "styles"
CSS_STYLES_FILE = CSS_DIR / "styles.css"
CSS_BUNDLE_FILE = CSS_DIR / "bundle.css"

# Blog config
MAX_POSTS_PER_PAGE = 7

# Header quotes
QUOTES = [
  'it\'s not the user\'s fault',
  'it\'s not the mountains we conquer, but ourselves',
  'a ship in a harbor is safe, but that is not what ships are built for',
  'everything excellent is as difficult as it is rare',
  'you can just do things',
  'reach heaven by violence!',
  'I like this player. It played well. It did not give up.',
  '...the player believed the universe had spoken to it through the zeroes and ones',
]
