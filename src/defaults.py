#
# CPSC 424-001 SP21
# Term Project
#
# Ben Godfrey (bfgodfr)
# and
# Avery Holder (holder9)
#
# defaults.py - the default settings for our program
#


from typing import List

from base import Setting, SettingGroup, SettingManager, SettingType


def generate() -> SettingManager:

    appearance = SettingGroup(
        "Appearance",
        "Control how the desktop looks.",
        [
            Setting(
                "Wallpaper",
                "Path to the desktop background image.",
                SettingType.STRING,
                ["org", "gnome", "desktop", "background"],
                "picture-uri",
            ),
            Setting(
                "Wallpaper Display Mode",
                "Controls how the wallpaper image is rendered.",
                SettingType.CHOICE,
                ["org", "gnome", "desktop", "background"],
                "picture-options",
                value_list=[
                    "none",
                    "wallpaper",
                    "centered",
                    "scaled",
                    "stretched",
                    "zoom",
                    "spanned",
                ],
            ),
            Setting(
                "Button icons",
                "Whether buttons display icons.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "interface"],
                "buttons-have-icons",
            ),
            Setting(
                "Menu icons",
                "Whether menu items display icons.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "interface"],
                "menus-have-icons",
            ),
            Setting(
                "Show date in menu bar",
                "Whether the menu bar displays the date.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "interface"],
                "clock-show-date",
            ),
            Setting(
                "Show weekday in menu bar",
                "Whether the menu bar displays the day of the week.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "interface"],
                "clock-show-weekday",
            ),
        ],
    )

    security = SettingGroup(
        "Security",
        "Control system security features.",
        [
            Setting(
                "Lock when idle",
                "Locks the screen after the display has turned off.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "screensaver"],
                "lock-enabled",
            ),
            Setting(
                "Lock on suspend",
                "Locks the screen after the computer goes to sleep.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "screensaver"],
                "ubuntu-lock-on-suspend",
            ),
            Setting(
                "Idle timeout",
                "Number of seconds of inactivity before being considered idle.",
                SettingType.NUMBER,
                ["org", "gnome", "desktop", "session"],
                "idle-delay",
            ),
            Setting(
                "Show notifications when locked",
                "Whether to show notifications on the lock screen.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "screensaver"],
                "show-notifications",
            ),
        ],
    )

    privacy = SettingGroup(
        "Privacy",
        "Control system privacy features.",
        [
            Setting(
                "Disable camera",
                "Prevent applications from accessing the camera.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "privacy"],
                "disable-camera",
            ),
            Setting(
                "Disable microphone",
                "Prevent applications from accessing the microphone.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "privacy"],
                "disable-microphone",
            ),
            Setting(
                "Remember recent files",
                "Allow the shell to remember recently opened files.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "privacy"],
                "remember-recent-files",
            ),
        ],
    )

    return SettingManager([appearance, security, privacy])

