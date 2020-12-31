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
leagues = []

def lambda_handler(event, context):
    leagues = find_league_id(event["owner_id"])
    #print(leagues)
    where_string = "("
    for league in leagues:
        #print(league["league_id"])
        where_string += str(league["league_id"]) + ","
    where_string = where_string[:-1]
    where_string += ")"
    #print(where_string)

    try:
        print("Got Here")
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select league_name from league where league_id in " + where_string)
        records = cursor.fetchall()
        print(records)

        return {
            'statusCode': 200,
            'body': records
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def find_league_id(owner_id):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select l.league_id from leagues l, team t where l.team_id = t.team_id and t.owner_id = " + owner_id)
    leagues = cursor.fetchall()
    return leagues

def main():
    event = {'owner_id': '9'}

    context = None
    lambda_handler(event,context)

if __name__ == "__main__":
    main()
