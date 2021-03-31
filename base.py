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

from enum import Enum
from abc import abstractmethod
from json import dumps as json_dump
from typing import Any, Final, List, Protocol, TextIO


class SettingType(Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"


class Setting:
    name: str
    description: str

    kind: SettingType

    path: List[str]
    key: str
    value: Any = None

    def __init__(
        self,
        name: str,
        description: str,
        kind: SettingType,
        path: List[str],
        key: str,
        value: Any = None,
    ) -> None:

        self.name = name
        self.description = description
        self.kind = kind
        self.path = path
        self.key = key
        self.value = value

    def get_value(self) -> Any:
        return self.value

    def set_value(self, value: Any) -> None:
        if (
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
        self.set_value(None)

    def is_set(self) -> bool:
        return self.value is not None

    def full_path(self) -> str:
        return "/".join(self.path)

    def fully_qualified_name(self) -> str:
        return f"{self.full_path()}/{self.key}"

    def __str__(self) -> str:
        payload = f"'{self.value}'"

        if isinstance(self.value, int):
            payload = f"{self.value}"
        elif isinstance(self.value, bool):
            payload = "true" if self.value is True else "false"

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
        if self.has_active_items():
            current_path = path_so_far + [self.name]
            current_path_str = "/".join(current_path)

            profile_file.write(f"[{current_path_str}]\n")
            for item in self.items:
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


class SettingManagerProto(Protocol):
    groups: List[SettingGroup]

    @abstractmethod
    def set_setting(self):
        pass

