import re


def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/",session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string
    return ""

def get_str_from_food_dict(food_dict: dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])

if __name__ == "__main__":
    print(get_str_from_food_dict({'pizza':1, "mango_lassi":3}))
#     print(extract_session_id( "projects/nutrinet-chatbot-urse/agent/sessions/61979092-861a-e432-335b-0b040f6095c2/contexts/ongoing-order"))