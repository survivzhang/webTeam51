from flask import Flask, render_template, request, redirect, url_for

# initialise Flask app
app = Flask(__name__)  

# define a route for the root URL
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/homepage', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        # 获取表单数据
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 这里应该添加验证用户凭据的逻辑
        # 简单示例，实际应用中需要更完善的处理
        print(f"登录尝试: {email}")
        
        # 登录成功后重定向到欢迎页面
        return redirect(url_for('welcomePage'))
    
    # GET请求时显示首页（包含登录表单）
    return render_template('homepage.html', title="Homepage")

@app.route('/welcomePage')
def welcomePage():
    return render_template('welcome_page.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # 这里应该添加验证和数据库存储逻辑
        # 简单示例，实际应用中需要更完善的处理
        print(f"注册用户: {username}, 邮箱: {email}")
        
        # 注册成功后重定向到首页或欢迎页面
        return redirect(url_for('welcomePage'))
    
    # GET请求时显示注册表单
    return render_template('registration.html', title="Register")
    
@app.route('/logpage')
def login():
    # 记录日志的页面
    return render_template('logpage.html', title="Activity Log")

@app.route('/update')
def update():
    return "<h1>Update Page (Coming Soon)</h1>"

@app.route('/visualisation')
def visualisation():
    return "<h1>Visualisation Page (Coming Soon)</h1>"

@app.route('/sharing')
def sharing():
    return "<h1>Sharing Page (Coming Soon)</h1>"

@app.route('/profile')
def profile():
    return "<h1>Profile Page (Coming Soon)</h1>"

if __name__ == '__main__':
    app.run(debug=True) 