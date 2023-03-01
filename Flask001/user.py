from flask import Blueprint, request, render_template, redirect

# 导入模块

from datetime import datetime, timedelta

import flask
import jwt
import pymysql as pymysql
from flask import request, Flask, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from time import strftime, gmtime
import requests
import os
from flask_cors import CORS

user = Blueprint('user', __name__)

# 创建数据库
DBHOST = '127.0.0.1'
DBUSER = 'root'
DBPASS = '123456'
DBNAME = 'usermessage127135'
DBTYPE = 'utf8'
# DBPORT = 8000

try:
    usermessage127135 = pymysql.connect(
        host='127.0.0.1',
        user="root",
        # port=8000,
        password="123456"
    )
    # 创建表格
    mycursor = usermessage127135.cursor()
    # mycursor.execute('DROP DATABASE IF EXISTS usermessage127135')
    mycursor.execute("CREATE DATABASE IF NOT EXISTS usermessage127135")

    db = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME, charset=DBTYPE)
    print('数据库usermessage127135连接成功')
    cur = db.cursor()
    # cur.execute('DROP TABLE IF EXISTS TODOLIST')
    sql1 = '''
    CREATE TABLE IF NOT EXISTS USERMESSAGE1271(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username1 VARCHAR(1000),
    password1 VARCHAR(1000))'''

    cur.execute(sql1)

    print('表格创建成功')
    cur.close()
except pymysql.Error as e:
    print('表格创建失败：' + str(e))

# 初始化
CORS(user)
SECRET_KEY = '123456'
user.secret_key = "1271"
ALGORITHM = "HS256"

# uri = 'mysql+pymysql://root:123456@127.0.0.1:3306/usermessage127135'
# app.config['SQLALCHEMY_DATABASE_URI'] = uri

# db = SQLAlchemy(app)

# 链接数据库
db = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME, charset=DBTYPE)


# 设置向userdata表格插入数据的函数
def insert_dbuser(username1, password1):
    cursor = db.cursor()
    todolist_sql1 = "INSERT INTO `USERMESSAGE1271` (`username1`, `password1`) VALUES(" \
                    "%s, %s); "
    cursor.execute(todolist_sql1, (username1, password1))
    db.commit()
    id001 = cursor.lastrowid
    return id001


# JWT鉴权的函数，用来验证token
def authorized_user(data):
    try:
        token = data["token"]
        input_username = data["username"]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(username)
        if username == input_username:
            return username
    except Exception as e:
        print(e)
        return jsonify(code=403, message="无法检验token")
        # raise HTTPException(
        # status_code=HTTP_401_UNAUTHORIZED,
        # detail="认证失败,无权查看",
        # headers={"WWW-Authenticate": "Bearer"}, )


# 函数
# 用来将密码用加盐哈希算法加密的算法
'''def generate_password_hash(s: str):
    # 随机生成长度为4的盐值
    salt = "".join([random.choice(string.ascii_lowercase) for i in range(4)])

    # 拼接原始密码和盐值
    s = s + salt

    # 对加入盐值的字符串加密
    _md5 = hashlib.md5()
    _md5.update(s.encode("utf-8"))
    return salt + "$" + _md5.hexdigest()  # 返回 盐值+哈希值 的字符串
    '''


# 注册功能（我还没想好要怎么和前端对接）
@user.route('/user', methods=['POST'])
def register():
    try:
        register_json = request.get_json()  # 获取json数据
        print(register_json)
        get_username = register_json.get("username")
        # 检测用户名是否重复（还没做，后面写）
        '''cursor = db.cursor()
        sql_search_onepiece = "SELECT * FROM USERMESSAGE1271 where username1 = %r"  # 我不知道为啥%d不行，%s也不行，但是%r就可以跑了...
        cursor.execute(sql_search_onepiece,get_username )
        a = cursor.fetchall()
        print(a)
        if a != 0:
            return jsonify(message="该用户名已被注册！")'''
        get_password = register_json.get("password")
        get_checkPassword = register_json.get("checkPassword")
        if not all([get_username, get_password, get_checkPassword]):
            return jsonify(message="您的信息录入不完全，请检查")
        # ps1 = get_password.strip()
        # ps2 = get_checkPassword.strip()
        # if ps1 != ps2:
        if get_password != get_checkPassword:
            return jsonify(message="两次密码输入不一致")
        get_password_hash = generate_password_hash(get_password)
        new_id = insert_dbuser(get_username, get_password_hash)
        data1 = {"id": new_id, "username": get_username}
        return jsonify(code=200, message="success", data=data1)
    except Exception as e:
        print(e)
        # return jsonify(message="出错了！请查看是否正确访问！")
        return jsonify(code=404, message="该活动不存在")


# 登陆功能
@user.route('/user/login', methods=['POST'])
def login():
    try:
        login_json = request.get_json()  # 获取json数据
        cursor = db.cursor()
        sql_search_onepiece = "SELECT * FROM USERMESSAGE1271 where username1 = %s"  # 我不知道为啥%d不行，%s也不行，但是%r就可以跑了...
        get_username = login_json.get("username")
        get_password = login_json.get("password")
        # 这里还缺一个检测用户是否注册的方法
        cursor.execute(sql_search_onepiece, get_username)
        myresult = cursor.fetchall()
        # print(myresult)
        mr = myresult[0]
        # token相关
        password_data = str(mr[2])
        ret = check_password_hash(password_data, str(get_password))
        '''print(mr)
        print(data1)
        print(password_data)
        print(get_username)
        print(get_password)
        print(ret)'''
        if ret:
            access_token_expires = timedelta(minutes=60)
            expire = datetime.utcnow() + access_token_expires
            payload = {
                "sub": get_username,
                "exp": expire
            }
            # 生成Token,返回给前端
            access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
            # return {"access_token": access_token, "token_type": "bearer"}
            data1 = {"id": str(mr[0]), "username": get_username, "token": access_token}
            return jsonify(code=200, message="success", data=data1)  # 返回的数据的顺序有问题，我还没改
        else:
            return jsonify(code=401, message="密码错误！")
    except Exception as e:
        print(e)
        # return jsonify(message="出错了！请查看是否正确访问！")
        return jsonify(code=404, message="该活动不存在")
