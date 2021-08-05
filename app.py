import flask
import gunicorn

from flask import Flask, request, render_template, session, redirect

app = flask.Flask(__name__, template_folder='templates', static_folder = 'assets')

@app.route('/')
def main():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run()
    
