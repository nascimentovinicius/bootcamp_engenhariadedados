from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql+psycopg2://root:root@localhost/test_db')

sql = '''
select * from vw_song;
'''

df = pd.read_sql_query(sql, engine)
print(df)

df_acdc = pd.read_sql_query("select * from vw_song where artist like 'AC/DC'", engine)
print(df_acdc)


sql = "insert into tbl_qualquer values (1,2,3,'aaaaa')"
engine.execute(sql)
