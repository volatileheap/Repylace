from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import os
import uuid
import random
import shutil
from sys import platform

# <editor-fold desc="Image Data">
searchPhotoData = b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAMQSURBVFhHzZVNaBNBFMdfsh+JetNaaD159iDYg1ixIB4qWCviwYNCJUHB1g8sSCIN4qFiKjQWLXoxwRxEFCtUA3qreBCE1ot49qTFWm9+5GM/fG8ys92vbFaaRH+w7OzMzrz/vPfmTQQ4pmnyVuuIRKzlGX42HAJoQhghMzfTpizLEFNVkGSJJkPibMZpjWMXsW4Bt6ZSbJD+i0ajIKNxKSqxNj1EctQrRIhYlwBhXHApNWXNnZ2eMMkTkiSxNU6PXfUV0VRAI+zG7YbdzOYmMDQKCon6ivCj7rcAwhonzo1fj2hajW0mf3fSmke7F2Fw4xGwVNhi2h/e3dS4gETous6/muMQYDdIvP6atELjHgtC13QwDAPy99a80AhrV4v5zdbPu3Z3s3f26SBLrAO9D9j337D44zwoigI7YzneA9CX+O7xoicEwjjx89dvqFSrjr6w6IYO7lD4edHjAbux1P09sCEeh2snF3hPeO68PMpqw9jgHPt+/26FvQm7JwJPAWWuhrvIzh3kPeGYKQ2zHNA0jfc4N2b3RKCAbPItLqJDrVrjPeGh5L14aJ5/1fELZcMQLH9aZe/bC0ew5MqwaWMcRvoesr4gHn9M8BbA8R0F3qrTs72LvSkcIgy+HhDGiQv753E3BpQrVSguneC9/jz6cMo6tm7jhH1dAVNBk0RcerrXNAnFRKa4D3MiCqoig6IqkD72io9gqDBHtBrGG1dT8ejRJTU+XOKjdezGl1cMywMOAY2MC64U9uK/wG9B/Jdm47fOEk5HgQCxmIonJ4Y1QA4U0Tv0zSngS2lr3XeIn3E76Xw/nnGDbLMF6PKhhCXIUwpeSPG4GijCIeDzi67QxsOQKQ6gCNlXhBCw7fBqhDbuSMJWGCcmR95ADWtAuVyFGuZG7vkQH3FCdcb3FLSCsCLaJoAIEiGOa1sFEG4RVCsEnhxoF0EiOiKAcIuYvnGZxaBjAggSQTdkBcs63bJERwUQowPPWDVNZXKsBnVcAHGm/wlv/SMBdjyl2IJGvL0tQ9wFjT3QRuP/EQB/AIbNiCWYySxlAAAAAElFTkSuQmCC"
iconPhotoData = b"iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAQAAABKfvVzAAAAAmJLR0QA/4ePzL8AAAEUSURBVDjLvdOxLsNRFMfxz8Zo6kCaLoiYDNI+gIm3MDJ6Ch7A0piJFDF36oLBQtp0MOrAQKLoIGlzDK3qv/+mjUHvGW5y7u97zj3nnss0V4g/+acEFMCWhoZNUBgN7MioC20HZjWE8GjWvrZQl7U3KN8VqrL94+jZT4h1DWH7F8ioCu9uPfTFXXtRUfUlVMwN5si4H5Im7cRMuo4Nlzop6YdDK2lxxt2IuL/4cTJDt4ZnR25SyJkLn8M1dLs0ryh0tPrylo5QtDbcJXYsKQst14kMV1pC2WryHaAmPMl7TwBv8p6E2ujByPX2QSM3ejh+nGnAeKA5dKWJwHkCKE0Glr305a8WJwMsONXUVOrJx3yh/1jfnBrl6+/1hx0AAAAASUVORK5CYII="
# </editor-fold>

def browse_button():
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)

def scan_tree(path):
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield entry
            yield from scan_tree(entry.path.replace("\\","/"))
        else:
            yield entry

def check_folder_update():
    global replaceDirectoryNames
    replaceDirectoryNames = not replaceDirectoryNames

def check_file_update():
    global replaceFileNames
    replaceFileNames = not replaceFileNames

def replace_button():
    global replaceDirectoryNames
    global result_text
    search = searchForText.get()
    include = includeText.get()
    exclude = excludeText.get()
    replace = replaceText.get()

    if len(search) == 0:
        return

    if folder_path.get() == "":
        return

    occurrence = 0

    count = 0
    for _ in scan_tree(folder_path.get().replace("\\","/")):
        if not _.is_dir():
            count += 1

    progressBar["maximum"] = count

    renamePostIteration = []

    for entry in scan_tree(folder_path.get().replace("\\","/")):
        if entry.is_dir():
            directory = entry.path.replace("\\","/")
            if replaceDirectoryNames:
                if search in entry.name:
                    renamePostIteration.append(directory)
                    occurrence += 1
        else:
            predicted_file_path = entry.path.replace("\\","/")
            final_file_path = ""
            if replaceFileNames:
                if exclude != "":
                    exclusion_free = predicted_file_path.replace(exclude, "")
                    if search in exclusion_free:
                        temp_list = []
                        temp_dirname = os.path.dirname(predicted_file_path)
                        dir_split = os.path.basename(predicted_file_path).split(exclude)
                        for split in dir_split:
                            temp_list.append(split.replace(search, replace))
                        replacement = exclude.join(temp_list)
                        final_file_path = os.path.join(temp_dirname, replacement).replace("\\","/")
                else:
                    temp_dirname = os.path.dirname(predicted_file_path)
                    final_file_path = os.path.join(temp_dirname, os.path.basename(predicted_file_path).replace(search, replace)).replace("\\","/")
            else:
                final_file_path = predicted_file_path.replace("\\","/")
            temp_file_path = os.path.join(predicted_file_path[:-len(entry.name) - 1], str(uuid.uuid1()).replace("-", "")).replace("\\","/")
            try:
                with open(temp_file_path, "x") as _:
                    pass
            except FileExistsError:
                with open(str(os.path.join(predicted_file_path[:-len(entry.name) - 1], str(str(random.randint())))), "x") as _:
                    pass
            temp_file = open(temp_file_path, "a")
            found = False
            with open(predicted_file_path) as f:
                try:
                    for line in f:
                        try:
                            if search in line:
                                found = True
                                if exclude != "":
                                    exclusion_free = line.replace(exclude, "")
                                    if search in exclusion_free:
                                        occurrence += 1
                                        if include != "":
                                            temp_list = []
                                            line_split = line.split(exclude)
                                            for split in line_split:
                                                temp_list.append(split.replace(include, replace))
                                            replacement = exclude.join(temp_list)
                                            temp_file.write(replacement)
                                        else:
                                            temp_list = []
                                            line_split = line.split(exclude)
                                            for split in line_split:
                                                temp_list.append(split.replace(search, replace))
                                            replacement = exclude.join(temp_list)
                                            temp_file.write(replacement)
                                    else:
                                        temp_file.write(line)
                                else:
                                    occurrence += 1
                                    if include != "":
                                        replacement = line.replace(include, replace)
                                        temp_file.write(replacement)
                                    else:
                                        replacement = line.replace(search, replace)
                                        temp_file.write(replacement)
                            else:
                                temp_file.write(line)
                        except UnicodeDecodeError:
                            temp_file.write(line)
                except UnicodeDecodeError:
                    pass
            temp_file.close()
            if found:
                os.unlink(predicted_file_path)
                os.rename(temp_file_path.replace("\\","/"), final_file_path.replace("\\","/"))
            else:
                os.unlink(temp_file_path)
                if predicted_file_path.replace("\\","/") != final_file_path.replace("\\","/"):
                    os.rename(predicted_file_path.replace("\\","/"), final_file_path.replace("\\","/"))
        progressBar["value"] += 1
        progressBar.update()
    futureIndex = 0
    while futureIndex < len(renamePostIteration):
        directory = renamePostIteration[futureIndex].replace("\\","/")
        try:
            # noinspection DuplicatedCode
            if exclude != "":
                exclusion_free = directory.replace(exclude, "")
                # noinspection DuplicatedCode
                if search in exclusion_free:
                    temp_list = []
                    dir_split = directory.split(exclude)
                    for split in dir_split:
                        temp_list.append(split.replace(search, replace))
                    replacement = exclude.join(temp_list)
                    shutil.move(directory, os.path.join(os.path.dirname(directory), replacement))
                    index = 0
                    for futureDirectory in renamePostIteration:
                        if futureIndex > index:
                            index += 1
                            pass
                        if directory in futureDirectory:
                            renamePostIteration[index] = futureDirectory.replace(directory, os.path.join(os.path.dirname(directory), replacement))
                            index += 1
            else:
                replacement = os.path.basename(directory).replace(search, replace)
                shutil.move(directory, os.path.join(os.path.dirname(directory), replacement))
                index = 0
                for futureDirectory in renamePostIteration:
                    if futureIndex > index:
                        index += 1
                        pass
                    if directory in futureDirectory:
                        renamePostIteration[index] = futureDirectory.replace(directory, os.path.join(os.path.dirname(directory), replacement))
                        index += 1
        except PermissionError:
            pass
        futureIndex += 1
    progressBar["value"] = 0
    if occurrence == 0:
        result_text.set("Found no occurrences")
    elif occurrence == 1:
        result_text.set("Replaced 1 occurrence")
    else:
        result_text.set("Replaced " + str(occurrence) + " occurrences")

window = Tk()
window.resizable(False, False)

folder_path = StringVar()
result_text = StringVar()
result_text.set("")

window.title("Repylace")
icon = PhotoImage(data=iconPhotoData)
window.tk.call("wm", "iconphoto", window._w, icon)

directoryInfoText = Label(window, text="In directory")
directoryInfoText.grid(column=0, row=0)

directoryText = Entry(window, width=60, textvariable=folder_path, state="disabled")
directoryText.grid(column=1, row=0, padx=5)

replaceDirectoryNames = False
replaceFileNames = False

searchPhoto = PhotoImage(data=searchPhotoData)

searchButton = Button(window, image=searchPhoto, command=browse_button)
searchButton.grid(column=2, row=0)

# <editor-fold desc="search">
searchForInfoText = Label(window, text="search for")
searchForInfoText.grid(column=0,row=1)

searchForText = Entry(window, width=30)
searchForText.grid(column=1, row=1, padx=5)
# </editor-fold>

# <editor-fold desc="include">
includeInfoText = Label(window, text="only including when it's as")
includeInfoText.grid(column=0, row=2)

includeText = Entry(window, width=30)
includeText.grid(column=1, row=2)
# </editor-fold>

# <editor-fold desc="exclude">
excludeInfoText = Label(window, text="excluding when it's as")
excludeInfoText.grid(column=0, row=3)

excludeText = Entry(window, width=30)
excludeText.grid(column=1, row=3)
# </editor-fold>

# <editor-fold desc="replace">
replaceInfoText = Label(window, text="and replace with")
replaceInfoText.grid(column=0, row=4)

replaceText = Entry(window, width=30)
replaceText.grid(column=1, row=4)
# </editor-fold>

# <editor-fold desc="replaceDirectory">
replaceDirectory = Checkbutton(window, text="including directory names", command=check_folder_update)
replaceDirectory.grid(column=0, row=5)
replaceDirectory.invoke()
replaceDirectory.invoke()
# </editor-fold>

# <editor-fold desc="replaceFiles">
replaceFiles = Checkbutton(window, text="including file names", command=check_file_update)
replaceFiles.grid(column=0, row=6)
replaceFiles.invoke()
replaceFiles.invoke()
# </editor-fold>

style = ttk.Style()
system = platform
if system == "win32":
    if "winnative" in style.theme_names():
        style.theme_use("winnative")
    else:
        style.theme_use("default")
elif system == "darwin":
    if "aqua" in style.theme_names():
        style.theme_use("aqua")
    else:
        style.theme_use("default")
else:
    style.theme_use("default")

resultText = Label(window, textvariable=result_text)
resultText.grid(column=0, row=7)

progressBar = ttk.Progressbar(window, length=200, mode="determinate")
progressBar.grid(column=1, row=7)

replaceButton = Button(window, text="Replace", command=replace_button)
replaceButton.grid(column=1, row=8)

window.mainloop()