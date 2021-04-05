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
from json import loads as json_load
from os import getenv, makedirs
from os import remove as delete_file
from subprocess import run as proc_open
from os.path import exists as file_or_dir_exists
from typing import Any, Final, List, Protocol, TextIO


def is_debug_mode() -> bool:
    return getenv("DEBUG") is not None


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
        return "/".join(self.path)

    def fully_qualified_name(self) -> str:
        return f"/{self.full_path()}/{self.key}"

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

    def try_merge_values(self, other: SettingGroup) -> None:
        for my_item in self.items:
            my_fqn = my_item.fully_qualified_name()

            for other_item in other.items:
                if my_fqn == other_item.fully_qualified_name():
                    try:
                        my_item.set_value(other_item.get_value())
                    except RuntimeError as e:
                        print(
                            f"Could not set {my_item.fully_qualified_name()} "
                            + f"to stored value of {other_item.get_value()}. \n"
                            + f"\tReceived: {e}"
                        )

                    other.items.remove(other_item)

                    # not breaking here would cause strange iteration since we
                    # are removing from the list we are iterating over.
                    # Fortunately, we need to break anyway.
                    break


class SettingTree:
    name: str

    items: List[Setting]
    subtrees: List[SettingTree]

    def __init__(
        self,
        name: str = "",
        groups: List[SettingGroup] = None,  # should not be none for root.
        setting_file_name: str = None,  # should not be none for load.
    ) -> None:

        self.name = name
        self.items = []
        self.subtrees = []

        if groups is not None and setting_file_name is not None:
            raise RuntimeError(
                "cannot construct from groups and disk simultaneously"
            )
        elif groups is not None:
            self.construct_from_groups(groups)
        elif setting_file_name is not None:
            self.construct_from_disk(setting_file_name)

    def has_active_items(self) -> bool:
        active_count = 0
        for item in self.items:
            if item.is_set():
                active_count += 1

        return active_count > 0

    def save_to_disk(
        self, path_so_far: List[str], setting_file: TextIO, lock_file: TextIO,
    ) -> None:
        current_path = path_so_far + [self.name] if self.name != "" else []
        current_path_str = "/".join(current_path)

        if self.has_active_items():
            setting_file.write(f"[{current_path_str}]\n")
            for item in self.items:
                if not item.is_set():
                    continue

                setting_file.write(str(item) + "\n")
                lock_file.write(item.fully_qualified_name() + "\n")
            setting_file.write("\n")

        for subtree in self.subtrees:
            subtree.save_to_disk(current_path, setting_file, lock_file)

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

    def construct_from_groups(self, groups: List[SettingGroup]) -> None:
        settings: List[Setting] = []
        for group in groups:
            for item in group.items:
                settings.append(item)

        for setting in settings:
            self.insert(setting, setting.path)


class SettingManager:
    groups: List[SettingGroup]

    login_profile_file: str
    user_profile_file: str
    setting_file: str
    lock_file: str

    def __init__(self, groups: List[SettingGroup]) -> None:
        self.groups = groups

        self.login_profile_file = "/etc/dconf/profile/gdm"
        self.user_profile_file = "/etc/dconf/profile/user"
        self.setting_file = "/etc/dconf/db/local.d/00_setting_mgr"
        self.lock_file = "/etc/dconf/db/local.d/locks/00_setting_mgr"

        if is_debug_mode():
            self.login_profile_file = "profile-login.out"
            self.user_profile_file = "profile-user.out"
            self.setting_file = "settings.out"
            self.lock_file = "locks.out"

    def do_dconf_update(self) -> None:
        if not is_debug_mode():
            proc_open(["/usr/bin/dconf", "update"])

    def save_to_disk(self) -> None:
        tree = SettingTree(groups=self.groups)

        if not is_debug_mode() and not file_or_dir_exists(
            "/etc/dconf/db/local.d/locks"
        ):
            # When running without debug mode, we must ensure that this full
            # directory structure exists, and create it if not.
            makedirs("/etc/dconf/db/local.d/locks")

        with open(self.login_profile_file, "w") as pf:
            pf.writelines(
                [
                    "user-db:user\n",
                    "system-db:local\n",
                    "file-db:/usr/share/gdm/greeter-dconf-defaults\n",
                ]
            )

        with open(self.user_profile_file, "w") as pf:
            pf.writelines(["user-db:user\n", "system-db:local\n"])

        with open(self.setting_file, "w") as sf, open(  # file for profile
            self.lock_file, "w"  # file for locks
        ) as lf:
            tree.save_to_disk([], sf, lf)

        self.do_dconf_update()

    def load_from_disk(self) -> None:
        if not file_or_dir_exists(self.setting_file):
            return

        merge_group = SettingGroup(
            "Merge", "Scratch group for merging ops.", []
        )

        with open(self.setting_file, "r") as sf:
            path: List[str] = None

            for line in sf.readlines():
                line = line.rstrip()

                # ignore blank lines; these are just for humans.
                if len(line) == 0:
                    continue

                if line[0] == "[" and line[-1] == "]":
                    path_str = line[1:-1]
                    path = path_str.split("/")
                    continue

                equal_idx = line.index("=")

                if path is None:
                    raise RuntimeError(
                        "invalid format: found key-value pair before path"
                    )
                elif equal_idx == -1:
                    raise RuntimeError(
                        "malformed key-value pair: no equals sign in expression"
                    )

                key = line[:equal_idx]
                value_str = line[equal_idx + 1 :]
                value: Any = None
                kind = SettingType.STRING

                if value_str[0] == "'" and value_str[-1] == "'":
                    value = value_str[1:-1]
                else:
                    value = json_load(value_str)

                    if isinstance(value, int):
                        kind = SettingType.NUMBER
                    elif isinstance(value, bool):
                        kind = SettingType.BOOLEAN

                s = Setting(
                    "unknown",  # cannot infer title from file; not stored!
                    "unknown",  # cannot infer description from file; not stored!
                    kind,
                    path,
                    key,
                    value,
                )

                merge_group.items.append(s)

        for group in self.groups:
            group.try_merge_values(merge_group)

    def unlock_all(self) -> None:
        targets = [
            self.login_profile_file,
            self.user_profile_file,
            self.setting_file,
            self.lock_file,
        ]

        for f in targets:
            if file_or_dir_exists(f):
                delete_file(f)

        self.do_dconf_update()

