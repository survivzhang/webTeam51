from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms import LoginForm, RegistrationForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/homepage', methods=['GET', 'POST'])
def about():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        
        print(f"登录尝试: {email}, 记住我: {remember_me}")
        
        flash('Login requested for user {}'.format(email))
        return redirect(url_for('main.welcomePage'))
    
    return render_template('homepage.html', title="Homepage", form=form)

@main.route('/welcomePage')
def welcomePage():
    return render_template('welcome_page.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        print(f"注册用户: {username}, 邮箱: {email}")
        
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.welcomePage'))
    
    return render_template('registration.html', title="Register", form=form)
    
@main.route('/logpage')
def login():
    return render_template('logpage.html', title="Activity Log")

@main.route('/update')
def update():
    return "<h1>Update Page (Coming Soon)</h1>"

@main.route('/visualisation')
def visualisation():
    return "<h1>Visualisation Page (Coming Soon)</h1>"

@main.route('/sharing')
def sharing():
    return "<h1>Sharing Page (Coming Soon)</h1>"

@main.route('/profile')
def profile():
    return "<h1>Profile Page (Coming Soon)</h1>" 