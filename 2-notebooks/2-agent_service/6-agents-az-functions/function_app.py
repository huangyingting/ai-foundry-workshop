import os
import json
import logging
import azure.functions as func
from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy

app = func.FunctionApp()

@app.function_name(name="FooReply")
@app.queue_output(
    arg_name="outputQueueItem", 
    queue_name="azure-function-foo-output", 
    connection="STORAGE_CONNECTION")
@app.queue_trigger(
    arg_name="inmsg",
    queue_name="azure-function-foo-input",
    connection="STORAGE_CONNECTION"  # or connection string setting name
)
def run_foo(inmsg: func.QueueMessage, outputQueueItem: func.Out[str]) -> None:
    logging.info("Azure Function triggered with a queue item.")

    # Parse the function call payload, e.g. { "Query": "Hello?", "CorrelationId":"..."}

    payload = json.loads(inmsg.get_body().decode('utf-8'))
    query = payload.get("Query", "")
    correlation_id = payload.get("CorrelationId", "")

    # Example: We'll return a comedic 'Foo says: <some witty line>'
    result_message = {
        "FooReply": f"This is Foo, responding to: {query}! Stay strong 💪!",
        "CorrelationId": correlation_id
    }

    # Put the result on the output queue
    outputQueueItem.set(json.dumps(result_message).encode('utf-8'))
    logging.info(f"Sent message: {result_message}")