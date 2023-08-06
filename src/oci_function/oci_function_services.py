import json
import os


def execute_command_with_json(command):
    result = os.popen(command).read().strip()
    return json.loads(result)


class OciFunctionServices:
    @staticmethod
    def deploy_function(fnapp_name: str):
        command = f"fn deploy --app {fnapp_name}"
        return execute_command_with_json(command)

    @staticmethod
    def get_function_list(fnapp_id: str):
        command = f"oci fn function list --application-id {fnapp_id} --all"
        return execute_command_with_json(command)
