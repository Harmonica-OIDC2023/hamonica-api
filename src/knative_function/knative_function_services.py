import json
import os

from fastapi import HTTPException


def execute_command_with_json(command):
    try:
        result = os.popen(command).read().strip()
        return json.loads(result)
    except Exception as err:
        raise HTTPException(status_code=404, detail=f"Wrong Input: {err}")


class KnativeFunctionServices:
    @staticmethod
    def create_function_in_knative(function_name: str):
        command = f"func create -l python {function_name}"
        return execute_command_with_json(command)

    @staticmethod
    def deploy_function_in_knative(function_name: str, tenancy_namespace: str):
        command = (
            f"func deploy -p /app/{function_name} -r iad.ocir.io/{tenancy_namespace}"
        )
        return execute_command_with_json(command)

    @staticmethod
    def create_secret_for_registry(
        user_email: str, tenancy_namespace: str, user_password: str
    ):
        command = f"kubectl create secret docker-registry container-registry --docker-server=https://iad.ocir.io/ --docker-email={user_email} --docker-username={tenancy_namespace}/{user_email} --docker-password={user_password}"
        return execute_command_with_json(command)

    @staticmethod
    def k8s_update_with_service_account():
        command = 'kubectl patch serviceaccount default -p "{"imagePullSecrets": [{"name": "container-registry"}]}'
        return execute_command_with_json(command)
