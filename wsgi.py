import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    debug = False or os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug)
