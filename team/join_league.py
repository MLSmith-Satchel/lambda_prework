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

    sql = "INSERT INTO `leagues` (`league_id`, `team_id`) VALUES(%s, %s)"
    val = (event["league_id"], event["team_id"])

    with conn.cursor() as cur:
        cur.execute(sql, val)
        conn.commit()
        #user_id = cur.lastrowid


    return {
        'statusCode': 200,
        'body': json.dumps('Data has been inserted successfully')
    }
def main():
    event = {'league_id': '2', 'team_id':'2'}

    context = None
    lambda_handler(event,context)

if __name__ == "__main__":
    main()
