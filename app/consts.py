from pathlib import Path


# Directory structure
APP_ROOT = Path(__file__).parent
STATIC_DIR = APP_ROOT / 'static'
TEMPLATES_DIR = APP_ROOT / 'templates'
RAW_POSTS_DIR = STATIC_DIR / 'raw_posts'
POSTS_DIR = STATIC_DIR / 'posts'
TAGS_FILE = POSTS_DIR / 'tags.html'
CSS_DIR = STATIC_DIR / 'styles'
CSS_STYLES_FILE = CSS_DIR / 'styles.css'
CSS_BUNDLE_FILE = CSS_DIR / 'bundle.css'


# Blog
MAX_POSTS_PER_PAGE = 7


# Main page quotes
QUOTES = [
  'it\'s not the user\'s fault',
  'it\'s not the mountains we conquer, but ourselves',
  'a ship in a harbor is safe, but that is not what ships are built for',
  'everything excellent is as difficult as it is rare',
  'you can just do things',
  'reach heaven by violence!',
  'I like this player. It played well. It did not give up.',
  '...the player believed the universe had spoken to it through the 0s and 1s',
]
