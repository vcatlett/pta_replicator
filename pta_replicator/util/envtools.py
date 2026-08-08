from importlib.metadata import version
from importlib.util import find_spec


def check_installed(package_name) -> bool:
    # [TODO] Doesn't find PINT...
    return find_spec(package_name) is not None


def check_version(package_name):
    return version(package_name)


def get_package_version(package_name) -> str:
    if check_installed(package_name):
        return check_version(package_name)
    else:
        return None
