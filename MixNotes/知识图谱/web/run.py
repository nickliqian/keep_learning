from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('g61.html')

if __name__ == '__main__':
    app.run()