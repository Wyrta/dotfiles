#!/usr/bin/env python3
import sys
import subprocess
import re
import os

def get_info() -> str:
    sink = subprocess.run(
        ["pactl", "list", "sinks"],
        capture_output = True, # Python >= 3.7 only
        text = True # Python >= 3.7 only
    ).stdout
    
    return sink


def proc_devices(sinks: str) -> list:

# Sink #(?P<id>[0-9])+$\n\tState: (?P<state>.*)\n\tName:(?P<name>.*)$\n\tDescription: (?P<description>.*)$\n.*\n.*\n.*\n.*\n\tMute: (?P<muted>(?:yes)|(?:no))$
    pattern = r"Sink #(?P<id>[0-9])+$\n\tState: (?P<state>.*)\n\tName: (?P<name>.*)$\n\tDescription: (?P<description>.*)$\n.*\n.*\n.*\n.*\n\tMute: (?P<muted>(?:yes)|(?:no))$"
    
    matches = re.findall(pattern, sinks, re.MULTILINE)

    return matches


def print_choice(choices: list):
    
    for match in choices:
        output = f"{match[3]}"

        # if match[4] == "yes":
         #   output += " Muted"

        print(output)

    print("Quit")


def main():
    os.environ["LC_ALL"] = "C"

    sinks = get_info()

    devices = proc_devices(sinks)
    
    arg = sys.argv[-1]

    if arg == "Quit":
        return
    
    for device in devices:
        if arg.find(device[3]) >= 0:
            output = subprocess.run(
                ["pactl", "set-default-sink", device[2]],
                capture_output = True, # Python >= 3.7 only
                text = True # Python >= 3.7 only
            )
            return

    print_choice(devices)


if __name__ == "__main__":
    main()
