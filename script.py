from flask import Flask, render_template, request, redirect, url_for
import sys
import socket

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        md5 = request.form['md5']
        numWokers = request.form['workerNum']
    
    # here are code for sending md5 and numWorkers to the master
    data = ""
    time = 0
    
    # decode the cracked password
    pwd = data.decode('utf-8')
    return render_template('index.html', pwd=pwd, timeTaken=time)

if __name__ == '__main__':
    app.run(debug=True)