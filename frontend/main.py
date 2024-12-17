import csv
import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import subprocess

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Página del formulario
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@app.post("/submit")
async def process_form(email: str = Form(...)):
    # Rutas de los archivos CSV
    names_csv_path = os.path.join("..", "names.csv")  # Ruta al archivo names.csv
    #booked_csv_path = os.path.join("..", "booked.csv")  # Ruta al archivo booked.csv

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
        return templates.TemplateResponse("index.html", {"request": {}, "email": email, "error": "Error al procesar la reserva."})

    try:
        if last_id==0:
            new_row = [1, email, ""]
        new_row = [last_id + 1, email, ""]
        rows.append(new_row)

        with open(names_csv_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        print("Email añadido al archivo CSV.")
    except Exception as e:
        print(f"Error al guardar el email en booked.csv: {e}")
        return templates.TemplateResponse("index.html", {"request": {}, "email": email, "error": "Error al guardar la reserva."})

    # Llama a otro programa Python y pasa el email
    subprocess.run(["python", "welcome_script.py", email])

    return templates.TemplateResponse("index.html", {"request": {}, "email": email})
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
