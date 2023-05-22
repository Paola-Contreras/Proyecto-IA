from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

app = Flask(__name__)
@app.route("/")
@app.route("/index")
def index():
    print('in')
if __name__ == '__main__':
    app.run()
