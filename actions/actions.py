import csv
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ValidateSimplePizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_pizza_form"

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `name` value."""

        if not slot_value or not slot_value.strip():  # Check if slot_value is empty or just whitespace
            dispatcher.utter_message(text="We only accept pizza sizes: s/m/l/xl.")
            return {"name": None}
        
        # Use slot_value directly in the message
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza. CAca de vaca 3 0 .")
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
            dispatcher.utter_message(text="We only accept pizza sizes: s/m/l/xl.")
            return {"surname": None}
        
        # Use slot_value directly in the message
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza. Apellido 3 0 .")
        return {"surname": slot_value}
    
class ActionSaveNameToCSV(Action):
    def name(self) -> Text:
        return "action_save_name_to_csv"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[EventType]:
        """Save the name and surname slots to a CSV file."""
        name = tracker.get_slot("name")
        surname = tracker.get_slot("surname")

        if not name or not surname:
            dispatcher.utter_message(text="I couldn't save your name or surname. Please provide them again.")
            return []

        # Write the name and surname to the CSV file
        file_path = "names.csv"
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([name, surname])
                dispatcher.utter_message(text=f"Your name and surname have been saved: {name} {surname}.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred while saving your details: {str(e)}")
        
        return []
    
