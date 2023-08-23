import redis
from helpers.mysql_connection import MySQLConnection

mysql_conn = MySQLConnection()
mysql_conn.select_database("salevant")

connection = mysql_conn.get_connection()

def get_lead_data_func(user_uid):
    redis_host = '65.0.21.175'
    redis_port = 6379
    redis_password = 'yogleadsRedis@2023'  # If you set up a password

    # Create a Redis client
    client = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

    try:
        #get record_uid from user_id after doing rpop from redis.
        cursor = connection.cursor()
        prefix = "app_user"
        hash_key = f"{prefix}_{user_uid}"
        record_uid = client.rpop(user_uid)
        if record_uid is not None:
            client.hdel(hash_key, record_uid)

        print("record_uid:",record_uid)
        if record_uid is not None:
            record_uid = record_uid.decode('utf-8')
            print("Popped data:", record_uid)

            query="SELECT * FROM get_b2b WHERE record_uid = %s"
            
            cursor.execute(query, (record_uid,))
            row = cursor.fetchone()

            if row:
                if cursor.description is not None:
                    columns = [desc[0] for desc in cursor.description]
                    data_dict = {columns[i]: row[i] for i in range(len(columns))}
                    cursor.close()  # Close the cursor here, after fetching the data
                    return {'status': 'success', 'data': data_dict}
                else:
                    cursor.close()
                    return {'status': 'failure', 'data': "Cursor description is None"}

                
            else:
                cursor.close()  # Close the cursor even if no data is found
                return {'status': 'success', 'data': "No Data Found"}
        else:
            return {'status': 'success', 'data': 'Redis Queue is Empty'}

    except Exception as e:
        print(f"An error occurred in get_lead_data_func: {str(e)}")
        return {'status': 'failure', 'data': str(e)}

if __name__ == '__main__':
    result=get_lead_data_func('fde83688-e9cd-44bd-bda8-ed7462fc2038')
    print(result)
