import json
from mysql.connector import pooling
import re

db = {
    "host":"localhost",
    "user":"root",
    "password":"123qwe",
    "database":"taipeitour_website"
}
pool = pooling.MySQLConnectionPool(pool_name="pool", pool_size=5, **db)
connection=pool.get_connection()
cursor=connection.cursor()

#create TABLE attractionscat
cursor.execute("""CREATE TABLE attractionscat (
               id INT AUTO_INCREMENT PRIMARY KEY,
               cat VARCHAR(255) UNIQUE
);""")

#create TABLE attractionsmrt
cursor.execute("""CREATE TABLE attractionsmrt (
               id INT AUTO_INCREMENT PRIMARY KEY,
               mrt VARCHAR(255) UNIQUE);
               """)

#create TABLE attractions
cursor.execute("""CREATE TABLE attractions (
                id INT AUTO_INCREMENT PRIMARY KEY ,
                serial_no BIGINT NOT NULL,
                name VARCHAR(255) NOT NULL,
                address VARCHAR(255) NOT NULL,
                attractionscat_id INT ,
                attractionsmrt_id INT,
                MEMO_TIME varchar(500),
                transport VARCHAR(2000),
                description VARCHAR(2000),
                rate INT,
                longitude float NOT NULL,
                latitude float NOT NULL,            
                FOREIGN KEY (attractionscat_id) REFERENCES attractionscat(id),
                FOREIGN KEY (attractionsmrt_id) REFERENCES attractionsmrt(id));
               """)

#create TABLE attractionsImages 
cursor.execute("""CREATE TABLE attractionsImages(
              id INT AUTO_INCREMENT PRIMARY KEY, 
              attractions_id INT,
              image_url TEXT NOT NULL,
              FOREIGN KEY(attractions_id) REFERENCES attractions(id));
              """)


# 讀取JSON檔
def load_data():
    with open('taipei-attractions.json', 'r', encoding='utf-8') as file:
        data=json.load(file)
    return data["result"]["results"]

def insert_data():
    data=load_data()
    for item in data:    
        serial_no = item.get("SERIAL_NO")
        name = item.get("name")
        address = item.get("address")
        cat = item.get("CAT")
        mrt = item.get("MRT",'')
        memo_time = item.get("MEMO_TIME",'')
        transport=item.get("direction")
        description = item.get("description")
        rate = item.get("rate")
        longitude = item.get("longitude")
        latitude = item.get("latitude")
        image_urls=item.get("file")
              

        print("Inserting data for:", name) 

        # insert attractionscat 資料表
        if cat:
            cursor.execute("""INSERT IGNORE INTO attractionscat (cat) VALUES (%s)""", (cat,))
            cursor.execute("SELECT id FROM attractionscat WHERE cat = %s", (cat,))
            cat_row=cursor.fetchone()       
            attractionscat_id=cat_row[0] 
        else:
            attractionscat_id=None

        # insert attractionsmrt 資料表
        if mrt:
            cursor.execute("""INSERT IGNORE INTO attractionsmrt (mrt) VALUES (%s)""", (mrt,))
            cursor.execute("SELECT id FROM attractionsmrt WHERE mrt = %s", (mrt,))
            mrt_row=cursor.fetchone()
            attractionsmrt_id=mrt_row[0] if mrt_row else None
        else:
            attractionsmrt_id=None


        # 檢查資料庫中是否已存在相同 serial_no 的資料
        cursor.execute("SELECT COUNT(*) FROM attractions WHERE serial_no = %s", (serial_no,))
        result=cursor.fetchone()
        if result[0] > 0:
            print(f"serial_no {serial_no} 已經存在資料表中")
        
        else:
            # insert attractions 資料表    
            cursor.execute("""
            INSERT INTO attractions (serial_no, name, address, attractionscat_id, attractionsmrt_id, MEMO_TIME, transport, description, rate, longitude, latitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (serial_no, name, address,  attractionscat_id, attractionsmrt_id, memo_time, transport, description, rate, longitude, latitude,))
    
   
        # 取得插入資料的ID
        attractions_id = cursor.lastrowid

        #分割urls
        def extract_urls_from_images(image_urls):
            urls_list =re.findall(r'https?://[^\s]+?\.(?:JPG|jpg|PNG|png)', image_urls)
            return urls_list

        #insert attractionsImages 資料表
        urls = extract_urls_from_images(image_urls)
                
        for url in urls:
            cursor.execute("""INSERT INTO attractionsImages (attractions_id, image_url) VALUES (%s, %s)""", (attractions_id, url))
 
    connection.commit()
    cursor.close()
    connection.close()

insert_data()
