import csv
import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import subprocess

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/templates/backgroundimages/{filename}")
async def get_image(filename: str):
    image_path = os.path.join("templates", "backgroundimages", filename)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    return {"error": "Image not found"}

# Página del formulario
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@app.post("/submit")
async def process_form(
    request: Request,  # Asegurarse de incluir el request aquí
    email: str = Form(...),
    name: str = Form(...),
    surname: str = Form(...)
):
    # Rutas de los archivos CSV
    names_csv_path = os.path.join("..", "names.csv")  # Ruta al archivo names.csv

    # Obtener el último booking_id
    try:
        rows = []
        with open(names_csv_path, mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Obtener el nuevo ID_Booking
        if len(rows) > 1:  # Si hay datos en el CSV
            last_id = int(rows[-1][0])  # Último ID en la columna ID_Booking
        else:
            last_id = 0 
    except Exception as e:
        print(f"Error al leer el archivo names.csv: {e}")
        return templates.TemplateResponse("index.html", {"request": request, "email": email, "error": "Error al procesar la reserva."})

    # Guardar los datos en el archivo CSV
    try:
        new_row = [last_id + 1, email, name, surname]
        rows.append(new_row)

        with open(names_csv_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    except Exception as e:
        print(f"Error al guardar los datos en names.csv: {e}")
        return templates.TemplateResponse("index.html", {"request": request, "email": email, "error": "The booking could not be saved."})

    return templates.TemplateResponse("index.html", {"request": request, "email": email, "name": name, "surname": surname})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
