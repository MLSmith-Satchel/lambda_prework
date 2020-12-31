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

        if event.get("username") != None:
            print("username column update")
            column += " username = '"+ event['username'] +"', "

        if event.get("password") != None:
            print("password column update")
            column += " password = '"+ event['password'] +"', "

        if event.get('email_address') != None:
            print("email_address column update")
            column += " email_address = '"+ event['email_address'] +"', "

        if event.get("email_opt_in") != None:
            print("email_opt_in column update")
            column += " email_opt_in = '"+ event['email_opt_in'] +"', "

        print("End If")

        if column != None:

            column = column[:-2]
            print(event.get("id"))
            updateStatement = "UPDATE user set "+ column +" where id=" + event.get("id")
            print("Got Here")
            print(updateStatement)

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

def main():
    event = {'id': "9", 'username':'newname123', 'email_address': 'jdoe1234@fake.com', 'email_opt_in': "0"}

    context = None
    lambda_handler(event,context)

if __name__ == "__main__":
    main()
