from flask import Flask, render_template
from flask_script import Manager

from pyecharts_app import create_app

app = create_app()
manager=Manager(app)


if __name__ == '__main__':
    manager.run()
