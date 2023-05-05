#!/usr/bin/env python3
import subprocess
import os
from datetime import datetime
from rich.console import Console

console = Console()
# command center
USER_HOME = os.environ.get("HOME")
# scripts home directory
current_directory = os.getcwd()


def list_dir_files(directory):
    res = []
    for path in os.listdir(directory):
        if os.path.isfile(os.path.join(current_directory, path)):
            res.append(path)
    print("Directory files : {}".format(res))


def format_Date(file_name):
    unformatted_time = os.path.getctime(file_name)
    return datetime.fromtimestamp(unformatted_time)


def open_script_editor(folder_name):
    open_script_editor_answer = str(input("open with text editor ? [y/n] : "))
    if open_script_editor_answer == "y":
        p1 = subprocess.run(["code", folder_name], capture_output=True, text=True)
        print(p1.stderr)
    else:
        list_dir_files(current_directory)


def is_success(task_name):
    console.print(f"{task_name} ✅ ", style="bold green")


def is_loading(task_name):
    console.print(f"{task_name} 🔧 ", style="bold yellow")


def is_error(task_name):
    console.print(f"{task_name}  ❗️", style="bold red")


def divider():
    console.print("---------------------------------", style="bold white")


def install_deps(path):
    is_loading("installing node modules...")
    sp2 = subprocess.run(["npm", "install"], capture_output=True, text=True)
    if sp2.returncode != 0:
        is_error("error : " + sp2.stderr)
    else:
        print(sp2.stdout)
        divider()
        open_script_editor(path)


def format_directory(src, dest, svr_name):
    if os.path.exists(src):
        os.rename(src, dest)
        is_success("project renamed")
        os.chdir(dest)
        rm_dot_git_command = "rm -rf .git && ls"
        sp1 = subprocess.run(rm_dot_git_command, capture_output=True, shell=True)
        if sp1.returncode != 0:
            print(sp1.stderr.decode())
        else:
            is_success(".git removed")
            divider()
            print("Server Name : " + svr_name)
            divider()
            print("Files : ")
            print(sp1.stdout.decode())
            divider()
            print("createdAt ⏳: " + str(format_Date(dest)))
            divider()
            install_deps(dest)
    else:
        print("error: could not rename directory")


subprocess.run("clear")
print("\n")
command = 'toilet --gay -f future "shyXperience" | boxes -d parchment '
ret = subprocess.run(command, capture_output=True, shell=True)
print(ret.stdout.decode())
console.print("# -  NODE SERVER INIT SCRIPT", style="bold red ")
console.print("#comrade let us be lazy", style="bold italic")
print("---------------------------------")
print("⚡️[command center] : " + os.getcwd())
server_name_answer = str(input("enter server name 💻 : "))
project_directory = str(input("enter project directory : "))
if server_name_answer != "":
    os.chdir(project_directory)
    print("⚡️[project Directory] : " + os.getcwd())
    git_clone_template = subprocess.run(
        ["git", "clone", "https://github.com/AdamuAbba/node_server_template.git"], capture_output=True, text=True
    )
    print(git_clone_template.stderr)
    if git_clone_template.returncode == 0:
        is_success("template clone success")
        template_directory = os.path.join(project_directory, "node_server_template")
        server_name_directory = os.path.join(project_directory, server_name_answer)
        format_directory(template_directory, server_name_directory, server_name_answer)
else:
    print("error: server name cannot be blank")
