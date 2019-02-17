# -*- coding: utf-8 -*-
# quiz-orm/app.py

import os

from flask import g

from views import *

app.config.update(dict(
    SECRET_KEY='bardzosekretnawartosc',
    DATABASE=os.path.join(app.root_path, baza_plik),
))


@app.before_request
def before_request():
    g.db = baza
    g.db.connect(reuse_if_open=True)


@app.after_request
def after_request(response):
    g.db.close()
    return response


if __name__ == '__main__':
    app.run(debug=True)

