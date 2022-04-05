import pymysql

# 접속 객체 반환 함수
def getConnection():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='password',
        db='final',
        charset='utf8'
    )
    return conn
