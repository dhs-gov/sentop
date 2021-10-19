import logging
import jsonpickle
import azure.functions as func
import azure.durable_functions as df
from datetime import datetime
from util import data_extractor
from util import text_validator
from util import postgres
from util import globalutils
from util import sentop_log
import sentop_config as config
from util import DataType
            

# Generate SENTOP ID from current timestamp.
def generate_sentop_id():
    import datetime
    milliseconds_since_epoch = datetime.datetime.now().timestamp() * 1000
    return str(int(milliseconds_since_epoch))


# Returns id, file_url, is_test, error
def check_query_params(req):
    sentlog = sentop_log.SentopLog()

    valid_endpoint_namesnames = ['sentop', 'sentop-test']
    endpoint_name = req.route_params.get('functionName')
    if endpoint_name not in valid_endpoint_namesnames:
        return None, None, False, "Invalid endpoint name."
    elif endpoint_name == 'sentop-test':
        test_requested = True
        return None, None, test_requested, False

    kms_id = req.params.get('id')

    if not kms_id:
        return None, None, False, "Query parameter 'id' not received."
    elif kms_id.startswith('http') or kms_id.startswith('file'):
        #sentlog.append(f"- Received file URL: {kms_id}")
        # Azure replaces '%20' with spaces, so re-add '%20' since this is
        # required for Windows file URLs.
        file_url = kms_id.replace(" ", "%20")
        sentop_id = generate_sentop_id()
        return "url" + sentop_id, file_url, False, None
    else:
        sentop_id = generate_sentop_id()
        return "kms" + sentop_id, kms_id, False, None


# ================================== M A I N ===================================

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:

    sentlog = sentop_log.SentopLog()
    sentlog.reset()
    sentlog.set_level('DEBUG')

    # ---------------------------- SET LOGGING ---------------------------------

    logging.basicConfig(
        force=True, 
        format='%(asctime)s %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s', 
        datefmt='%Y-%m-%d:%H:%M:%S', 
        level=logging.INFO)

    # Set the logging level for all azure-* libraries
    #logger = logging.getLogger('azure')
    #logger.setLevel(print)

   # -------------------- DELETE EXISTING RUN INSTANCES -----------------------

    # Azure Durable Functions retain instances of runs that do not complete
    # successfully. These instances are queued and re-run at a later time.
    # This re-running of previous instances could lead to unexpected execution
    # of previous runs. To check if previous run instances are queued by Azure,
    # view the storage account by using the Azure Storage Explorer. The
    # following attempts to check for previous runs queued in storage and
    # remove them. Note that this block of code cannot be moved to a function
    # because the 'awaits' keyword must be within scope of the async function.
    # Delete any existing (old) run instances, otherwise previous runs will
    # 'replay'.

    client = df.DurableOrchestrationClient(starter)
    instances = await client.get_status_all()
    # sentlog.append("Previous run instances found: ", len(instances))
    for instance in instances:
        old_instance_id = instance.instance_id
        # Terminate previous run instances
        status = await client.get_status(old_instance_id)
        status_str = str(status.runtime_status)
        #sentlog.append("- Instance Status: ", status_str)
        if status_str == 'OrchestrationRuntimeStatus.Completed':
            purge_results = await client.purge_instance_history(old_instance_id)
            # sentlog.append("Purged instance: ", purge_results)
        else:
            #sentlog.append("Instance NOT COMPLETED-TERMINATING!: ", old_instance_id)
            await client.terminate(old_instance_id, "Trying to terminate")
            purge_results = await client.purge_instance_history(old_instance_id)
            # sentlog.append("Terminated old instance: ", purge_results)
            #sentlog.append("Terminating old instances.")

    # Make sure old instances are deleted
    instances = await client.get_status_all()
    for instance in instances:
        if instance:
            sentlog.warn(f"Old Azure instance still alive.")

   # -------------------------- CHECK QUERY PARAMS -----------------------------

    sentlog.info_h1("Submission")

    sentop_id, kms_id, is_test, error = check_query_params(req)
    if error:
        sentlog.error(f"{error}")
        sentlog.write(sentop_id, config.data_dir_path.get("output"))
        return func.HttpResponse(error, status_code=400)
    if is_test:
        sentlog.info_p("Test request successful.")
        return func.HttpResponse("SENTOP test successful.", status_code=200)

    sentlog.info_keyval(f"KMS ID|{kms_id}")
    sentlog.info_keyval(f"SENTOP ID|{sentop_id}")

   # ---------------------- SAVE REQUEST DATA TO DB ----------------------------

    db = postgres.Database()
    error = db.add_submission(sentop_id, kms_id)
    if error:
        sentlog.error(f"{error}")
        sentlog.write(sentop_id, config.data_dir_path.get("output"))
        return func.HttpResponse(error, status_code=400)

   # ------------------------ GET INCOMING DATA ----------------------------

    sentlog.info_h1("Data")
    data_in, error = data_extractor.get_data(req, sentop_id, kms_id)

    if error:
        return func.HttpResponse(error, status_code=400)
    elif data_in:
        data_in.show_info()
        #if not data_in.row_id_list:
        #    return func.HttpResponse("Error retrieving row ID list.", status_code=400)
        if not data_in.data_list:
            return func.HttpResponse("Error retrieving corpus data.", status_code=400)
        elif data_in.data_type == 2 and not data_in.xlsx_data_table:
            return func.HttpResponse("Error retrieving data table for XLSX data.", status_code=400)
        elif data_in.data_type == 2 and not data_in.headers_row_index:
            return func.HttpResponse("Error retrieving headers row for XLSX data.", status_code=400)
    else:
        return func.HttpResponse("Unknown error getting data.", status_code=400)

    if not data_in.all_stop_words:
        sentlog.warn(f"No stop words found.")

    sentlog.write(sentop_id, config.data_dir_path.get("output"))


   # ------------------ CREATE JSON DATA FOR AZURE ACTIVITY --------------------


    # Since Azure requires that we pass an object that is JSON
    # serializable, we have to convert all data to a JSON object.
    json_obj = jsonpickle.encode(data_in, unpicklable=True)

    if not json_obj:
        sentlog.error("Could not create JSON object from data_in")


    # ------------------------ CREATE NEW INSTANCE -----------------------------

    # Note that "functionName" gets automatically resolved to req.method function name
    # (e.g., 'sentop').
    instance_id = await client.start_new(req.route_params["functionName"], None, json_obj)

    # -------------------------- RETURN RESPONSE -------------------------------

    response = client.create_check_status_response(req, instance_id)
    #sentlog.append("Returned Azure URL links.")

    return response
