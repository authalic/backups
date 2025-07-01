# %% [markdown]
# # Backup Portal Item JSON files
# <p>Developed: 30 October, 2024<br>
# Justin Johnson, justinpjohnson@utah.gov</p>
#
# ## What this does
#
# <p>An issue was reported by users of the Projects portal at UDOT https://projects.udot.utah.gov/portal
# <p>Users were seeing edits that they made to web maps, forms, popups, and other configurations revert or entirely disappear after saving.
# <p>This script copies the Item json configuration files from the arcgisporta\content\items folder to use as either a restore or to compare changes happening to the files from day to day.

# %%
import os
import shutil
from datetime import datetime

# %%
# input folder and output locations on the Projects Portal machine: srgwcongisporta
# creates a backup folder using the current date

items_path = r'D:\arcgisportal\content\items'
backup_folder = r"D:\Backups_portal_items\items_" + datetime.strftime(datetime.today(), r'%Y_%m_%d_%H%M')


# %%
# check if the current output directory already exists.  If not, create it.
# running this script on the same date will overwrite the previous information in the folder
# if it is necessary to do multiple backups on the same day, add the time string to the folder name

if not os.path.isdir(backup_folder):
    os.mkdir(backup_folder)

# %%
# copy the JSON files from each subfolder to a backup folder with today's date

def copy_json_files(items_path):
    for root, dirs, files in os.walk(items_path):
        for file in files:
            # json files are named with 32-character UUID strings

            if len(file) == 32:
                # check if the filename is a valid UUID (string of 32 hexadecimal digits)

                try:
                    t = int(file, 16)
                    shutil.copy2(os.path.join(root,file), backup_folder)
                except ValueError:
                    pass
    print('  done\n')


# %%
print("Copying JSON files from:", items_path)

copy_json_files(items_path)

print("Copies saved in:", backup_folder)