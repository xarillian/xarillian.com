import os


class Config:
    """
    Collection of configuration settings for xarillian.com.

    Attributes:
      - SECRET_KEY (str): Securely stores session data. Note: this currently uses a random
                          value. This means session data will not persist.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
