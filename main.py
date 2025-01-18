from flask import Flask, render_template, request, url_for, redirect
from stitch import stitch_finder
from ocr import image_to_text
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
        try:
            img = request.form["img"]
        except:
            img = ''

        if img and img.filename.split('.')[-1] in ['jpg', 'jpeg', 'png']:
            img.save("images/" + img.filename)

            text = image_to_text(img)

            os.remove("images/" + img.filename)

        
        clean_text, stitches = stitch_finder(text)

        
        return render_template('tutorial_page.html', clean_text=clean_text, stitches=stitches)
    
    else:
        return redirect('/home/')


@app.route('/stitches/')
def stitches():
    return render_template('stitches.html') 

app.run(debug=True)
