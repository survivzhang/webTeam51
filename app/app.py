from flask import Flask, render_template

# initialise Flask app
app = Flask(__name__)  

# define a route for the root URL
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/homepage')
def about():
    return render_template('homepage.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')

@app.route('/update')
def update():
    return render_template('update.html', title='Update')

@app.route('/visualisation')
def visualisation():
    return render_template('visualisation.html', title='Visualisation')

@app.route('/sharing')
def sharing():
    return render_template('sharing.html', title='Sharing')


@app.route('/welcomePage')
def welcomePage():
    return render_template('welcome_page.html')
if __name__ == '__main__':
    app.run(debug=True) 