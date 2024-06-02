import json
from mysql.connector import pooling
import re

db = {
    "host":"localhost",
    "user":"root",
    "password":"123qwe",
    "database":"taipeitourd_website"
}
pool = pooling.MySQLConnectionPool(pool_name="pool", pool_size=5, **db)
connection=pool.get_connection()
cursor=connection.cursor()

#create TABLE attractionsCAT
cursor.execute("""CREATE TABLE attractionsCAT (
               id INT AUTO_INCREMENT PRIMARY KEY,
               CAT VARCHAR(255) UNIQUE
);""")

#create TABLE attractionsMRT
cursor.execute("""CREATE TABLE attractionsMRT (
               id INT AUTO_INCREMENT PRIMARY KEY,
               MRT VARCHAR(255) UNIQUE);
               """)

#create TABLE attractions
cursor.execute("""CREATE TABLE attractions (
                id INT AUTO_INCREMENT PRIMARY KEY ,
                SERIAL_NO BIGINT NOT NULL,
                name VARCHAR(255) NOT NULL,
                address VARCHAR(255) NOT NULL,
                attractionsCAT_id INT ,
                attractionsMRT_id INT,
                MEMO_TIME varchar(500),
                transport VARCHAR(2000),
                description VARCHAR(2000),
                rate INT,
                longitude float NOT NULL,
                latitude float NOT NULL,            
                FOREIGN KEY (attractionsCAT_id) REFERENCES attractionsCAT(id),
                FOREIGN KEY (attractionsMRT_id) REFERENCES attractionsMRT(id));
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
        SERIAL_NO = item.get("SERIAL_NO")
        name = item.get("name")
        address = item.get("address")
        CAT = item.get("CAT")
        MRT = item.get("MRT",'')
        MEMO_TIME = item.get("MEMO_TIME",'')
        transport=item.get("direction")
        description = item.get("description")
        rate = item.get("rate")
        longitude = item.get("longitude")
        latitude = item.get("latitude")
        image_urls=item.get("file")
              

        print("Inserting data for:", name) 

        # insert attractionsCAT 資料表
        if CAT:
            cursor.execute("""INSERT IGNORE INTO attractionsCAT (CAT) VALUES (%s)""", (CAT,))
            cursor.execute("SELECT id FROM attractionsCAT WHERE CAT = %s", (CAT,))
            cat_row=cursor.fetchone()       
            attractionsCAT_id=cat_row[0] 
        else:
            attractionsCAT_id=None

        # insert attractionsMRT 資料表
        if MRT:
            cursor.execute("""INSERT IGNORE INTO attractionsMRT (MRT) VALUES (%s)""", (MRT,))
            cursor.execute("SELECT id FROM attractionsMRT WHERE MRT = %s", (MRT,))
            mrt_row=cursor.fetchone()
            attractionsMRT_id=mrt_row[0] if mrt_row else None
        else:
            attractionsMRT_id=None


        # 檢查資料庫中是否已存在相同 SERIAL_NO 的資料
        cursor.execute("SELECT COUNT(*) FROM attractions WHERE SERIAL_NO = %s", (SERIAL_NO,))
        result=cursor.fetchone()
        if result[0] > 0:
            print(f"SERIAL_NO {SERIAL_NO} 已經存在資料表中")
        
        else:
            # insert attractions 資料表    
            cursor.execute("""
            INSERT INTO attractions (SERIAL_NO, name, address, attractionsCAT_id, attractionsMRT_id, MEMO_TIME, transport, description, rate, longitude, latitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (SERIAL_NO, name, address,  attractionsCAT_id, attractionsMRT_id, MEMO_TIME, transport, description, rate, longitude, latitude,))
    
   
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
