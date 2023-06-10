from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contactus')
def contactus():
    return render_template('ContactUs.html')

@app.route('/how-it-works')
def howitworks():
    return render_template('How_it_works.html')

@app.route('/testingpage')
def testingPage():
    return render_template('testingPage.html')

if __name__ == '__main__':
    app.run(debug=True)
