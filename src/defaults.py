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
                "Theme",
                "Controls which GTK theme to use.",
                SettingType.CHOICE,
                ["org", "gnome", "desktop", "interface"],
                "gtk-theme",
                value_list=[
                    "Yaru",
                    "Yaru-light",
                    "Yaru-dark",
                    "Adwaita",
                    "Adwaita-dark",
                    "HighContrast",
                    "HighContrastInverse",
                ],
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
                "Background shading type",
                "Controls gradient/solid background mode (display mode: none).",
                SettingType.CHOICE,
                ["org", "gnome", "desktop", "background"],
                "color-shading-type",
                value_list=["solid", "horizontal", "vertical"],
            ),
            Setting(
                "Wallpaper",
                "URI of the desktop background image. May be a web address. "
                + "For local files, prefix path with 'file:///'.",
                SettingType.STRING,
                ["org", "gnome", "desktop", "background"],
                "picture-uri",
            ),
            Setting(
                "Primary background color",
                "Hex code of the primary background color.",
                SettingType.STRING,
                ["org", "gnome", "desktop", "background"],
                "primary-color",
            ),
            Setting(
                "Secondary background color",
                "Hex code of the secondary background color.",
                SettingType.STRING,
                ["org", "gnome", "desktop", "background"],
                "secondary-color",
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
        ],
    )

    dock = SettingGroup(
        "Dock and Menu Bar",
        "Control dock and menu bar features.",
        [
            Setting(
                "Dock position",
                "Where the dock appears on the screen.",
                SettingType.CHOICE,
                ["org", "gnome", "shell", "extensions", "dash-to-dock"],
                "dock-position",
                value_list=["LEFT", "BOTTOM", "RIGHT"],
            ),
            Setting(
                "Always show the dock",
                "Whether to keep the dock visible on the display at all times.",
                SettingType.BOOLEAN,
                ["org", "gnome", "shell", "extensions", "dash-to-dock"],
                "dock-fixed",
            ),
            Setting(
                "Show dock on all displays",
                "Whether to show a dock on each display or just the primary.",
                SettingType.BOOLEAN,
                ["org", "gnome", "shell", "extensions", "dash-to-dock"],
                "multi-monitor",
            ),
            Setting(
                "Dock icon size",
                "The maximum size of icons on the dock.",
                SettingType.NUMBER,
                ["org", "gnome", "shell", "extensions", "dash-to-dock"],
                "dash-max-icon-size",
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
            Setting(
                "Show seconds in menu bar",
                "Whether the menu bar displays seconds with the time.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "interface"],
                "clock-show-seconds",
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
                "Lock delay",
                "Number of seconds after idle before the system locks.",
                SettingType.NUMBER,
                ["org", "gnome", "desktop", "screensaver"],
                "lock-delay",
            ),
            Setting(
                "Show notifications when locked",
                "Whether to show notifications on the lock screen.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "notifications"],
                "show-in-lock-screen",
            ),
            Setting(
                "Enable automatic mounts",
                "Whether to automatically mount connected storage devices.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "media-handling"],
                "automount",
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
            Setting(
                "Remember recent applications",
                "Allow the shell to remember recently opened applications.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "privacy"],
                "remember-app-usage",
            ),
            Setting(
                "Auto-delete trashed items",
                "Whether to automatically delete files in trash after a while.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "privacy"],
                "remove-old-trash-files",
            ),
            Setting(
                "Auto-delete temp files",
                "Whether to automatically delete temp files after a while.",
                SettingType.BOOLEAN,
                ["org", "gnome", "desktop", "privacy"],
                "remove-old-temp-files",
            ),
            Setting(
                "Old files age",
                "Number of days to keep old files (if auto-delete is enabled).",
                SettingType.NUMBER,
                ["org", "gnome", "desktop", "privacy"],
                "old-files-age",
            ),
        ],
    )

    login_window = SettingGroup(
        "Login Window",
        "Control login window features.",
        [
            Setting(
                "Show banner message",
                "Whether to show the banner message on the login screen.",
                SettingType.BOOLEAN,
                ["org", "gnome", "login-screen"],
                "banner-message-enable",
            ),
            Setting(
                "Banner message text",
                "The text to display in the banner message, if enabled.",
                SettingType.STRING,
                ["org", "gnome", "login-screen"],
                "banner-message-text",
            ),
            Setting(
                "Disable user list",
                "Do not show the list of users; require manual username entry.",
                SettingType.BOOLEAN,
                ["org", "gnome", "login-screen"],
                "disable-user-list",
            ),
            Setting(
                "Disable power controls",
                "Do not show shutdown/restart/etc options on login window.",
                SettingType.BOOLEAN,
                ["org", "gnome", "login-screen"],
                "disable-restart-buttons",
            ),
            Setting(
                "Login screen logo",
                "Path to a small image displayed on login screen (no prefix).",
                SettingType.STRING,
                ["org", "gnome", "login-screen"],
                "logo",
            ),
        ],
    )

    return SettingManager([appearance, dock, security, privacy, login_window])

