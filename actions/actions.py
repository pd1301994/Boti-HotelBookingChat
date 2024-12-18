import csv
from datetime import datetime
from datetime import timedelta
import os
from typing import Text, List, Any, Dict
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk import Action, Tracker
import actions.programs.send_mail as sm
import actions.programs.functionalities as f


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
file_path = "names.csv"


#Mapping the room type according to the number of guests
def get_room_type(guest_count):
    guest_count = int(guest_count)
    if guest_count == 1:
        return "Single"
    elif guest_count == 2:
        return "Double"
    elif 3 <= guest_count <= 7:
        return "Familiar"

class ValidateBookingForm(FormValidationAction):
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
                text=f"Does not work {NOGUESTS}."
            )
            return {"number_of_guests": None}
        # mapping of all the information so its in the correct format to put iut on the csv
        dispatcher.utter_message(text=f"You will be:  {slot_value} people.")
        month_slot_value = tracker.get_slot('month').lower()
        month_number = month_mapping.get(month_slot_value)
        number_of_booking_days = int(tracker.get_slot('number_of_days'))
        formatted_date = f"2025-{month_number}-{tracker.get_slot('day').zfill(2)}"
        entry_date = datetime.strptime(formatted_date, "%Y-%m-%d")
        exit_date = entry_date + timedelta(days=number_of_booking_days)
        noguest = int(slot_value)
        room_type = get_room_type(noguest)
        try:
            bookings = f.load_bookings(file_path)
            if len(bookings)>=1:
                last_row  = bookings[-1]
                id_booking = list(last_row.values())[0]
                email_client =  list(last_row.values())[1]
                name_client =  list(last_row.values())[2]
                surnamename_client =  list(last_row.values())[3]


            file_path_pop = f.remove_last_row(file_path)     
            
            if f.is_room_available(room_type,entry_date, exit_date, bookings):
                new_booking = {

                'ID_Boking': id_booking,  
                'email': email_client,
                'name': name_client,
                'surname': surnamename_client,
                'Room_Type': room_type,
                'Entry_Date': entry_date.strftime('%Y-%m-%d'),
                'Exit_Date': exit_date.strftime("%Y-%m-%d"),              

            }
              
                   
                with open(file_path_pop, mode='a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['ID_Boking','email','name','surname','Room_Type','Entry_Date','Exit_Date'])
                    if file.tell() == 0:
                        writer.writeheader()
                    writer.writerow(new_booking)
                
                dispatcher.utter_message(
                    text=f"Your details have been saved: {tracker.get_slot('month')}, "
                        f"{tracker.get_slot('day')}, {name_client}, {slot_value}."
                )
               
                sm.send_mail(id_booking,email_client,name_client,surnamename_client,entry_date, exit_date, room_type)
                
            else:
                dispatcher.utter_message(
                    text=f"Sorry {name_client} the room you wanted is book on the {tracker.get_slot('day')} of {tracker.get_slot('month')}, try another date)")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred while saving your details: {str(e)}")
        return {"number_of_guests": slot_value}
class ActionResetSlots(Action):
    def name(self) -> str:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        return [tracker.SlotSet("month", None), tracker.SlotSet("day", None), 
                tracker.SlotSet("number_of_days", None),tracker.SlotSet("number_of_guests", None)]

