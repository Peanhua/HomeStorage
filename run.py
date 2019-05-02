#!/usr/bin/env python3

from application import app
from os          import environ

if __name__ == "__main__":
    debug = bool(environ.get("DEBUG"))
    app.run(debug=debug)
