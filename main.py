from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import re

app = FastAPI()

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    image = Image.open(file.file)
    text = pytesseract.image_to_string(image)

    # Extract two numbers and operator
    match = re.search(r'(\d+)\s*[*xX×]\s*(\d+)', text)
    if match:
        a = int(match.group(1))
        b = int(match.group(2))
        return {
            "answer": a * b,
            "email": "24f1002255@ds.study.iitm.ac.in"
        }
    else:
        return JSONResponse(content={"error": "Could not extract multiplication"}, status_code=400)