from flask import Flask, render_template, request, url_for, redirect
from stitch import stitch_finder
from convert import detect_text
import os

app = Flask(__name__)

@app.route('/')
@app.route('/home/')
def home():
    return render_template('index.html')


@app.route('/tutorial_page/', methods=["POST", "GET"])
def tutorial_page():
    if request.method == "POST":
        text = request.form["text"]
        #try:
        img = request.files["img"]
        #except:
        #    img = ''

        if img and img.filename.split('.')[-1] in ['jpg', 'jpeg', 'png']:
            img.save("static/images/" + img.filename)

            text = detect_text("static/images/" + img.filename)

            #os.remove("static/images/" + img.filename)

        
        clean_text, stitches = stitch_finder(text)

        
        return render_template('tutorial_page.html', clean_text=clean_text, stitches=stitches)
    
    else:
        return redirect('/home/')


@app.route('/stitches/')
def stitches():
    return render_template('stitches.html') 

app.run(debug=True)
