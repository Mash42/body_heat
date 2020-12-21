from flask import Flask, render_template, request
import pymysql
import requests
import re
from flask import Markup

app = Flask(__name__)

# データベースコネクション情報
MYSQL_OPTIONS = {"host": 'db'
                ,"port": 3306
                ,"user": 'hoge_user'
                ,"passwd": 'hoge_pass_db'
                ,"db": 'hoge_db'
                ,"charset": 'utf8'
                }

# ホーム
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html",measure_list=get_measure_list())

# 検索
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == 'POST':
        None
    
    return render_template("index.html")

# 測定結果データ一覧を取得する。
def get_measure_list():
    conn = getConnection()
    try:
        with conn.cursor() as cursor:
            sql = """
                  SELECT MEASURE_DATE
                        ,MEASURE_RESULT
                    FROM TBL_MEASURE
                  ;
                  """
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        conn.close()
    result_list = list()
    for row in result:
        result_list.append({"MEASURE_DATE":row["MEASURE_DATE"]
                           ,"MEASURE_RESULT":row["MEASURE_RESULT"]
                           }
                          )
    return result_list

# データベースコネクション獲得
def getConnection():
    conn = pymysql.connect(host=MYSQL_OPTIONS['host']
                          ,port=MYSQL_OPTIONS['port']
                          ,user=MYSQL_OPTIONS['user']
                          ,passwd=MYSQL_OPTIONS['passwd']
                          ,db=MYSQL_OPTIONS['db']
                          ,charset=MYSQL_OPTIONS['charset']
                          ,cursorclass=pymysql.cursors.DictCursor
                          )
    return conn

# アプリ起動
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
