#
# CPSC 424-001 SP21
# Term Project
#
# Ben Godfrey (bfgodfr)
# and
# Avery Holder (holder9)
#
# base.py - the backend of our program
#


from __future__ import annotations

from abc import abstractmethod
from enum import Enum
from json import dumps as json_dump
from os import remove as delete_file
from os.path import exists as file_exists
from typing import Any, Final, List, Protocol, TextIO


class SettingType(Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    CHOICE = "choice"


class Setting:
    name: str
    description: str
    kind: SettingType
    path: List[str]
    key: str
    value: Any = None
    value_list: List[str] = None

    def __init__(
        self,
        name: str,
        description: str,
        kind: SettingType,
        path: List[str],
        key: str,
        value: Any = None,
        value_list: List[str] = None,
    ) -> None:

        self.name = name
        self.description = description
        self.kind = kind
        self.path = path
        self.key = key
        self.value = value
        self.value_list = value_list

        if self.value_list is not None and self.kind is not SettingType.CHOICE:
            raise RuntimeError(
                "Settings not of type CHOICE cannot have value lists."
            )

    def get_value_list(self) -> Any:
        return self.value_list

    def get_kind(self) -> Any:
        return self.kind

    def get_value(self) -> Any:
        return self.value

    def set_value(self, value: Any) -> None:
        if self.kind == SettingType.CHOICE:
            if value not in self.value_list:
                raise RuntimeError(
                    "Illegal setting value: {} is not in {}.".format(
                        json_dump(value), json_dump(self.value_list)
                    )
                )
        elif (
            (self.kind == SettingType.BOOLEAN and not isinstance(value, bool))
            or (self.kind == SettingType.NUMBER and not isinstance(value, int))
            or (self.kind == SettingType.STRING and not isinstance(value, str))
        ):
            raise RuntimeError(
                "Setting type mismatch: value {} is not of kind {}.".format(
                    json_dump(value), self.kind
                )
            )

        self.value = value

    def unset(self) -> None:
        self.value = None

    def is_set(self) -> bool:
        return self.value is not None

    def full_path(self) -> str:
        return "/" + "/".join(self.path)

    def fully_qualified_name(self) -> str:
        return f"{self.full_path()}/{self.key}"

    def __str__(self) -> str:
        payload = json_dump(self.value)

        if isinstance(self.value, str):
            # JSON will double-quote strings, we need single-quote.
            payload = f"'{self.value}'"

        return f"{self.key}={payload}"


class SettingGroup:
    title: str
    description: str

    items: List[Setting]

    def __init__(
        self, title: str, description: str, items: List[Setting],
    ) -> None:

        self.title = title
        self.description = description
        self.items = items


class SettingTree:
    name: str

    items: List[Setting]
    subtrees: List[SettingTree]

    def __init__(
        self,
        name: str = "",
        groups: List[SettingGroup] = None,  # should not be none for root.
    ) -> None:

        self.name = name
        self.items = []
        self.subtrees = []

        if groups is None:
            return

        settings: List[Setting] = []
        for group in groups:
            for item in group.items:
                settings.append(item)

        for setting in settings:
            self.insert(setting, setting.path)

    def has_active_items(self) -> bool:
        active_count = 0
        for item in self.items:
            if item.is_set():
                active_count += 1

        return active_count > 0

    def save_to_disk(
        self, path_so_far: List[str], profile_file: TextIO, lock_file: TextIO,
    ) -> None:
        current_path = path_so_far + [self.name]
        current_path_str = "/".join(current_path)

        if self.has_active_items():
            profile_file.write(f"[{current_path_str}]\n")
            for item in self.items:
                if not item.is_set():
                    continue

                profile_file.write(str(item) + "\n")
                lock_file.write(item.fully_qualified_name() + "\n")
            profile_file.write("\n")

        for subtree in self.subtrees:
            subtree.save_to_disk(current_path, profile_file, lock_file)

    def insert(self, setting: Setting, remaining_path: List[str]) -> None:
        # Base case - remaining path is empty.
        if len(remaining_path) < 1:
            self.items.append(setting)
            return

        # Recursive case.
        target = remaining_path[0]
        target_tree = None

        for subtree in self.subtrees:
            if subtree.name == target:
                # IMPORTANT: this is a reference assignment in Python.
                target_tree = subtree

        if target_tree is None:
            target_tree = SettingTree(name=target)
            self.subtrees.append(target_tree)

        target_tree.insert(setting, remaining_path[1:])


class SettingManager:
    groups: List[SettingGroup]

    PROFILE_FILE = "profile.out"  # FIXME
    LOCK_FILE = "locks.out"  # FIXME

    def __init__(self, groups: List[SettingGroup]) -> None:
        self.groups = groups

    def save_to_disk(self) -> None:
        tree = SettingTree(groups=self.groups)

        with open(
            SettingManager.PROFILE_FILE, "w"  # file for profile
        ) as pf, open(
            SettingManager.LOCK_FILE, "w"  # file for locks
        ) as lf:
            tree.save_to_disk([], pf, lf)

    def unlock_all(self) -> None:
        if file_exists(SettingManager.PROFILE_FILE):
            delete_file(SettingManager.PROFILE_FILE)

        if file_exists(SettingManager.LOCK_FILE):
            delete_file(SettingManager.LOCK_FILE)

