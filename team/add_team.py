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

    sql = "INSERT INTO `team` (`owner_id`, `team_name`, `image_url`,`draft_order`) VALUES(%s, %s, %s, %s)"
    val = (event["owner_id"], event["team_name"], event["image_url"], event["draft_order"])

    with conn.cursor() as cur:
        cur.execute(sql, val)
        conn.commit()
        user_id = cur.lastrowid


    return {
        'statusCode': 200,
        'body': json.dumps('Data has been inserted successfully')
    }
def main():
    event = {'owner_id': '9', 'team_name':'Test Team Name', 'image_url': 's3://fakeurl.com', 'draft_order': '12'}

    context = None
    lambda_handler(event,context)

if __name__ == "__main__":
    main()
