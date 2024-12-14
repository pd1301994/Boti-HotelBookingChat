import csv
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk import Action, Tracker
DAY = ["1", "2", "3"]
MONTHS = ["January", "February", "March"]
month_mapping = {
    "january": "01",
    "february": "02",
    "march": "03",
}
file_path = "names.csv"

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
                text=f"FUCK YOU {slot_value}."
            )
            return {"month": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"a lot of months {slot_value}."
            )
            return {"month": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} MONTHS.")
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
                text=f"FUCK YOU {DAY}."
            )
            return {"day": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"IKeine AHNung {DAY}."
            )
            return {"day": None}
        dispatcher.utter_message(text=f"Day {slot_value} .")
        return {"day": slot_value}
    
    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `name` value."""
        
        if not slot_value or not slot_value.strip():  # Check if slot_value is empty or just whitespace
            dispatcher.utter_message(text="We only accept valid names.")
            return {"name": None}
        dispatcher.utter_message(text=f"OK! Your name is {slot_value}.")
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
            dispatcher.utter_message(text="We only accept valid surnames.")
            return {"surname": None}

        dispatcher.utter_message(text=f"OK! Your surname is {slot_value}.")
        month_slot_value = tracker.get_slot('month').lower()
        month_number = month_mapping.get(month_slot_value)
      
        try:
            with open(file_path, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file) 
                formatted_date = f"2025-{month_number}-{tracker.get_slot('day').zfill(2)}"            
                writer.writerow([
                    formatted_date,                   
                    tracker.get_slot('name'),
                    "2025",
                    slot_value
                ])
            
            # Confirmar que los detalles han sido guardados
            dispatcher.utter_message(
                text=f"Your details have been saved: {tracker.get_slot('month')}, "
                     f"{tracker.get_slot('day')}, {tracker.get_slot('name')}, {slot_value}."
            )
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred while saving your details: {str(e)}")


        return {"surname": slot_value}  
class ActionResetSlots(Action):
    def name(self) -> str:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        return [tracker.SlotSet("name", None), tracker.SlotSet("surname", None)]

   
