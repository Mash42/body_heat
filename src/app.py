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
    return render_template("index.html"
                          ,measure_list=get_measure_list()
                          ,status_message=None
                          )

# 測定結果登録
@app.route('/create_data', methods=["GET", "POST"])
def search():
    measure_date = None
    body_heat = None
    status_message = None
    
    if request.method == 'POST':
        # 測定日 YYYY-MM-DD形式
        measure_date = request.form['measure_date']
        measure_date = measure_date.replace("-", "") # YYYYMMDD形式へ編集
        # 体温 文字列
        body_heat = request.form['body_heat']

        # 既に測定されている場合
        if is_exist_measure_data(measure_date):
            status_message = "入力された測定日には既に測定結果が登録されています。"
        else:
            create_measure_data(measure_date
                               ,body_heat
                               )
            status_message = "登録が完了しました。"

    return render_template("index.html"
                          ,measure_list=get_measure_list()
                          ,status_message=status_message
                          )

# 測定結果データ一覧を取得する。
def get_measure_list():
    conn = getConnection()
    try:
        with conn.cursor() as cursor:
            sql = """
                  SELECT MEASURE_DATE
                        ,BODY_HEAT
                    FROM TBL_MEASURE
                   ORDER BY MEASURE_DATE
                  ;
                  """
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        conn.close()
    result_list = list()
    for row in result:
        result_list.append({"MEASURE_DATE":row["MEASURE_DATE"]
                           ,"BODY_HEAT":row["BODY_HEAT"]
                           }
                          )
    return result_list

def create_measure_data(measure_date, body_heat):
    conn = getConnection()
    # # Insert処理
    try:
        with conn.cursor() as cursor:
            sql = """
                  INSERT INTO TBL_MEASURE (MEASURE_DATE, BODY_HEAT) 
                  VALUES (%s, %s)
                  """
            r = cursor.execute(sql, (measure_date, body_heat))
            conn.commit()
    finally:
        conn.close()

# 測定データが既に登録されているかをチェックする
def is_exist_measure_data(measure_date):
    conn = getConnection()
    result = None
    try:
        with conn.cursor() as cursor:
            sql = """
                  SELECT COUNT(0) AS COUNT_RESULT
                    FROM TBL_MEASURE
                   WHERE MEASURE_DATE = %s
                  ;
                  """
            cursor.execute(sql, (measure_date))
            result = cursor.fetchall()
    finally:
        conn.close()
    count_result = result[0]["COUNT_RESULT"]
    return count_result > 0
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
