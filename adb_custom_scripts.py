#!/usr/bin/env python3
import subprocess
import os
import shlex
from datetime import datetime
from rich.console import Console
from texttable import Texttable


table = Texttable()
console = Console()


USER_HOME = os.environ.get("HOME")
current_directory = os.getcwd()


def format_Date(file_name):
    unformatted_time = os.path.getctime(file_name)
    return datetime.fromtimestamp(unformatted_time)


def is_success(task_name):
    console.print(f"✅ {task_name.strip()}", style="bold green")


def is_loading(task_name):
    console.print(f"🔧 {task_name.strip()}", style="bold blue")


def is_error(task_name):
    console.print(f"❗️ {task_name.strip()}", style="bold red")


def is_normalOutput(task_name):
    console.print(f"{task_name.strip()}", style="bold yellow")


def divider():
    console.print("---------------------------------", style="bold white")


def spacer():
    print("\n")


def adb_device_check():
    device_check_command = shlex.split("adb devices -l")
    devices_check_process = subprocess.run(device_check_command, capture_output=True, text=True)

    if devices_check_process.returncode != 0:
        is_error(devices_check_process.stderr)
    else:
        is_success(devices_check_process.stdout)


def unlock_device() -> None:
    screen_state_check_command = shlex.split("adb shell dumpsys deviceidle | grep 'mScreenOn='")
    unlock_command = shlex.split("adb shell input keyevent 26")
    # swipe_command = "adb shell input touchscreen swipe 300 300 500 1000 100"

    try:
        screen_state_process = subprocess.run(screen_state_check_command, capture_output=True, text=True, check=True)
        screen_state = screen_state_process.stdout.strip()
        match screen_state:
            case "mScreenOn=false":
                try:
                    subprocess.run(unlock_command, capture_output=True, text=True, check=True)
                    is_success("device unlocked")
                    divider()
                except subprocess.CalledProcessError as e:
                    is_error(e.stderr)
                    divider()
            case "mScreenOn=true":
                is_normalOutput("device already unlocked")
                divider()
            case _:
                is_error("cannot get screen state")
                divider()
    except subprocess.CalledProcessError as e:
        is_error(e.stderr)
        divider()


def toggle_hotspot():
    # # hexadecimal hotspot toggle button coordinates
    #  ABS_MT_POSITION_X  = 00000d21
    #  ABS_MT_POSITION_Y  =  000002bd

    # # decimal coordinates
    # position_x = 3361
    # position_y = 701

    toggle_command = "adb shell input tap 3361 701"
    subprocess.run(toggle_command, capture_output=True, text=True, shell=True)
    # if toggle_process.returncode != 0:
    #     is_error(toggle_process.stderr)
    # else:
    #     is_success(toggle_process.stdout)

    open_hotspot_settings_command = "adb shell am start -S com.android.settings/.TetherSettings && sleep 2"
    open_hotspot_settings_process = subprocess.run(
        open_hotspot_settings_command, capture_output=True, text=True, shell=True
    )
    if open_hotspot_settings_process.returncode == 0:
        is_normalOutput(open_hotspot_settings_process.stdout)
        subprocess.run(toggle_command, capture_output=True, text=True, shell=True)

    else:
        is_error(open_hotspot_settings_process.stderr)


def adb_get_device_ip():
    interface_command = (
        "adb shell ifconfig rmnet_data0 | grep --line-buffered -E -m1 -o '10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'"
    )
    interface_process = subprocess.run(interface_command, capture_output=True, text=True, shell=True)
    if interface_process.returncode != 0:
        is_error(interface_process.stderr)
    else:
        is_loading("fetching device Interface data and filtering IP address")
        is_success("ip address found : " + interface_process.stdout)
        divider()
        return interface_process.stdout


def switch_to_wireless_debugging():
    switch_command = "adb tcpip 5555 && sleep 2 && ipAddress=\"$(adb shell ifconfig rmnet_data0 | grep --line-buffered -E -m1 -o '10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')\" && adb connect \"$ipAddress\":5555"
    try:
        switch_process = subprocess.run(
            switch_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True, check=True, shell=True
        )
        is_success(switch_process.stdout)
    except subprocess.CalledProcessError as e:
        is_error(e.stdout)
        print(e.stdout == "adb: no devices/emulators found")


def mirror_display() -> None:
    try:
        mirror_display_command = "scrcpy"
        mirror_display_process = subprocess.run(
            mirror_display_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True, shell=True
        )
        output: str = mirror_display_process.stdout.strip()
        print(output)
    except subprocess.CalledProcessError as e:
        is_error(e.stdout)


def process_selector():
    try:
        console.print("Select script ID from table", style="bold italic red")

        table.header(["id", "script"])
        table.add_row([1, "Unlock Device"])
        table.add_row([2, "Check Connected Devices"])
        table.add_row([3, "Get Device IP"])
        table.add_row([4, "Switch to wireless debugging"])
        table.add_row([5, "Cast device screen to pc"])

        console.print(table.draw(), style="bold green")
        divider()
        options = int(input("select script: ").strip())
        divider()
        match options:
            case 1:
                unlock_device()
            case 2:
                adb_device_check()
            case 3:
                adb_get_device_ip()
            case 4:
                switch_to_wireless_debugging()
            case 5:
                mirror_display()
            case _:
                is_error("invalid option")
    except KeyboardInterrupt:
        print("\n")
        divider()
        is_error("Remain Lazy or i'll come get you")
        divider()
        print("\n")


def header(title: str) -> None:
    subprocess.run("clear")
    print("\n")
    command = 'toilet --gay -f future "shy.X" | boxes -d parchment '
    ret = subprocess.run(command, capture_output=True, shell=True)
    print(ret.stdout.decode())
    console.print(f"# - {title}", style="bold red ")
    console.print("#comrade let us be lazy", style="bold italic")
    divider()
    print("⚡️[command center] : " + os.getcwd())
    divider()


def __main__():
    header("PERILS OF A BLIND PHONE SCRIPT")
    process_selector()


__main__()
