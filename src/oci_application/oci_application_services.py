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


class OciApplicationServices:
    @staticmethod
    def create_application(
        compartment_id: str, fnapp_name: str, subnet_id: str,
    ):
        command = f"""oci fn application create -c {compartment_id} --display-name {fnapp_name} --subnet-ids '["{subnet_id}"]'"""
        return execute_command_with_json(command)

    @staticmethod
    def get_application_list(compartment_id: str):
        command = f"""oci fn application list -c {compartment_id} --all"""
        application_list = execute_command_with_json(command)
        result, _ = setting_dotenv_with_key(
            dataset=application_list, key_name="FNAPP_NAME", key_id="FNAPP_ID"
        )
        return application_list


"""
{
  "compartment_id":"ocid1.tenancy.oc1..aaaaaaaaxaut52vhoboa3dsy7vzwtszofw4wwb32dmvxl7wxgvdtr47evc5a",
  "fnapp_name": "test-cli23",
  "subnet_id": "ocid1.subnet.oc1.iad.aaaaaaaahinl3qiwypplcnsczppekqi7df24yhekeppkadstmmamckgdnosq",
  "ords_base_url": "https://g22889306d9db7d-ph2b6w6cokoq00zp.adb.us-ashburn-1.oraclecloudapps.com/ords/",
  "db_user_secret_ocid": "test_user",
  "db_password_secret_ocid": "Qwerty12345!"
}
"""

"""
ORDS_BASE_URL='https://g22889306d9db7d-ph2b6w6cokoq00zp.adb.us-ashburn-1.oraclecloudapps.com/ords/'
DB_USER_SECRET_OCID='test_user'
DB_PASSWORD_SECRET_OCID='Qwerty12345!'
FNFNC_NAME='product-store-operations-python'
APIGW_NAME='test-cli-gw'
APIDEPLOY_NAME='test-cli-gw-deploy'
"""
