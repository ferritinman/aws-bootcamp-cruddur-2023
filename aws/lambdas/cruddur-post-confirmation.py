import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('========')
    print('User attributes')
    print(user)

    user_display_name = user['name']
    user_email = user['email']
    user_handle = user['preferred_username']
    user_cognito_id = user['sub']

    print(os.getcwd())

    try:
        conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
        cur = conn.cursor()
        
        params = {
            'display_name': user_display_name,
            'user_email': user_email,
            'handle': user_handle,
            'user_cognito_id': user_cognito_id
        }

        sql = f"""
            INSERT INTO users (
                display_name, 
                email,
                handle, 
                cognito_user_id
            ) VALUES (
                %(display_name)s,
                %(user_email)s,
                %(handle)s,
                %(user_cognito_id)s
            )
        """
        print(sql)
        cur.execute(sql, params)
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print('error:')
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event
    