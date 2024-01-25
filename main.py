from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import json
import db_helper   
import re
import genaric_helper

inprogress_orders ={}

app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "JAYANTH IS THE WINNER"}


# inprogress_orders = {
#     "session_id_1": {"pizza":2,"mango_lassi": 1},
#     "session_id_2": {"samosa":5,"rava dosa":2}
# }

@app.post("/")
async def handle_request(request: Request):
    # REtrieve the Json data from the request
    payload = await request.json()

    # Extract the neccessary information from the palyoad
    # based on teh sturecture of the WebhookRequestion
    intent = payload['queryResult']['intent']['displayName']
    parameters= payload['queryResult']['parameters']
    outputContexts = payload['queryResult']['outputContexts']

    session_id = genaric_helper.extract_session_id(outputContexts[0]['name'])


    intent_handler_dict = {
        'new.order': new_order,
        'order.add - context ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order.complete - context: ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order
        }

    return intent_handler_dict[intent](parameters, session_id)


def add_to_order(paramters: dict, session_id: str):
    food_items = paramters["food-item"]
    qunatities = paramters["number"]

    if len(food_items) != len(qunatities):
        fulfillment_text = "Sorry I didn't understood. Can you please specify food items and quantities clearly"
    else:
        new_food_dict = dict(zip(food_items, qunatities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        print("************")
        print(inprogress_orders)

        order_str = genaric_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?" 

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def new_order(parameters:dict, session_id: str): #session_id: str
    if session_id in inprogress_orders:
        # Clear the existing order for the given session_id
        del inprogress_orders[session_id]
    else:
        # If it's the first time, just print the new order message
        return JSONResponse(content={
            "fulfillmentText": "ok, starting a new order. You can say things like 'I want two pizzas and one mango lassi'. "
                               "Make sure to specify a quantity for every food item! Also, we have only the following items on our menu: "
                               "Pav Bhaji, Chole Bhature, Pizza, Mango Lassi, Masala Dosa, Biryani, Vada Pav, Rava Dosa, and Samosa."
        })

    return JSONResponse(content={
        "fulfillmentText": "Ok, starting a new order. You can say things like 'I want two pizzas and one mango lassi'. "
                           "Make sure to specify a quantity for every food item! Also, we have only the following items on our menu: "
                           "Pav Bhaji, Chole Bhature, Pizza, Mango Lassi, Masala Dosa, Biryani, Vada Pav, Rava Dosa, and Samosa."
    })


def complete_order(parameters:dict,session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! can you place a new order please"

    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)

        if order_id ==-1:
            fulfillment_text = "Sorry, I couldn't proccess your order dur to a backend error." \
            "Please place a new order again"
        else:
            order_total = db_helper.get_total_order_price(order_id)
            fulfillment_text = f"Awesome. We have placed your order. " \
                            f"Here is your order id # {order_id}. " \
                            f"Your order total is {order_total} which you can pay at the time of delivery!"

        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })  


def save_to_db(order:dict):
    # order = {"pizza":1, "chole":2}
    next_order_id = db_helper.get_next_order_id()

    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1
    
    db_helper.insert_order_tracking(next_order_id,"in progress")

    return next_order_id

# step1: locate the session id record:  
# step 2: get teh value form dict : {"pizza":2,"mango_lassi": 1}
# step 3: remove the food items. request: ["vada pav", "pizza"]
 
def remove_from_order(parameters: dict, session_id: str):
    """Removes items from an ongoing order based on provided parameters."""

    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having trouble finding your order. Sorry! Can you place a new order?"
        })
  
    current_order = inprogress_orders[session_id]
    food_items = parameters["food-item"]
    quantity = parameters["number"]
    no_such_items = []
    removed_items = []
    print(inprogress_orders[session_id])


    for item in food_items:
        quantity_to_remove = int(quantity[0])  # Reset for each item

        if item not in current_order:
            no_such_items.append(item)
        else:
            print(inprogress_orders[session_id])
            if quantity_to_remove >= int(inprogress_orders[session_id][item]):
                removed_items.append(item)
                del current_order[item]
            else:
                current_order[item] -= quantity_to_remove
                removed_items.append(f"{quantity_to_remove} {item}")

    fulfillment_text = ""

    if len(removed_items) > 0:
        fulfillment_text += f'Removed {", ".join(removed_items)} from your order!'
    elif len(no_such_items) > 0:
        fulfillment_text += f"I couldn't find {', '.join(no_such_items)} in your order."

    if len(current_order) == 0:
        fulfillment_text += "Your order is empty!"
    else:
        order_str = genaric_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"Remaining items in your order: {order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



def track_order(parameters:dict, session_id: str):
    order_id = int(parameters['number'])
    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is : {order_status}"
    else:
        fulfillment_text = f"No order found with order id:{order_id}"

    return JSONResponse(content={
            "fulfillmentText": fulfillment_text
        })
