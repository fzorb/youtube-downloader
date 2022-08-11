from flask import Flask, render_template, request, redirect, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import subprocess

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per second"]
)
#limit post
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ytdl = request.form.get("link")
        #get video url using youtube-dl library and get the output
        if "youtube" not in ytdl:
            return redirect("/")
        if "&" in ytdl:
            return redirect("/")
        result = subprocess.getoutput("youtube-dl --get-url {}".format(ytdl))
        #parse result
        result = result.split("\n")
        return render_template("result.j2", video=result[0], audio=result[1])
    return render_template("index.j2")