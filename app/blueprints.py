from flask import Blueprint

# 创建蓝图
main = Blueprint('main', __name__)

# 不要在这里导入路由，而是在 create_app 函数中导入
# 这样可以避免循环导入问题