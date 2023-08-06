import json
import os


def execute_command_with_json(command):
    try:
        result = os.popen(command).read().strip()
        return json.loads(result)
    except Exception as err:
        raise Exception(f"Cannot Response Data\n{err}")


class OciApplicationServices:
    @staticmethod
    def create_application(
        compartment_id: str,
        fnapp_name: str,
        subnet_id: str,
        ords_base_url: str,
        db_user_secret_ocid: str,
        db_password_secret_ocid: str,
    ):
        command = f"""oci fn application create -c {compartment_id} --display-name {fnapp_name} --subnet-ids '["{subnet_id}"]' --config \"{{'ORDS_BASE_URL': '{ords_base_url}','DB_USER_SECRET_OCID': '{db_user_secret_ocid}','DB_PASSWORD_SECRET_OCID': '{db_password_secret_ocid}'}}\""""
        return execute_command_with_json(command)

    @staticmethod
    def get_application_list(compartment_id: str):
        command = f""" oci fn application list -c {compartment_id} --all"""
        return execute_command_with_json(command)


"""
{
  "compartment_id": "ocid1.tenancy.oc1..aaaaaaaagkmgmjlchsvkyk2xfuvr5hhlqklr5ppah66n6k47z2dy7xn2wjuq",
  "fnapp_name": "test-cli2",
  "subnet_id": "ocid1.subnet.oc1.iad.aaaaaaaak5xcagncijm745pg2qlzu6tulscelmchewge5jp4wmhbcpg2tyka",
  "ords_base_url": "https://g8bb70b33c2435e-tu6gicbkl30gnyja.adb.us-ashburn-1.oraclecloudapps.com/ords/",
  "db_user_secret_ocid": "test_user",
  "db_password_secret_ocid": "Qwerty12345!"
}
"""
