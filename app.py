from flask import Flask, render_template, redirect, request
import shutil
from datetime import datetime

from googletrans import *
translator = Translator()
import Caption_it

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# __name__ == __main__
app = Flask(__name__)


import pip
pip.main(["gtts", package])
pip.main(["googletrans", package])

from gtts import gTTS


@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/', methods= ['POST'])
def marks():
    if request.method == 'POST':
        f = request.files['userfile']
        l = request.form.get('lang')
        path = "./static/{}".format(f.filename)# ./static/images.jpg
        f.save(path)
        
        caption = Caption_it.caption_this_image(path)
        caption = translator.translate(caption, dest = l).text
        
        time=datetime.now().strftime("_%H_%M_%S")
        name="test"+time+".mp3"
        #name=`test${time}.mp3
        gTTS(caption,lang=l).save(name)
        shutil.move(name, "./static/"+name)
        audio="./static/"+name
        result_dic = {
        'image' : path,
		'caption' : caption,
        'audio' : audio
		}
    return render_template("index.html", your_result =result_dic)

if __name__ == '__main__':
	# app.debug = True
	# due to versions of keras we need to pass another paramter threaded = Flase to this run function
    app.run(debug = False, threaded = False)
