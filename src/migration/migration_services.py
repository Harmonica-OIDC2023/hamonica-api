import os

from fastapi import File, UploadFile

from src.knative_function.knative_function_services import KnativeFunctionServices
from src.oci_api_gateway.oci_api_gateway_services import OciApiGatewayServices
from src.oci_application.oci_application_services import OciApplicationServices
from src.oci_function.oci_function_services import OciFunctionServices
from src.script_converter.script_converter_services import ScriptConverterServices


def setting_oci_config(user: str, fingerprint: str, tenancy: str, region: str):
    return f"""[DEFAULT]\nuser={user}\nfingerprint={fingerprint}\ntenancy={tenancy}\nregion={region}\nkey_file=/root/.oci/harmonica2023-oci.pem"""


def setting_oci_function_config(api_url: str, compartment_id: str, registry: str):
    return f"""api-url: {api_url}\noracle.compartment-id: {compartment_id}\noracle.profile: DEFAULT\nprovider: oracle\nregistry: iad.ocir.io/{registry}/test"""


def setting_common_process(docker_pw, docker_registry, user_email):
    os.environ["DOCKER_PWD"] = docker_pw
    os.environ["DOCKER_REGISTRY"] = docker_registry
    os.environ["OCI_EMAIL"] = user_email

    os.popen("chmod 600 /root/.oci/*").read().strip()
    os.popen(
        f"docker login -u {docker_registry}/{user_email} iad.ocir.io -p {docker_pw}"
    ).read().strip()


def get_oci_config_path():
    return "/root/.oci"


def get_oci_function_config_path():
    return "/root/.fn"


def get_oci_function_path():
    return "/root/oci-cli"


def save_oci_config(config_string: str):
    oci_config_folder_path = get_oci_config_path()
    text_file = open(f"{oci_config_folder_path}/config", "w")
    text_file.write(config_string)
    text_file.close()


def save_oci_function_config(config_string: str):
    oci_function_config_path = get_oci_function_config_path()
    text_file = open(f"{oci_function_config_path}/contexts/default.yaml", "w")
    text_file.write(config_string)
    text_file.close()


def save_key_file(pem_file: File):
    oci_config_folder_path = get_oci_config_path()
    text_file = open(f"{oci_config_folder_path}/harmonica2023-oci.pem", "wb")

    text_file.write(pem_file)
    text_file.close()


def save_python_script(python_file: File):
    oci_function_path = get_oci_function_path()
    text_file = open(f"{oci_function_path}/my-func/func.py", "wb")
    text_file.write(python_file)
    text_file.close()


def save_python_package_file(req_file: File):
    oci_function_path = get_oci_function_path()
    text_file = open(f"{oci_function_path}/my-func/requirements.txt", "wb")
    text_file.write(req_file)
    text_file.close()


def get_oci_function_id(oci_application_list, application_name: str):
    for item in oci_application_list["data"]:
        if item["display-name"] != application_name:
            continue
        return item["id"]


def get_api_gateway_id(api_gateway_deployment_list, api_gateway_name: str):
    for item in api_gateway_deployment_list["data"]["items"]:
        if item["display-name"] != api_gateway_name:
            continue
        return item["gateway-id"]


class MigrationServices:
    @staticmethod
    def set_oci(
        user: str,
        fingerprint: str,
        tenancy: str,
        region: str,
        subnet_id: str,
        fnapp_name: str,
        compartment_id: str,
        api_gateway_deploy_name: str,
        api_gateway_name: str,
        registry: str,
        api_url: str,
        key_pem: bytes,
        function_name: str,
        docker_registry: str,
        docker_pw: str,
        user_email: str,
        requirements: bytes,
        func_file: bytes,
    ):
        setting_common_process(docker_pw, docker_registry, user_email)
        script_converter_services = ScriptConverterServices()
        func_file_str = script_converter_services.get_oci_python_code_by_knative_python_code(
            func_file.decode("utf-8")
        )
        save_python_script(python_file=func_file_str.encode("utf-8"))
        save_python_package_file(req_file=requirements)

        config_detail = setting_oci_config(
            user=user, fingerprint=fingerprint, tenancy=tenancy, region=region
        )

        config_function_detail = setting_oci_function_config(
            api_url=api_url, compartment_id=compartment_id, registry=registry
        )

        save_oci_config(config_string=config_detail)
        save_oci_function_config(config_string=config_function_detail)

        save_key_file(pem_file=key_pem)

        oci_application_services = OciApplicationServices()
        oci_function_services = OciFunctionServices()
        oci_api_gateway_services = OciApiGatewayServices()

        oci_function_services.init_function_by_function_name(
            function_name=function_name
        )
        oci_application_services.create_application(
            compartment_id=compartment_id, fnapp_name=fnapp_name, subnet_id=subnet_id
        )
        oci_function_services.deploy_function_by_id(
            fnapp_name=fnapp_name, function_name=function_name
        )
        oci_application_list = oci_application_services.get_application_list(
            compartment_id=compartment_id
        )
        fnapp_id = get_oci_function_id(
            oci_application_list=oci_application_list, application_name=fnapp_name
        )
        oci_function_services.get_function_by_id(fnapp_id=fnapp_id)
        # oci_api_gateway_services.create_api_gateway(
        #     compartment_id=compartment_id,
        #     endpoint_type="PUBLIC",
        #     subnet_id=subnet_id,
        #     api_gateway_name=api_gateway_name,
        # )
        api_gateway_id = oci_api_gateway_services.get_api_gateway_id(
            compartment_id=compartment_id, api_gateway_name=api_gateway_name
        )
        oci_api_gateway_services.create_api_gateway_deploy(
            compartment_id=compartment_id,
            api_gateway_id=api_gateway_id,
            api_display_name=api_gateway_deploy_name,
            specification_path="file:///app/oci-cli/apideploy-spec.json",
        )
        _, endpoint = oci_api_gateway_services.get_api_gateway_deployment_list(
            compartment_id=compartment_id, api_deploy_name=api_gateway_deploy_name
        )
        return endpoint

    @staticmethod
    def set_knative(
        docker_registry: str,
        docker_pw: str,
        user_email: str,
        function_name: str,
        requirements: bytes,
        func_file: bytes,
    ):
        setting_common_process(docker_pw, docker_registry, user_email)

        script_converter_services = ScriptConverterServices()
        func_file_str = script_converter_services.get_knative_python_code_by_oci_python_code(
            func_file.decode("utf-8")
        )

        save_python_script(python_file=func_file_str.encode("utf-8"))
        save_python_package_file(req_file=requirements)

        knative_function_services = KnativeFunctionServices()
        knative_function_services.create_function_in_knative(
            function_name=function_name
        )
        # knative_function_services.create_secret_for_registry(
        #     user_email=user_email,
        #     tenancy_namespace=docker_registry,
        #     user_password=docker_pw,
        # )
        #
        # knative_function_services.k8s_update_with_service_account()
        # knative_function_services.deploy_function_in_knative(
        #     function_name=function_name, tenancy_namespace=docker_registry
        # )
