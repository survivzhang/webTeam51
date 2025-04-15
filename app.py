from flask import Flask, render_template

# initialise Flask app
app = Flask(__name__)  

# define a route for the root URL
@app.route('/') 
def home():
    return render_template('index.html')  


@app.route('/homepage')
def about():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True) 