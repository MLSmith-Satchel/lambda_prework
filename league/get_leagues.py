import sys
import json
import pymysql
import rds_config
import logging

rds_host = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
#port = rds_config.port

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

records = []
def lambda_handler(event, context):
    try:

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select * from league")
        records = cursor.fetchall()
        return {
            'statusCode': 200,
            'body': records
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
