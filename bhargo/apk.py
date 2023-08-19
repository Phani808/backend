# API for APK Generator
import os
from fastapi import FastAPI, File, UploadFile, Form, Response
from starlette.responses import FileResponse
import parse
import urllib.request
import requests

# Create a FastAPI app instance
app = FastAPI()
wd =  os.getcwd()

# Define a route for uploading a file and generating an APK
@app.post("/appGen/")
async def upload_file(file: UploadFile = File(...), appID: str = Form(...)):
    # Save the uploaded file to disk
    status = 100
    message = ""
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())
    
    # Generate APK using the uploaded file
    # Replace this with your actual APK generation code
    try:
        status = 200
        message = "Waiting for APK Generation"
        parseYaml.apkGenerator("./config.yaml", appID)
    except KeyError:
        status = 201
        message = "Error Occurred"
        
    # Return a message indicating success
    return {"status": status, "message": message}

@app.get("/download_file")
def download_file(appID: str):
    # Open the file in binary mode
    
    file_path = f"{wd}/{appID}/apk/app-debug.apk"
    
    #try:
    #    with open(file_path, mode="rb") as file:
    #        file_content = file.read()
    #except FileNotFoundError:
    #    return "File not found"

    # Create a response object with the file content as the body
    #response = Response(content=file_content)

    # Set the content type and disposition headers
    #response.headers["Content-Type"] = "application/octet-stream"
    #response.headers["Content-Disposition"] = f"attachment; filename={file_path.split('/')[-1]}"
    return FileResponse(file_path, media_type='application/octet-stream',filename=f"{appID}.apk")
     

