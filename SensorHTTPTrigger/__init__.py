import logging
import azure.functions as func
import azure.cosmos.cosmos_client as cosmos_client


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    client = get_client()
    
    if not client:
        return func.HttpResponse("can't connect to Azure client", status_code=500)

    collection = get_collection_url()

    if not insert_reading(req, client, collection):
        return func.HttpResponse("can't insert into database", status_code=500)

    return func.HttpResponse("data received", status_code=200)

def insert_reading(req, client, collection):
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

    try:
        client.CreateItem(collection, reading)
        return True
    except:
        return False


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

def get_client():
    url = "https://localhost:8081"
    # this is an emulator key, good luck stealing my credits
    key = "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="

    try:
        client = cosmos_client.CosmosClient(url, {'masterKey': key})
        return client
    except:
        return False

def get_collection_url():
    name = "aqm_db"
    container_id = 'sensor_readings'
    return ("dbs/" + name + "/colls/" + container_id)