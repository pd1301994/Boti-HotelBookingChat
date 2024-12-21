import csv
from datetime import datetime

#get all the bookings and formating the date
def load_bookings(file_path):
    bookings = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Evitar errores si el archivo solo contiene el header o hay celdas vacías
                if any(row.values()):
                    # Validar que las fechas existan y no sean None antes de limpiar y convertir
                    entry_date = row['Entry_Date']
                    exit_date = row['Exit_Date']

                    if entry_date and entry_date.strip():
                        row['Entry_Date'] = datetime.strptime(entry_date.strip(), "%Y-%m-%d")
                    else:
                        row['Entry_Date'] = None

                    if exit_date and exit_date.strip():
                        row['Exit_Date'] = datetime.strptime(exit_date.strip(), "%Y-%m-%d")
                    else:
                        row['Exit_Date'] = None

                    bookings.append(row)

    except FileNotFoundError:
        print("File was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return bookings

#checking if the room is available in the desire dates
def is_room_available(room_type, entry_date, exit_date, names):
    """Comprueba la disponibilidad de la habitación para las fechas solicitadas."""
    if not names:
        return True
    for booking in names:
        if booking['Room_Type'] == room_type:
            if not (exit_date <= booking['Entry_Date'] or entry_date >= booking['Exit_Date']):
                return False  
    return True

def remove_last_row(file_path):
    try:
        # Read all rows from the CSV
        with open(file_path, mode="r", newline='') as read_file:
            reader = csv.reader(read_file)
            rows = list(reader)  # Convert to list

        # Check if there are more than just the header
        if len(rows) > 1:
            rows.pop()  # Remove the last row

        # Write the remaining rows back to the CSV
        with open(file_path, mode='w', newline='') as write_file:
            writer = csv.writer(write_file)
            writer.writerows(rows)  # Write all remaining rows (including header)
        return file_path

    except Exception as e:
        print(f"An error occurred while trying to remove the last row: {str(e)}")


