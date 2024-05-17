from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def ShowMain():
    return render_template('index.html')
@app.route("/view")
def View():
    return render_template('view.html')

@app.route("/create")
def Create():
    return render_template('create.html')

@app.route("/login")
def Login():
    return render_template('login.html')

@app.route("/sign")
def Sign():
    return render_template('sign.html')

@app.route("/FAQs")
def FAQs():
    return render_template('FAQs.html')

@app.route("/about")
def about():
    return render_template('about.html')