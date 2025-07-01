# %% [markdown]
# # Backup Portal Item JSON files
# Justin Johnson, justinpjohnson@utah.gov
#
# - Developed: 30 October, 2024
# - Updated: 27 June, 2025
#
# ## What this does
#
# An issue was reported by users of the Projects portal at UDOT https://projects.udot.utah.gov/portal
#
# Items in the Portal were losing changes and edits
# - Users were seeing edits that they made to web maps, forms, popups, and other configurations revert or entirely disappear after saving.
#
# This script
# - copies the Item json configuration files from the arcgisporta\content\items folder to use as either a restore or to compare changes happening to the files from day to day
#
# ### Update: 27 June, 2025
#
# Added code to:
# - zip each daily backup folder
# - specify the number of daily backups to retain
#

# %%
import os
import shutil
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime

# %%
# set the archive retention limit
# this is the maximum number of zip files that will be retained
# Note: this will always be the number of newest files, not necessarily the number of days that are retained

retention_limit = 10

# %%
# Portal folder location storing JSON configuration file for each Item
# these are the files getting backed up by this script

items_path = Path(r'D:\arcgisportal\content\items')

# %%
# Create names for timestamped folder and zip archive

# Archive folder location
# temporarly folder containing copies of the JSON files are stored here
# this folder is zipped, then deleted

arch_path = Path(r"D:\Backups_portal_items")
arch_name = Path("items_" + datetime.strftime(datetime.today(), r'%Y_%m_%d_%H%M'))
# ex: items_2025_06_27_1447

# new folder storing the copied JSON files (unzipped)
arch_folder = Path(arch_path, arch_name)

# filename of archived folder (zipped)
arch_zip = Path(arch_path, arch_name).with_suffix(".zip")

# %%
# check if the current output directory already exists in the backup folder location.  If not, create it.

if not arch_folder.is_dir():
    Path.mkdir(arch_folder)

# %%
# iterate through the current folders in the Portal Items folder
# each folder is an Item ID for an Item in the Portal
# some folders may be empty, others may have subfolders

# copy the JSON files from each subfolder to the backup folder named with today's date and time

def copy_json_files(items_path):

    for root, dirs, files in os.walk(items_path):

        for file in files:  # returns filename string

            # json files for Portal Items are named with 32-character UUID strings
            # we don't need to copy any other files (.xml, \esriinfo folder, or thumbnails, etc)

            # check if the filename is a valid UUID (string of 32 hexadecimal digits)
            if len(file) == 32:
                try:
                    # attempt to convert the filename string to an integer
                    test_int = int(file, 16)

                    # copy the file
                    shutil.copy2(os.path.join(root,file), arch_folder)

                except ValueError:
                    # the file name is not a valid UUID, which means it's not the Item json we want to copy
                    pass

    print('  done\n')

# %%
# copy the files...

copy_json_files(items_path)

# %% [markdown]
# At this point:
# - the current Portal Item JSON files have been copied from `items_path` to a backup folder `arch_folder`
#
# Next:
# - zip and delete the folder of JSON files
# - delete the oldest zip files to maintain the file retention limit setting
#
# Note: Zip archive file size seems to be about 40% of the unzipped folder size

# %% [markdown]
# Zip the folder, then delete it

# %%
# create the zip file and add files to it
with ZipFile(arch_zip, mode='w', compression=ZIP_DEFLATED, compresslevel=9) as outzip:

    for itemfile in Path(arch_folder).iterdir():

        # write the Item JSON file to the zip archive
        outzip.write(itemfile)

        # delete the original file
        itemfile.unlink()

# remove the empty archive folder
arch_folder.rmdir()

# %% [markdown]
# Remove the oldest archive(s) to maintain the retention limit

# %%
# get a list of all zip files in the archive folder

filelist = list(arch_path.glob('*.zip'))

# Sort the filenames in ascending order
# this is also chronological order, since filenames are based on date and time of archive
filelist.sort()

if len(filelist) > retention_limit:

    # slice off a list of files to drop from the FRONT of the sorted list
    # when sorted alphabetically, the oldest files are first

    dropfiles = filelist[:(len(filelist) - retention_limit)]

    for file in dropfiles:
        Path.unlink(file)
