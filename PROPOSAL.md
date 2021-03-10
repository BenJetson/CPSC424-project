# Project Proposal

CPSC 424-001 SP21 &bullet; Ben Godfrey (bfgodfr) and Avery Holder (holder9)

## Logistics

For our project, we have chosen the third option:

> Develop an open-source system administration tool that assists with system
> security tasks.

## Objective

We plan to create a utility that allows system administrators to manage Dconf
configuration locks. Our utility will allow administrators to set the value of a
particular setting and then lock it such that it applies system-wide and users
cannot change it.

The utility will support reading and writing both the Dconf system configuration
and lock files so they can be updated over time easily.

## Background

The Dconf system is a part of the GNOME desktop environment and is used to
manage both user-level and system-level preferences for how GNOME behaves. GNOME
desktop documentation provides an example of how administrators may [set a
preference at the system level][doc-sys-setting] and how administrators may then
[lock a preference][doc-lock-setting] but does not provide an easy way to do
this without writing the files by hand.

## Relevance

There are many desktop settings in GNOME which administrators may wish to lock
to a particular value for security or usability purposes. For example:

- how long before the screen goes blank
- whether screen lock is enabled or disabled
- desktop wallpaper (perhaps company branding)
- whether or not notifications are shown when user is away
- whether or not to empty trashed files automatically

Considering that GNOME does not currently expose a simple interface for doing
this beyond writing the configuration files yourself, this could be a
significant entry barrier for many novice administrators. Our utility will take
this burden away and give administrators the ability to write these
configuration files correctly without spending much time.

## Implementation

Our current plan is to implement this in Python with a GUI for administrators to
change their setting locks. If the GUI programming proves to be a challenge
given the short time constraints, we may fall back to a command-line interface
instead.

<!-- Hyperlinks -->

[doc-sys-setting]:
  https://help.gnome.org/admin/system-admin-guide/stable/desktop-background.html.en
[doc-lock-setting]:
  https://help.gnome.org/admin/system-admin-guide/stable/dconf-lockdown.html.en
