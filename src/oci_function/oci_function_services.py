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


def setting_dotenv_with_key(dataset, key_name, key_id):
    try:
        for data in dataset["data"]:
            if data["display-name"] == os.environ[key_name]:
                dotenv.set_key(dotenv_file, key_id, data["id"])
                break
        return dataset, data["id"]
    except Exception as err:
        raise HTTPException(status_code=404, detail=f"Not Found: {err}")


class OciFunctionServices:
    @staticmethod
    def create_function_in_oci(function_name: str):
        command = f"func create -l python {function_name}"
        os.popen(command).read().strip()
        return

    @staticmethod
    def deploy_function_by_id(fnapp_name: str, function_name: str):
        command = f"fn deploy --app {fnapp_name} --working-dir /app/{function_name}"
        os.popen(command).read().strip()
        return

    @staticmethod
    def get_function_by_id(fnapp_id: str):
        command = f"oci fn function list --application-id {fnapp_id} --all"
        function_list = execute_command_with_json(command)
        result, function_id = setting_dotenv_with_key(
            dataset=function_list, key_name="FNFNC_NAME", key_id="FNFNC_ID"
        )
        f = open("./oci-cli/apideploy-spec.json", "r")
        file = f.read().replace("FUNCTION_ID", function_id)
        f.close()
        f = open("./oci-cli/apideploy-spec.json", "w")
        f.write(file)
        f.close()
        return result

    @staticmethod
    def init_function_by_function_name(function_name: str):
        command = f"""fn init --runtime python --entrypoint "/python/bin/fdk /function/func.py main" {function_name}"""
        return os.popen(command).read().strip()
