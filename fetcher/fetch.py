import json
import requests
import utils

POLICY_GEN_FILE = "https://awspolicygen.s3.amazonaws.com/js/policies.js"

response = requests.get(POLICY_GEN_FILE)

policy_data = response.text.replace("app.PolicyEditorConfig=", "")
policy_data = json.loads(policy_data)

# Write the entire policy generator file
utils.write_file("policy_gen_raw.json", policy_data)

condition_operators = policy_data["conditionOperators"]
# Write all global condition operators
utils.write_file_from_list("policy_global_condition_operators.txt", condition_operators)

condition_keys = policy_data["conditionKeys"]
# Write all global condition keys
utils.write_file_from_list("policy_global_condition_keys.txt", condition_keys)

service_map = policy_data["serviceMap"]

prefixed_actions = []
services         = []

for service in service_map:
    service_full_name   = service
    service_name_prefix = service_map[service]["StringPrefix"] if "StringPrefix" in \
        service_map[service] else []
    service_actions     = service_map[service]["Actions"] if "Actions" in \
        service_map[service] else []
    service_arn_fmt     = service_map[service]["ARNFormat"] if "ARNFormat" in \
        service_map[service] else []
    service_arn_regex   = service_map[service]["ARNRegex"] if "ARNRegex" in \
        service_map[service] else []
    service_cond_keys   = service_map[service]["conditionKeys"] if "conditionKeys" in \
        service_map[service] else []
    service_has_rsrce   = service_map[service]["HasResource"] if "HasResource" in \
        service_map[service] else []

    services.append(service_full_name)

    for action in service_actions:
        prefixed_actions.append(f"{service_name_prefix}:{action}")

    utils.write_file_from_list("policy_actions.txt", prefixed_actions)

utils.write_file_from_list("services.txt", services)
