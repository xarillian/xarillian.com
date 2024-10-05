import os


class Config:
    """
      Collection of configuration settings for xarillian.com.

      Attributes:
        - SECRET_KEY (str): Securely stores session data.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
