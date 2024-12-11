import csv
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk import Action, Tracker
file_path = "names.csv"

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
        try:
            with open(file_path, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([tracker.get_slot("name"), slot_value])  # Save name and surname
                dispatcher.utter_message(text=f"Your details have been saved: {tracker.get_slot('name')}, {slot_value}.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred while saving your details: {str(e)}")

        return {"surname": slot_value}
class ActionResetSlots(Action):
    def name(self) -> str:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        return [tracker.SlotSet("name", None), tracker.SlotSet("surname", None)]

   
