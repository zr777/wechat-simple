# -*- coding: utf-8 -*-

from wxapp import app

if __name__ == "__main__":
    app.debug = app.config['DEBUG']
    app.run(host='127.0.0.1', port=8000)
