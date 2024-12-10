from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict



ALLOWED_PIZZA_TYPES = ["mozzarella", "fungi", "veggie", "pepperoni", "hawaii"]
VEGETARIAN_PIZZAS = ["mozzarella", "fungi", "veggie"]
MEAT_PIZZAS = ["pepperoni", "hawaii"]


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
    
    def validate_birthday(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `birthday` value."""

        if not slot_value or not slot_value.strip():  # Check if slot_value is empty or just whitespace
            dispatcher.utter_message(text="We only accept pizza sizes: s/m/l/xl.")
            return {"birthday": None}
        
        # Use slot_value directly in the message
        dispatcher.utter_message(text=f"Your birthday {slot_value} pizza. BDAY 3 0 .")
        return {"birthday": slot_value}

    
