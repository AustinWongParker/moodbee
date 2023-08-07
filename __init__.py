from flask import Flask, render_template, url_for, redirect, session, request

app = Flask(__name__)
app.secret_key = 'dev'

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/track')
def track():
    return render_template('track.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contact-us')
def contactus():
    return render_template('ContactUs.html')

@app.route('/how-it-works')
def howitworks():
    return render_template('How_it_works.html')

@app.route('/testingpage')
def testingPage():
    return render_template('testingPage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/post-comment', methods=['POST'])
def post_comment():
    selected_image = request.form.get('selected-image')
    comment = request.form.get('comment')

    # Store the data in the session
    session['selected_image'] = selected_image
    session['comment'] = comment

    # Redirect back to the page with the form
    return redirect(url_for('display_comment'))

@app.route('/display_comment', methods=['POST', 'GET'])
def display_comment():
    if request.method == 'POST':
        selected_image = request.form.get('selected_image')
        comment = request.form.get('comment')

        # Store the data in the session
        session['selected_image'] = selected_image
        session['comment'] = comment

        # Redirect to the same page to prevent resubmission on page refresh
        return redirect(url_for('display_comment'))

    # If it's a GET request or after form submission, display the stored data
    selected_image = session.get('selected_image')
    comment = session.get('comment')

    return render_template('display_comment.html', selected_image=selected_image, comment=comment)


if __name__ == '__main__':
    app.run(debug=True)
