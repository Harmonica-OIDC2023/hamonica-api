import re

from fastapi import HTTPException


def is_main_function_matched(text):
    pattern = re.compile(r"def main\([^)]*\)")
    match = re.search(pattern, text)
    if match:
        return match.group()
    return None


class ScriptConverterServices:
    @staticmethod
    def get_oci_python_code_by_knative_python_code(knative_python_code: str):
        matched_result = is_main_function_matched(knative_python_code)

        if not matched_result:
            return HTTPException(404, "This is not knative python code")

        oci_python_code = knative_python_code.replace(
            matched_result, "def main(ctx,data)"
        )
        return oci_python_code

    @staticmethod
    def get_knative_python_code_by_oci_python_code(oci_python_code: str):
        matched_result = is_main_function_matched(oci_python_code)

        if not matched_result:
            return HTTPException(404, "This is not oci python code")

        knative_python_code = oci_python_code.replace(
            matched_result, "def main(context)"
        )
        return knative_python_code
