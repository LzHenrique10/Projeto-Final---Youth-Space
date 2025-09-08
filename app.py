from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html', body_class='login-page')

if __name__ == '__main__':
    app.run(debug=True)