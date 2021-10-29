import pymysql
from sqlalchemy import create_engine, MetaData, Table
import time
from DBconfig import base_addr

pymysql.install_as_MySQLdb()



engine = create_engine(base_addr + "/db_sqlstk", encoding='utf-8')

with engine.connect() as conn:
    sql_sa = """
        SELECT STK_CD, COUNT(*) AS 로우수
        FROM DB_SQLSTK.HISTORY_DT
        GROUP BY STK_CD;
    """

    total_time = 0
    for i in range(10):
        sa_st = time.time()
        data = conn.execute(sql_sa).fetchall()
        sa_ft = time.time()
        total_time += sa_ft - sa_st
    print('sqlalchemy.create_engine took {:3f} seconds.'.format(float(total_time / 10)))