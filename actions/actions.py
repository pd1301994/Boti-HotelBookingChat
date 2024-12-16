import csv
from datetime import datetime
from datetime import timedelta
from typing import Text, List, Any, Dict
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk import Action, Tracker
import actions.programs.send_mail as sm


DAY = [str(day) for day in range(1, 32)]
NODAYS = ['1', '2', '3', '4', '5', '6', '7']
NOGUESTS = ['1', '2', '3', '4', '5', '6']
MONTHS = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]
month_mapping = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12"
}

def is_room_available(room_type, entry_date, exit_date, bookings):
    """Comprueba la disponibilidad de la habitación para las fechas solicitadas."""
    for booking in bookings:
        if booking['Room_Type'] == room_type:
            # Verificar si las fechas se solapan
            if not (exit_date <= booking['Entry_Date'] or entry_date >= booking['Exit_Date']):
                return False  
    return True
file_path = "names.csv"
def load_bookings():
    bookings = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Limpiar espacios adicionales en las fechas antes de convertirlas
                row['Entry_Date'] = datetime.strptime(row['Entry_Date'].strip(), "%Y-%m-%d")
                row['Exit_Date'] = datetime.strptime(row['Exit_Date'].strip(), "%Y-%m-%d")
                bookings.append(row)
    except FileNotFoundError:
        # Si el archivo no existe, se crea una lista vacía
        print("File was not found.")
    return bookings
def get_room_type(guest_count):
    if guest_count == 1:
        return "Single"
    elif guest_count == 2:
        return "Double"
    elif 3 <= guest_count <= 7:
        return "Familiar"

class ValidateSimplePizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_booking_form"
    def validate_month(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `month` value."""

        if slot_value not in MONTHS:
            dispatcher.utter_message(
                text=f"Not a valid month, choose one from the dropdown menu {slot_value}."
            )
            return {"month": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"Not a valid month, choose one from the dropdown menu {slot_value}."
            )
            return {"month": None}
        dispatcher.utter_message(text=f"Perfect, you chose: {slot_value}")
        sm.send_mail("2024-01-01", "2024-01-07", 2) 
        return {"month": slot_value}
    def validate_day(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `day` value."""

        if slot_value not in DAY:
            dispatcher.utter_message(
                text=f"This day is not valid {DAY}."
            )
            return {"day": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"This day is not valid {DAY}."
            )
            return {"day": None}
        dispatcher.utter_message(text=f"Perfect, you chose: {slot_value} .")
        return {"day": slot_value}    
    def validate_number_of_days(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `number_of_days` value."""

        if slot_value not in NODAYS:
            dispatcher.utter_message(
                text=f"Not allowed {NODAYS}."
            )
            return {"number_of_days": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"Not allowed {NODAYS}."
            )
            return {"number_of_days": None}
        dispatcher.utter_message(text=f"You will stay: {slot_value} days.")
        return {"number_of_days": slot_value}
    def validate_number_of_guests(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `number_of_guests` value."""

        if slot_value not in NODAYS:
            dispatcher.utter_message(
                text=f"Not valid {NOGUESTS}."
            )
            return {"number_of_guests": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"Nope {NOGUESTS}."
            )
            return {"number_of_guests": None}
        dispatcher.utter_message(text=f"You will be:  {slot_value} people.")
        return {"number_of_guests": slot_value}
    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `name` value."""
        
        if not slot_value or not slot_value.strip():  # Check if slot_value is empty or just whitespace
            dispatcher.utter_message(text="Sorry, I didn´t get your name. Could you repeat it?")
            return {"name": None}
        dispatcher.utter_message(text=f"Hey, {slot_value}.")
        return {"name": slot_value}
    def validate_surname(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `surname` value."""
        
        if not slot_value or not slot_value.strip():  # Check if slot_value is empty or just whitespace
            dispatcher.utter_message(text="Sorry, I didn´t get your surname. Could you repeat it?")
            return {"surname": None}

        dispatcher.utter_message(text=f"And the surname is: {slot_value}.")
        month_slot_value = tracker.get_slot('month').lower()
        month_number = month_mapping.get(month_slot_value)
        number_of_booking_days = int(tracker.get_slot('number_of_days'))
        formatted_date = f"2025-{month_number}-{tracker.get_slot('day').zfill(2)}"
        entry_date = datetime.strptime(formatted_date, "%Y-%m-%d")
        exit_date = entry_date + timedelta(days=number_of_booking_days)
        try:
            bookings = load_bookings()
            
            room_type = get_room_type(number_of_booking_days)
            
            if is_room_available(room_type,entry_date, exit_date, bookings):
                new_booking = {

                'ID_Boking': str(len(bookings) + 1),  
                'Room_Type': room_type,
                'Entry_Date': entry_date.strftime('%Y-%m-%d'),
                'Exit_Date': exit_date.strftime("%Y-%m-%d"),
                'Name': tracker.get_slot('name'),
                'surname': slot_value

            }        
                with open(file_path, mode='a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['ID_Boking','Room_Type','Entry_Date','Exit_Date','Name','surname'])
                    if file.tell() == 0:
                        writer.writeheader()
                    writer.writerow(new_booking)
                
                dispatcher.utter_message(
                    text=f"Your details have been saved: {tracker.get_slot('month')}, "
                        f"{tracker.get_slot('day')}, {tracker.get_slot('name')}, {slot_value}."
                )
                
            else:
                dispatcher.utter_message(
                    text=f"Sorry {tracker.get_slot('name')} the room you wanted is book on the {tracker.get_slot('day')} of {tracker.get_slot('month')}, try another date:()")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred while saving your details: {str(e)}")
        return {"surname": slot_value}  
class ActionResetSlots(Action):
    def name(self) -> str:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        return [tracker.SlotSet("name", None), tracker.SlotSet("surname", None)]

