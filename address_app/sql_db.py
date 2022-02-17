import sqlite3
import logger
from logger import *

def connect_to_db():
    log().info("Connect to DB")
    conn = sqlite3.connect('database.db')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        conn.execute('''
            CREATE TABLE address_book (
                ad_id INTEGER PRIMARY KEY NOT NULL,
                address_detail TEXT NOT NULL,
                latitude TEXT NOT NULL,
                longitude TEXT NOT NULL
            );
        ''')

        conn.commit()
        log().info("Table created successfully")
        
    except Exception as e:
        conn.commit()
        log().info("Table already exists")
    finally:
        conn.close()

def insert_address(data):
    create_db_table()
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO address_book (ad_id, address_detail, latitude, longitude) VALUES (?, ?, ?, ?)", 
                    (data['ad_id'], data['address_detail'], data['latitude'], data['longitude']) )
        conn.commit()
    except:
        conn().rollback()
        log().error("Failed to create Address")
        return {"message":"Failed to create Address"}

    finally:
        conn.close()
    log().info("Address Created Successfully")
    return {'message':"Address added successfully","longitude":data['longitude'], "latitude":data['latitude'], "updated_address":data['address_detail']} 

def get_address():
    address = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM address_book")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            address.append({'ad_id':i['ad_id'], 'address_detail':i['address_detail'], 'latitude':i['latitude'], 'longitude':i['longitude']})
    except:
        log().info("Failed to fetch address")
        address = []

    return address  

def get_address_by_id(ad_id):
    address = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM address_book WHERE ad_id = ?", 
                       (ad_id,))
        i = cur.fetchone()

        # convert row object to dictionary
        address = {'ad_id':i['ad_id'], 'address_detail':i['address_detail'], 'latitude':i['latitude'], 'longitude':i['longitude']}
    except:
        log().error("Failed to get address")
        address = {}

    return address

def update_address(data,ad_id):
    updated_address = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE address_book SET address_detail = ?, latitude = ?, longitude = ? WHERE ad_id =?",  
                     (data['address_detail'], data['latitude'], data['longitude'],
                     ad_id,))
        conn.commit()
        log().error("address Updated successfully")
        #return the user
        updated_address = get_address_by_id(ad_id)

    except:
        log().info("Failed to Update address")
        conn.rollback()
        updated_address = {}
    finally:
        conn.close()

    return updated_address

def delete_user(ad_id):
    try:
        conn = connect_to_db()
        out = conn.execute("DELETE from address_book WHERE ad_id = ?",     
                      (ad_id,))
        conn.commit()
        log().info("Address deleted successfully")
    except Exception as e:
        conn.rollback()
        log().error("Cannot delete Address")
        return ({"message":"Cannot delete Address"})
    finally:
        conn.close()

    return ({"message":"Address deleted successfully"})   
