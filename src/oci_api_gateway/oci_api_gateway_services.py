import json
import os


def execute_command_with_json(command):
    try:
        result = os.popen(command).read().strip()
        return json.loads(result)
    except Exception as err:
        raise Exception(f"Cannot Response Data\n{err}")


class OciApiGatewayServices:
    def create_api_gateway(
        self,
        compartment_id: str,
        endpoint_type: str,
        subnet_id: str,
        api_gateway_name: str,
    ):
        command = f"oci api-gateway gateway create -c {compartment_id} --endpoint-type {endpoint_type} --subnet-id {subnet_id} --display-name {api_gateway_name}"
        return execute_command_with_json(command)

    def get_api_gateway_deployment_list(self, compartment_id: str):
        command = f"oci api-gateway deployment list -c {compartment_id} --all"
        return execute_command_with_json(command)
