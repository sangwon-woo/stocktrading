import mysql.connector as mc
import DBconfig as dbconf
import time

with mc.connect(**dbconf.dbConfig) as conn:
    cursor = conn.cursor()
    sql_mc = """
        SELECT STK_CD, COUNT(*) AS 로우수
        FROM DB_SQLSTK.HISTORY_DT
        GROUP BY STK_CD;
    """

    total_time = 0
    for i in range(10):
        mc_st = time.time()
        cursor.execute(sql_mc)
        data = cursor.fetchall()
        mc_ft = time.time()

        total_time += mc_ft - mc_st

    print("mysql.connector took {:3f} seconds.".format(float(total_time / 10)))
