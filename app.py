from fastapi import *
from fastapi.responses import FileResponse,JSONResponse
from typing import Optional
from mysql.connector import pooling
from attractions_handler import get_attraction_by_id, get_attractions, get_mrt_list

app=FastAPI()

db = {
    "host":"localhost",
    "user":"root",
    "password":"123qwe",
    "database":"taipeitour_website",
	"ssl_disabled": True
}
pool = pooling.MySQLConnectionPool(pool_name="pool", pool_size=5, **db)
connection=pool.get_connection()
cursor=connection.cursor()

# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")

@app.get("/api/attractions")
async def API_get_attractions(request: Request, page:int=0, keyword: Optional[str] = None):
	
	try:
		data = await get_attractions(page, keyword)
		return data
	
		
	except Exception as e:
		print("An error occurred while fetching data:", e)
	return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤，請稍後再試。"})

@app.get("/api/attraction/{attractionId}")
async def API_get_attracion_by_id(attractionId:int):
	
	try:
		data=await get_attraction_by_id(attractionId)
		return data
    
	except Exception as e:
		print("An error occurred while fetching data:", e)
	return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤，請稍後再試。"})


@app.get("/api/mrts")
async def API_get_mrt_list():
    
	try:
		mrtlist=await get_mrt_list()
		return mrtlist
      
	except Exception as e:
		print("An error occurred while fetching data:", e)
	return JSONResponse(status_code=500, content={"error": True, "message": "伺服器內部錯誤，請稍後再試。"})



