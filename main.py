from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')


@app.route('/tutorial_page/', methods=["POST", "GET"])
def tutorial_page():
    if request.method == "POST":
        text = request.form["text"]
        img = request.form["img"]

        if img:
            # img to text code
            pass

        
        return render_template('tutorial_page.html')
app.run()