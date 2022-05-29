from fastapi import FastAPI ,Request ,UploadFile,File
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from AttendanceProject import camera_output
import csv
import webbrowser
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
import os
csvfilepath="Attendance.csv"

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")




@app.get("/")
async def home(request: Request):
  return templates.TemplateResponse("home.html",{"request":request})

@app.get('/video_feed')
async def video_feed():
     return StreamingResponse(camera_output(),media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/attendance")
def attendance(request:Request):
       data=[]
       totalcount=0
       with open("totalcount.doc","r") as countfile:
             filedata=countfile.read()
             totalcount=int(filedata)

       with open("Attendance.csv","r") as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    
                    data.append(row)
                
                if os.stat(csvfilepath).st_size == 0:
                     pass
                else:
                     if(len(data[0])==0):
                        data.pop(0)
              
                
                return templates.TemplateResponse('attendance.html', {"request":request,"data":data,"noofstudentspresent":len(data),"totalcount":totalcount})    


@app.get("/clear")
def clear():
    with open("Attendance.csv","w") as file:
        file.truncate()
        file.close()
        msg={"message":"cleared"}
        json_data=jsonable_encoder(msg)
        return JSONResponse(content=json_data)



    
@app.post("/uploadfile/")
async def import_file_post(imagefile: UploadFile = File(...)):
    file_location = f"./ImagesAttendance/{imagefile.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(imagefile.file.read())
        
    msg={"status":True}
    json_data=jsonable_encoder(msg)
    return JSONResponse(content=json_data)
    



if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:8000"]
    webbrowser.open("http://localhost:8000/")
    asyncio.run(serve(app, Config()))