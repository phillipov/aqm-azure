import logging
import azure.functions as func
import azure.cosmos.cosmos_client as cosmos_client


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    readings_table = get_readings_table()
    if not readings_table:
        return func.HttpResponse("can't connect to database", status_code=500)

    if not insert_reading(req, readings_table):
        return func.HttpResponse("can't insert into database", status_code=500)

    return func.HttpResponse("data received", status_code=200)

def insert_reading(req, container):
    sensor_id = get_param(req, 'sensor_id')
    date = get_param(req, 'date')
    time = get_param(req, 'time')
    temp = get_param(req, 'temp')
    humidity = get_param(req, 'humidity')

    reading = {
	    "sensor_id": sensor_id,
	    "date": date,
	    "time": time,
	    "temp": temp,
	    "humidity": humidity
    }

    container.create_item(reading) # broken
    return True

# gets a parameter from a request, checks both URL and JSON parameters
def get_param(req, param_name):
    param = req.params.get(param_name) # check the URL parameter
    if not param: # not in the URL parameters
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            param = req_body.get(param_name) # use the JSON parameter instead
    
    return param

def get_readings_table():
    try:
        url = "https://localhost:8081"
        key = "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
        name = "aqm_db"
        container_id = 'sensor_readings'

        db_client = cosmos_client.CosmosClient(url, {'masterKey': key})
        container = db_client.ReadContainer("dbs/" + name + "/colls/" + container_id)

        return container
    except:
        return False
