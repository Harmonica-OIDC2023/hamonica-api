import json
import os

import dotenv
from fastapi import HTTPException

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


def execute_command_with_json(command):
    try:
        result = os.popen(command).read().strip()
        return json.loads(result)
    except Exception as err:
        raise HTTPException(status_code=404, detail=f"Wrong Input: {err}")


def health_check_api_gateway(result: str, api_gateway_name: str):
    for data in result["data"]["items"]:
        if data["display-name"] == api_gateway_name:
            if data["lifecycle-state"] == "ACTIVE":
                return data["id"]
            elif data["lifecycle-state"] == "CREATING":
                return None


def get_endpoint(result, api_deploy_name):
    for data in result["data"]["items"]:
        if data["display-name"] == api_deploy_name:
            return data["id"], data["endpoint"]


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

    def get_api_gateway_id(self, compartment_id: str, api_gateway_name: str):
        command = f"oci api-gateway gateway list -c {compartment_id} --all"
        while True:
            result = execute_command_with_json(command=command)
            has_id = health_check_api_gateway(result, api_gateway_name)
            print(has_id, result)
            if has_id is None:
                continue
            return has_id

    def get_api_gateway_deployment_list(
        self, compartment_id: str, api_deploy_name: str
    ):
        command = f"oci api-gateway deployment list -c {compartment_id} --all"
        result = execute_command_with_json(command)
        return get_endpoint(result=result, api_deploy_name=api_deploy_name)

    def create_api_gateway_deploy(
        self,
        compartment_id: str,
        api_gateway_id: str,
        api_display_name: str,
        specification_path: str,
    ):
        # "file://$(pwd)/apideploy-spec.json"
        command = f"""oci api-gateway deployment create -c {compartment_id} --gateway-id {api_gateway_id} --path-prefix "/" --display-name {api_display_name} --specification {specification_path}"""
        return os.popen(command).read().strip()
