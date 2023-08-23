from helpers.mysql_connection import MySQLConnection
import uuid

mysql_conn = MySQLConnection()
mysql_conn.select_database("callingApp")

connection = mysql_conn.get_connection()


def insertCallingTransaction(user_uid, lead_call_number, lead_status, record_uid, connect_status, remarks, contact_person):
    try:
        call_record_uid = str(uuid.uuid4())

        cursor = connection.cursor()
        query = "INSERT INTO calling_transaction (user_uid, lead_call_number, lead_status, record_uid, connect_status, remarks, contact_person, call_record_uid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (user_uid, lead_call_number, lead_status, record_uid, connect_status, remarks, contact_person, call_record_uid))
        cursor.close()
        connection.commit()

        return {"status": "success", "data": {"message": "update successful", "call_record_uid": call_record_uid}}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "failure", "data": str(e)}

if __name__ == '__main__':
    lead_status = insertCallingTransaction('shivam@gmail.com', '706172681', 0, 'yeah', 0, 'testing', '7061726881')
    print(lead_status)


