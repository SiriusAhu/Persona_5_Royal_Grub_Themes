import os
import shutil

characters = {
    0 : "crow",
    1 : "fox",
    2 : "joker",
    3 : "mona",
    4 : "navi",
    5 : "noar",
    6 : "panther",
    7 : "queen",
    8 : "skull",
    9 : "violet"
}

# get the path of this script
PWD = os.path.dirname(os.path.realpath(__file__))
PATH_THEME_SOURCE = os.path.join(PWD, "release")
PATH_THEME_TARGET = "/boot/grub/themes"

def check_input(inpt):
    # Enter, Y, y: Yes | N, n: No | Others: Invalid
    if inpt in ["Y", "y", ""]:
        return True
    elif inpt in ["N", "n"]:
        return False
    else:
        print("Invalid input.")
        print("Aborting...")
        exit(1)

# 0. Warining: "sudo" is required (shell: red background)
os.system("clear")
print("- Note: \033[41msudo is required to run this script.\033[0m")
print("        Please restart this script \033[41mif you are not using sudo.\033[0m")
input("Press Enter to continue...")
print("")
os.system("clear")

# 1. Choose theme
print("Please choose a theme:")
for k, v in characters.items():
    if k % 2 == 0:
        print(f"\t\033[44m{k}. {v}\033[0m")
    else:
        print(f"\t\033[41m{k}. {v}\033[0m")
theme = input("You choose (input 0-9): ")
if theme not in [str(i) for i in range(len(characters))]:
    print("Invalid input.")
    print("Aborting...")
    exit(1)
os.system("clear")


# 2. Copy theme to /boot/grub/themes
print("You chose \033[41m" + characters[int(theme)] + "\033[0m.")
print("Do you want this script to \033[41mcopy the theme files\033[0m to for you?")
print("- This will overwrite the existing theme with the same name.")
print("[Y]/N: ", end="")

if check_input(input()):
    path_theme_source = os.path.join(PATH_THEME_SOURCE, characters[int(theme)])
    print(f"Copying theme {characters[int(theme)]} to \033[41m{PATH_THEME_TARGET}\033[0m...")
    # overwrite if exists
    shutil.copytree(path_theme_source, PATH_THEME_TARGET + "/" + characters[int(theme)], dirs_exist_ok=True)
    print("Done!")

print("Press Enter to continue...")
os.system("clear")

# 3. Edit /etc/default/grub
print("Do you want this script to edit \033[41m/etc/default/grub\033[0m for you?")
print("- Your current \033[41m/etc/default/grub\033[0m will be overwritten.")
print(f"  But we'll make a backup at {PWD}/grub.bak (same path as the script) \033[41mno matter what you choose.")
print("- This \033[41mbackup won't be overwritten after being created\033[0m.")
print("[Y]/N: ", end="")

# backup
shutil.copyfile("/etc/default/grub", os.path.join(PWD, "grub.bak"))

if check_input(input()):
    print("Editing \033[41m/etc/default/grub\033[0m...")
    with open("/etc/default/grub", "r") as f:
        lines = f.readlines()
    for i in range(len(lines)):
        if "GRUB_THEME" in lines[i]:
            the_lines = lines[i].split("=")
            the_lines[1] = "\"" + PATH_THEME_TARGET + "/" + characters[int(theme)] + "/theme.txt\"\n"
            lines[i] = the_lines[0] + "=" + the_lines[1]
            break
    with open("/etc/default/grub", "w") as f:
        f.writelines(lines)
    print("Done!")

print("Press Enter to continue...")
os.system("clear")

# 4. After all
# Hint: update grub
print("Congratulations! Everything is done.")
print("Please run")
print("\t\033[41msudo update-grub\033[0m")
print("or")
print("\t\033[41msudo grub-mkconfig -o /boot/grub/grub.cfg\033[0m")
print("to update grub.")
print()
print("Hope you enjoy it! :)")
