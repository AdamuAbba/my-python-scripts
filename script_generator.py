#!/usr/bin/env python3
import subprocess
import os
from datetime import datetime

# command center
USER_HOME = os.environ.get("HOME")
documents_file_path = os.chdir(USER_HOME + "/Documents/Lazy me scripts")
# scripts home directory
current_directory = os.getcwd()


def list_dir_files(directory):
    res = []
    for path in os.listdir(directory):
        if os.path.isfile(os.path.join(current_directory, path)):
            res.append(path)
    print("Available scripts 📑: {}".format(res))


def format_Date(file_name):
    unformatted_time = os.path.getctime(file_name)
    return datetime.fromtimestamp(unformatted_time)


def open_script_editor(file_name):
    open_script_editor_answer = str(input("open text editor ? [y/n] : "))
    if open_script_editor_answer == "y":
        p1 = subprocess.run(["code", file_name], capture_output=True, text=True)
        print(p1.stderr)
    else:
        list_dir_files(current_directory)


print("\n")
print("shyXperience\ncomrade let us be lazy")
print("---------------------------------")
print("⚡️[command center] : " + os.getcwd())
create_script_answer = str(input("Do you want to create a new script ? [y/n] :"))
if create_script_answer == "y":
    script_name = str(input("Enter script name : "))
    new_file_path = current_directory + "/" + script_name + ".py"
    script_name_with_ext = script_name + ".py"
    if os.path.exists(new_file_path):
        print("{script_name} already exists \n".format(script_name=script_name))
    else:
        with open(new_file_path, "w") as file:
            file.write("#!/usr/bin/env python3\n")
            print("script created 🎊")
            print("---------------------------------")
            print("Name : " + script_name)
            print("createdAt ⏳: " + str(format_Date(file.name)))
            print("---------------------------------")
            open_script_editor(script_name_with_ext)

else:
    print("C'mon be lazy for once will ya ?")
    print("---------------------------------")
