# This Python file uses the following encoding: utf-8

# Built-in imports
import os

from typing import List

# First-party package imports
from constants import frameworks_constants


def get_frameworks_list() -> List[str]:
    return next(os.walk(frameworks_constants.FRAMEWORKS_DIRECTORY))[1]


def get_sorted_frameworks_list() -> List[str]:
    return sorted(get_frameworks_list())


def get_framework_path(framework_name: str) -> str:
    return os.path.join(frameworks_constants.FRAMEWORKS_DIRECTORY, framework_name)
