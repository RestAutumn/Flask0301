from flask import Flask

from user import user
from search import search
from history import history

app = Flask(__name__)

app.register_blueprint(user)
app.register_blueprint(search)
app.register_blueprint(history)

if __name__ == '__main__':
    print(app.url_map)
    app.run(host='127.0.0.1', port=8000)
