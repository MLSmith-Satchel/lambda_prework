import mysql.connector
import rds_config
from mysql.connector import Error
from pypika import MySQLQuery as Query, Table, Field
import re
import datetime

def create_user(connection, username, password, email_address, email_opt_in):
    isValid = check(email_address)
    if(isValid):
        mycursor = connection.cursor()
        user = Table('user')
        q = Query.into(user).columns('username', 'password', 'email_address', 'email_opt_in').insert(username, password,email_address,email_opt_in)
        #print(q.get_sql())
        mycursor.execute(str(q))

        connection.commit()
        return mycursor.rowcount + " record inserted."

def my_handler(event, context):
    message = 'Hello {} {}!'.format(event['first_name'], event['last_name'])
    return {
          'message' : message
      }
