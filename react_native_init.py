#!/usr/bin/env python3
from base64 import decode
import subprocess
import os
from datetime import datetime
from sys import stderr
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
    is_loading("installing dependencies...")
    sp2 = subprocess.run(["yarn"], capture_output=True, shell=True)
    if sp2.returncode != 0:
        is_error("error : " + sp2.stderr.decode())
    else:
        print(sp2.stdout.decode())
        is_success("dependencies installed")
        divider()
        open_script_editor(path)


def configureGit():
    is_loading("creating git repo & configuring origin")
    repo_configure_command = (
        "gh repo create "
        + app_name_answer
        + " --"
        + app_privacy_answer
        + " -d '"
        + app_description_answer
        + "' && git init && git remote add origin https://github.com/AdamuAbba/"
        + app_name_answer
        + ".git && git remote -v"
    )
    process = subprocess.run(repo_configure_command, capture_output=True, shell=True, check=True)
    if process.returncode != 0:
        print(process.stderr.decode())
    else:
        print(process.stdout.decode())
        divider()
        is_success("repository configured successfully")


def format_directory(src, dest, app_name):
    if os.path.exists(src):
        divider()
        is_loading("renaming project")
        os.rename(src, dest)
        is_success("project renamed")
        divider()
        os.chdir(dest)
        rm_dot_git_command = "rm -rf .git"
        is_loading("deleting .git file")
        sp1 = subprocess.run(rm_dot_git_command, capture_output=True, shell=True)
        if sp1.returncode != 0:
            print(sp1.stderr.decode())
        else:
            print(sp1.stdout.decode())
            is_success(".git removed")
            divider()
            configureGit()
            divider()
            print("app name : " + app_name)
            divider()
            is_loading("Project files : ")
            print("")
            is_success(sp1.stdout.decode())
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
console.print("# -  REACT NATIVE APP BOOTSTRAP SCRIPT", style="bold red ")
console.print("#comrade let us be lazy", style="bold italic")
print("---------------------------------")
print("⚡️[command center] : " + os.getcwd())
app_name_answer = str(input("enter app name 📱 : "))
project_directory = os.path.join(USER_HOME, "documents")
if app_name_answer != "":
    app_description_answer = str(input("app description 💬 : "))
    app_privacy_answer = str(input("app privacy status 🙊 : "))
    is_loading("CD into documents directory")
    os.chdir(project_directory)
    divider()
    print("⚡️[project Directory] : " + os.getcwd())
    divider()
    is_loading("cloning template from Github")
    git_clone_template = subprocess.run(
        [
            "git",
            "clone",
            "--verbose",
            "--progress",
            "https://github.com/AdamuAbba/react_native_typescript_template.git",
        ],
        capture_output=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    if git_clone_template.returncode == 0:
        print(git_clone_template.stdout)
        is_success("template clone success")
        template_directory = os.path.join(project_directory, "react_native_typescript_template")
        app_name_directory = os.path.join(project_directory, app_name_answer)
        format_directory(template_directory, app_name_directory, app_name_answer)
    elif git_clone_template.returncode != 0:
        print(git_clone_template.stderr)
else:
    print("")
    divider()
    is_error("Alaye app name cannot be blank jarey 😒,\nwho be this guy,na your type dey like problem")
    divider()
    print("")
