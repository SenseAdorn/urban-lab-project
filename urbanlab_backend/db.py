import pymysql
from flask import current_app

# Database connection
def get_db_connection():
    db_config = current_app.config['DATABASE_CONFIG']
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        cursorclass=pymysql.cursors.DictCursor
    )
