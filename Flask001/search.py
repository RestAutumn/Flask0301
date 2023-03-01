# 导入模块

import jwt
import pymysql as pymysql
from flask import request,jsonify,Blueprint
from time import strftime, gmtime
import requests
import os
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

    sql2 = '''
        CREATE TABLE IF NOT EXISTS HISTORY1271(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name1 VARCHAR(1000),
        artist1 VARCHAR(1000),
        album1 VARCHAR(1000),
        duration1 TIME,
        fav1 INT,
        rid1 INT)'''

    cur.execute(sql2)
    print('表格创建成功')
    cur.close()
except pymysql.Error as e:
    print('表格创建失败：' + str(e))

# 初始化
search = Blueprint('search',__name__)
CORS(search)
SECRET_KEY = '123456'
search.secret_key = "1271"
ALGORITHM = "HS256"



# 链接数据库
db = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME, charset=DBTYPE)

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


# 搜索酷我音乐
def search_music(kw):
    # 接受来自前端的关键词信息
    # 歌曲列表信息链接
    url = f'https://kuwo.cn/api/www/search/searchMusicBykeyWord?key={kw}&pn=1&rn=30&httpsStatus=1&reqId=a1622200-b009-11ec-94e3-c9fc163ba367'
    # 请求头
    headers = {
        'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1648629490; _ga=GA1.2.409316159.1648629490; _gid=GA1.2.1021303329.1648629490; _gat=1; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1648630329; kw_token=2EBX1R5WO8Z',
        'csrf': '2EBX1R5WO8Z',
        'Referer': 'https://kuwo.cn/'
    }

    # 访问链接，并返回json数据
    response = requests.get(url=url, headers=headers).json()
    # print(response)
    # 歌曲列表信息

    # 注意 你还没有针对翻页功能做出调整

    music_list = response['data']['list']
    # print(music_list)
    new_music_list = []
    # 遍历歌曲列表信息 本质上是在那一大坨json串里提取有用的信息
    for i in range(len(music_list)):
        # 歌曲
        name = music_list[i]['name']
        # 歌手
        artist = music_list[i]['artist']
        # 专辑
        album = music_list[i]['album']
        # 时长
        duration_second = music_list[i]['duration']
        duration = strftime("%H:%M:%S", gmtime(float(duration_second)))
        # rid(mid)
        rid = music_list[i]['rid']
        # 拼凑list
        total_dict = {"name": name, "artist": artist, "album": album, "duration": duration, "rid": rid}
        # print(total_dict)
        new_music_list.append(total_dict)

    insert_dbhistory(new_music_list)

    return new_music_list
    # 打印列表信息
    # print(f'{i + 1} {name} - {artist}-{album}-{duration}- id={rid}')


# 下载音乐的函数
def download_kuwo_music(rid, name, artist):
    try:
        # 创建文件夹
        kw_file = os.path.exists('kuwo')  # 判断文件夹是否存在
        if kw_file is True:
            pass
        else:
            kw_file = os.getcwd()
            os.mkdir(kw_file + '/kuwo')
        id = rid
        link = f'https://link.hhtjim.com/kw/{id}'
        # 访问直链
        response_down = requests.get(url=link).content

        # 下载歌曲
        # with open(f"酷我/{song} - {singer}.mp3", 'wb') as kw:
        with open(f"kuwo/{name} - {artist}.mp3", 'wb') as kw:
            kw.write(response_down)
            print('下载成功！')
    except Exception as e:
        print(e)


# 搜索功能
# 这玩意儿每用一次，服务器就得重启一下才能用第二次
# 我始终没找到是什么问题，难办┭┮﹏┭┮
@search.route('/search', methods=['GET'])  # 我有点疑惑这里的方法
def search_for_music():

    # 接受前端的信息
    try:
        judge = authorized_user(request.headers.get("Authorization"))
        print(judge)
        if judge:
            key_words_str = request.args["text"]
            print(key_words_str)
            music_list = search_music(key_words_str)
            print(music_list)
            music_dict = {'list': music_list}
            print(music_dict)
            return jsonify(code=200, message="success", data=music_dict)  # 返回的数据的顺序有问题，我还没改

    except Exception as e:
        print(e)
        return jsonify(code=404, message="该活动不存在")


# 下载功能
# 接口端的冒号是多打了吗
@search.route('/search/download/<rid>', methods=['GET'])
def dl_music(rid):
    # 接受前端的信息

    try:
        judge = authorized_user(request.headers.get("Authorization"))
        print(judge)
        if judge:
            # key_words_str = request.args[":"]
            # print(key_words_str)
            # rid = str(176051)
            # print(rid)

            # 去数据库里查找rid
            cursor = db.cursor()
            sql_update_done = "SELECT * FROM HISTORY1271 where rid1 = %s"
            cursor.execute(sql_update_done, rid)
            result1 = cursor.fetchone()
            # print(result1)
            # 生成展示的信息
            id = str(result1[0])
            name = result1[1]
            artist = result1[2]
            album = result1[3]
            duration_unmade = result1[4]
            # print(duration_unmade)
            # print(type(duration_unmade))
            duration = str(duration_unmade)
            # list1 = [id,name,artist,album,duration,rid]

            # 下载歌曲
            download_kuwo_music(rid, name, artist)
            # 写入下载记录
            insert_dbdownload(name, artist, album, duration, rid)
            return jsonify(code=200, message="success")  # 返回的数据的顺序有问题，我还没改
    except Exception as e:
        print(e)
        return jsonify(code=404, message="该活动不存在")


