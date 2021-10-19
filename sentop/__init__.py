import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    #print("Running sentiment orchestrator")

    json_obj = context.get_input()

    result1 = yield context.call_activity('sentop_activity', json_obj)
    #print("RESULT: ", result1)
    context.set_custom_status("NOTE: Asynchronous Azure Durable Functions add quotes around JSON output and also adds escaped double quotes around keys and values.")
    return [result1]


main = df.Orchestrator.create(orchestrator_function)