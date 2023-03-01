# 导入模块

import flask

import jwt
import pymysql as pymysql
from flask import request, jsonify, Blueprint
from flask_cors import CORS

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

    sql3 = '''
            CREATE TABLE IF NOT EXISTS DOWNLOAD1271(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name1 VARCHAR(1000),
            artist1 VARCHAR(1000),
            album1 VARCHAR(1000),
            duration1 TIME,
            rid1 INT)'''

    cur.execute(sql3)
    print('表格创建成功')
    cur.close()
except pymysql.Error as e:
    print('表格创建失败：' + str(e))

# 初始化
history = Blueprint('history', __name__)
CORS(history)
SECRET_KEY = '123456'
history.secret_key = "1271"
ALGORITHM = "HS256"

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


# 设置向history表格插入数据的函数
# def insert_dbhistory(name1, artist1, album1, duration1, fav1, rid1):
def insert_dbhistory(list1):
    cursor = db.cursor()
    todolist_sql2 = "INSERT INTO `HISTORY1271` (`name1`, `artist1`, `album1`, `duration1`, `fav1` ,`rid1`) VALUES(" \
                    "%s,%s,%s,%s,%s,%s); "
    for info in list1:
        cursor.execute(todolist_sql2,
                       (info["name"], info["artist"], info["album"], info["duration"], 0, info["rid"]))
        db.commit()

    cursor.close()
    db.close()
    # cursor.execute(todolist_sql2, (name1, artist1, album1, duration1, fav1, rid1))
    # db.commit()


# 设置向DOWNLOAD表格插入数据的函数
def insert_dbdownload(name, artist, album, duration, rid):
    cursor = db.cursor()
    todolist_sql2 = "INSERT INTO `DOWNLOAD1271` (`name1`, `artist1`, `album1`, `duration1`,`rid1`) VALUES(" \
                    "%s,%s,%s,%s,%s); "
    cursor.execute(todolist_sql2, (name, artist, album, duration, rid))
    db.commit()

    cursor.close()
    db.close()


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


# 修改收藏功能
@history.route('/user/history/lc', methods=['PUT'])  # 我有点疑惑这里的方法
# def history_lc(id,fav):
def history_lc():
    try:
        judge = authorized_user(request.headers.get("Authorization"))
        print(judge)
        if judge:
            change_json = request.get_json()  # 获取json数据
            print(change_json)
            get_id = change_json.get("id")
            get_fav = change_json.get("fav")
            cursor = db.cursor()
            # 查找表格里对应的line
            sql_update_done = "UPDATE HISTORY1271 SET fav1 = %s where id = %s"
            id1 = int(get_id)
            fav1 = int(get_fav)
            cursor.execute(sql_update_done, (fav1, id1))
            db.commit()  # 这一句究竟该丢到哪里，放在这里还是放在两行后？
            # 展示一下
            sql3 = "SELECT * FROM HISTORY1271 where id = %s"
            cursor.execute(sql3, id1)
            myresult = cursor.fetchone()
            # print(myresult)
            # 生成展示的data
            name = myresult[1]
            artist = myresult[2]
            album = myresult[3]
            duration_unmade = myresult[4]
            # print(duration_unmade)
            # print(type(duration_unmade))
            duration = str(duration_unmade)
            # print(duration)
            rid = myresult[0]
            data = {"name": name, "artist": artist, "album": album, "duration": duration, "rid": rid}
            # return jsonify(message="修改成功")
            return jsonify(code=200, message="success", data=data)
    except Exception as e:
        print(e)
        # return jsonify(message="请检查是否正确操作")
        return jsonify(code=404, message="该活动不存在")


# 删除历史记录
@history.route('/user/history', methods=['DELETE'])
def history_delete():
    try:
        judge = authorized_user(request.headers.get("Authorization"))
        print(judge)
        if judge:
            delete_json = request.get_json()  # 获取json数据
            print(delete_json)
            get_id = delete_json.get("id")
            get_type = delete_json.get("type")
            get_list = delete_json.get("list")
            id1 = int(get_id)
            type1 = int(get_type)
            cursor = db.cursor()
            # 根据type值判断删除的类型
            if type1 == 0:
                sql = "DELETE FROM HISTORY1271 WHERE id = %s"
                cursor.execute(sql, id1)
                # myresult = cursor.fetchone()
                db.commit()
                # print(myresult)
                return jsonify(code=200, message="success")
            elif type1 == 1:
                sql = "DELETE FROM HISTORY1271 WHERE id = %s"
                for i in get_list:
                    cursor.execute(sql, i)
                    # print(myresult)
                    db.commit()
                    # 读取现在的id列的信息
                    # data =
                return jsonify(code=200, message="success")
    except Exception as e:
        print(e)
        # return jsonify(message="请检查是否正确操作")
        return jsonify(code=404, message="该活动不存在")


# 获取历史记录
@history.route('/user/history', methods=['GET'])  # 我有点疑惑这里的方法
def search_for_history():
    # 接受前端的信息
    try:
        judge = authorized_user(request.headers.get("Authorization"))
        print(judge)
        if judge:
            page = request.args["page"]
            cursor = db.cursor()
            # lastid = cursor.lastrowid
            # 寻找最大的id，用它来计算总页数
            sql4 = 'SELECT MAX(id) AS maximum FROM HISTORY1271'
            cursor.execute(sql4)
            a = cursor.fetchall()
            print(page)
            print(a)
            for t in a:
                maximum = int(t[0])
            # 计算总页数
            total_page = maximum / 30
            total_list = []
            int_page = int(page) - 1

            # 生成返回的data
            for i in range(1 + 10 * int(int_page), 11 + 10 * int(int_page)):
                sql_update_done = "SELECT * FROM HISTORY1271 where id = %s"
                cursor.execute(sql_update_done, i)
                result1 = cursor.fetchone()
                print(result1)
                id = str(result1[0])
                name = result1[1]
                artist = result1[2]
                album = result1[3]
                duration_unmade = result1[4]
                # print(duration_unmade)
                # print(type(duration_unmade))
                duration = str(duration_unmade)
                fav = result1[5]
                rid = result1[6]
                # list1 = [id, name, artist, album, duration, fav, rid]
                data_i = {"name": name, "artist": artist, "album": album, "duration": duration, "fav": fav, "rid": rid,
                          "id": id}
                total_list.append(data_i)
            total_data = {"list": total_list}
            # print(key_words_str)
            # music_list = search_music(key_words_str)
            # print(music_list)
            # music_dict = {'list': music_list}
            # print(music_dict)

            return jsonify(code=200, message="success", data=total_data, count=total_page)  # 返回的数据的顺序有问题，我还没改
            # return jsonify(code=200, message="success", data=total_data)
    except Exception as e:
        print(e)
        return jsonify(code=404, message="该活动不存在")
