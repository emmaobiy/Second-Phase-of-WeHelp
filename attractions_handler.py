from typing import Optional
from fastapi.responses import JSONResponse

async def get_attractions(page:int=0, keyword: Optional[str] = None):

   # 使用在 app.py 中建立的資料庫連接池
    from app import pool

    # 從連接池中獲取連接和游標
    connection = pool.get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query="""
            SELECT a.id, a.name, a.description, a.address, a.transport, 
                a.longitude, a.latitude, m.mrt, c.CAT, 
                JSON_ARRAYAGG(i.image_url) AS images
                FROM attractions a
                LEFT JOIN attractionsMRT m ON a.attractionsMRT_id = m.id
                LEFT JOIN attractionsCAT c ON a.attractionsCAT_id = c.id
                LEFT JOIN attractionsImages i ON a.id = i.attractions_id          
        """ 
        # 搜尋條件
        if keyword:
            query+= "WHERE a.name LIKE %s OR m.mrt=%s GROUP BY a.id"
            cursor.execute(query,  ('%' + keyword + '%', '%' + keyword + '%'))

        else:
            query+= "GROUP BY a.id"
            cursor.execute(query)
        
        # 取得所有符合條件的景點資料
        attractions = cursor.fetchall()
        print(len(attractions))


        # 處理資料是否分頁
        limit=12
        offset = page * limit

        if not attractions:
            return JSONResponse(content={"error":True, "message":"查無資料"})  
        
        else:
            paginated_attractions = attractions[offset:offset+limit]
            total_pages = (len(attractions) - 1) // limit + 1  
            next_page = page + 1 if page < total_pages * limit < len(attractions) else None

            json_data={
                 "nextpage":next_page,
                 "data":paginated_attractions
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
                a.longitude, a.latitude, m.mrt, c.CAT, 
                JSON_ARRAYAGG(i.image_url) AS images
                FROM attractions a
                LEFT JOIN attractionsMRT m ON a.attractionsMRT_id = m.id
                LEFT JOIN attractionsCAT c ON a.attractionsCAT_id = c.id
                LEFT JOIN attractionsImages i ON a.id = i.attractions_id
                WHERE a.id=%s
                GROUP BY a.id          
        """ 
        cursor.execute(query, (attractionId,))
        attraction = cursor.fetchone()  
  

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
        query="""SELECT m.mrt FROM attractionsMRT m
                LEFT JOIN attractions a ON a.attractionsMRT_id = m.id
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
    
