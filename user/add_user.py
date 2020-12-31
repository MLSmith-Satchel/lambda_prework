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

def lambda_handler(event, context):
    print(conn.open)

    sql = "INSERT INTO `user` (`username`, `password`,  `email_address`, `email_opt_in`) VALUES(%s, %s, %s, %s)"
    val = (event["username"], event["password"], event["email_address"], event["email_opt_in"])

    with conn.cursor() as cur:
        cur.execute(sql, val)
        conn.commit()
        user_id = cur.lastrowid


    return {
        'statusCode': 200,
        'body': json.dumps('Data has been inserted successfully')
    }
