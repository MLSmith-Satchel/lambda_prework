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
    # TODO implement
    try:
        print(event)
        column = ""
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        print(event['body'])

        if event['body'].get("username") != None:
            column += " username = '"+ event['body']["username"] +"', "

        if event['body'].get("password") != None:
            column += " password = '"+ event['body']["password"] +"', "

        if event['body'].get("email_address") != None:
            column += " email_address = '"+ event['body']["email_address"] +"', "

        if event['body'].get("email_opt_in") != None:
            column += " email_opt_in = '"+ event['body']["email_opt_in"] +"', "

        if column:
            column = column[:-2]

            updateStatement = "UPDATE user set "+ column +" where id=" + event["id"]

            # Execute the SQL UPDATE statement
            cursor.execute(updateStatement)
            conn.commit()

        # records = cursor.fetchall()
        return {
            'statusCode': 200,
            'body': "Ok"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
