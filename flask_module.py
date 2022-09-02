from datetime import datetime
from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def submit():
    if request.method == "POST":
        username = request.values['username']
        password = request.values['password']
        if username=="root" and password=="1234":
            return "Welcome!"
        else: return "Something is error"
        
    return"""
    <form method='POST' action="">
        <p>account: <input type='text' name='username' /></p>
        <p>password: <input type='text' name='password' /></p>
        <p><button type='submit'>確定</button></p>
    </form>
    """
@app.route("/hello/<string:name>")
def hello(name):
    now = datetime.now()
    return render_template("hello.html", **locals())

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='5000', debug=False)
    app.run()
    