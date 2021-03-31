# Final Project - Milestone 2

CPSC 424-001 SP21 &bullet; Ben Godfrey (bfgodfr) and Avery Holder (holder9)

## Summary

Our plan is to make a utility that allows system administrators to manage dconf
configuration locks. This will allow system admins to change a setting and then
lock it such that normal users are not able to change these settings.

## Current Work

The program is being written in Python 3. This is because Python is an easy to
use programming language and it also makes the program very easy to run on many
different types of systems. Furthermore, its dynamic typing system makes it
simple to create generics for different setting types. The program is structured
as two to three different Python files.

The first file is the backend of the program. This is where most of the main
program will be, and this is what will actually generate the Dconf configuration
files. It contains several data structures and functions that will be used by
the frontend.

The second file is the frontend of the program and contains the code necessary
for the graphical user interface. This will allow the user to use a GUI to
interact and generate the Dconf configuration file, then apply it to the system
such that a normal user is not allowed to change the values.

We are starting by writing the backend of the program as that is the most
important piece. Should we run into a time crunch, this part of the program will
work even without a graphical user interface. However, we believe we will have
plenty of time to complete the entire graphic frontend in addition to the
backend.

Since code we have so far does not have any kind of user interface available we
must make our own calls to the methods to test the program. Fortunately, Python
makes this easy to do because of its native REPL shell.

## Resources

The resources we have so far are purely related to the mechanisms in the
operating system that we must employ to lock down settings.

- Documentation for dconf configuration in Ubuntu:
  http://manpages.ubuntu.com/manpages/bionic/man7/dconf.7.html
- Documentation for GNOME-specific dconf settings:
  https://help.gnome.org/admin/system-admin-guide/stable/dconf-lockdown.html.en
- More detailed explanation of dconf profiles and their use:
  https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/desktop_migration_and_administration_guide/configuration-overview-gsettings-dconf

## Enclosure

Attached to this submission, please find enclosed a copy of base.py, which
contains the current state of the program’s backend.
