from typing import Optional
from fastapi.responses import JSONResponse
import json

async def get_attractions(page:int=0, keyword: Optional[str] = None):

   # 使用在 app.py 中建立的資料庫連接池
    from app import pool

    # 從連接池中獲取連接和游標
    connection=pool.get_connection()
    cursor=connection.cursor(dictionary=True)

    try:
        limit=12
        offset=page * limit

        query="""
            SELECT a.id, a.name, a.description, a.address, a.transport, 
                a.longitude, a.latitude, m.mrt, c.cat, 
                GROUP_CONCAT(i.image_url SEPARATOR ',') AS images
                FROM attractions a
                LEFT JOIN attractionsmrt m ON a.attractionsmrt_id=m.id
                LEFT JOIN attractionscat c ON a.attractionscat_id=c.id
                LEFT JOIN attractionsimages i ON a.id=i.attractions_id          
        """ 
        if keyword:
            query+=" WHERE a.name LIKE %s OR m.mrt=%s"
      
        query+=" GROUP BY a.id LIMIT %s, %s"


        count_query="""
            SELECT COUNT(*) FROM (
                SELECT a.id
                FROM attractions a
                LEFT JOIN attractionsmrt m ON a.attractionsmrt_id=m.id
        """
        if keyword:
            count_query+=" WHERE a.name LIKE %s OR m.mrt=%s"

        count_query+=") AS count_alias"


        cursor.execute (query, ('%' + keyword + '%', keyword, offset, limit) if keyword else (offset, limit))
        results=cursor.fetchall()
        

        if not results and page==0:
            return JSONResponse(content={"error":True, "message":"查無資料"}) 
        
        cursor.execute(count_query, ('%' + keyword + '%', keyword) if keyword else ())
        row=cursor.fetchone() #字典
        result_count=row['COUNT(*)'] #從字典中取出值

        total_pages=(result_count//limit)+1
            
        if total_pages > 1:
            nextPage= page+1 if page+1 < total_pages else None

        else:
            nextPage=None

        for attraction in results:
            attraction['images']=attraction['images'].split(',')

        json_data = {
            "nextPage": nextPage,
            "data": results
        }

        return JSONResponse(content=json_data)
           
    finally:
        cursor.close()
        connection.close()


async def get_attraction_by_id(attractionId:int):
    from app import pool
    connection = pool.get_connection()
    cursor = connection.cursor(dictionary=True)
        
    try:
        query="""
            SELECT a.id, a.name, a.description, a.address, a.transport, 
                a.longitude, a.latitude, m.mrt, c.cat, 
                GROUP_CONCAT(i.image_url SEPARATOR ',') AS images
                FROM attractions a
                LEFT JOIN attractionsmrt m ON a.attractionsmrt_id = m.id
                LEFT JOIN attractionscat c ON a.attractionscat_id = c.id
                LEFT JOIN attractionsimages i ON a.id = i.attractions_id
                WHERE a.id=%s
                GROUP BY a.id          
        """ 
        cursor.execute(query, (attractionId,))
        attraction = cursor.fetchone()  
        attraction['images']=attraction['images'].split(',')
  
        if not attraction:
            return JSONResponse(status_code=400, content={"error": True, "message": "景點編號不正確"})
        else:
            return JSONResponse(content={"data":attraction})   
   
    finally:
        cursor.close()
        connection.close()


async def get_mrt_list():
    from app import pool
    connection = pool.get_connection()
    cursor = connection.cursor(dictionary=True)
        
    try:
        query="""SELECT m.mrt FROM attractionsmrt m
                LEFT JOIN attractions a ON a.attractionsmrt_id = m.id
                GROUP BY m.mrt
                ORDER BY COUNT(a.id) DESC
            """
        cursor.execute(query)
        mrts = cursor.fetchall()  
        
        mrts_list=[mrt['mrt'] for mrt in mrts]
        return JSONResponse(content={"data":mrts_list})   

    finally:
        cursor.close()
        connection.close()
    
