import argparse

from app import create_app


app = create_app()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help="Run the app in debug mode")
    args = parser.parse_args()

    app.run(debug=args.debug)
