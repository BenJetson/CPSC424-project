from defaults import generate

mgr = generate()

for group in mgr.groups:
    print(f"Group: {group.title}")

    for setting in group.items:
        print(f"    Setting: {setting.name} has value {setting.get_value()} and is type {setting.get_kind()}")

    print("")
