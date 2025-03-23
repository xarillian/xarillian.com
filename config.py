import os


class Config:
    """
    Collection of configuration settings for xarillian.com.

    Attributes:
      - SECRET_KEY (str): Securely stores session data. Note: this currently uses a random
                          value. This means session data will not persist.
      - USE_BUNDLE_CSS (bool): If the css served should use styles.css for rapid iteration or a nice bundle.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    USE_BUNDLE_CSS = True # os.environ.get('FLASK_ENV') == 'production'
