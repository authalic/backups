# %% [markdown]
# # Backup Portal Item JSON files
# Justin Johnson, justinpjohnson@utah.gov
#
# - Developed: 30 October, 2024
# - Updated: June/July, 2025
#
# ## What this does
#
# An issue was reported by users of the Projects portal at UDOT https://projects.udot.utah.gov/portal
#
# Items in the Portal were losing changes and edits
# - Users were seeing edits that they made to web maps, forms, popups, and other configurations revert or entirely disappear after saving.
#
# This script
# - copies the Item json configuration files from the arcgisportal\content\items folder to use as either a restore or to compare changes happening to the files from day to day
# - each daily backup folder is zipped
# - a retention limit is set to maintain the most recent number of daily backups
#
# ### Update: 27 June, 2025
#
# Added code to:
# - zip each daily backup folder
# - specify the number of daily backups to retain
#
# ### Update: 7 July, 2025
#
# - added logging functionality to store a log of each scheduled run
# - added error checks for file paths
#

# %%
import os
import sys
import shutil
import logging

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime

# %% [markdown]
# ## Required User Inputs

# %%
# set the archive retention limit
# this is the maximum number of zip files that will be retained
# Note: this will always be the number of newest files, not necessarily the number of days that are retained

retention_limit = 15


# %%
# set the logging level
# this is the minimum logging level that will be retained in all log files and output streams

# INFO
log_level = logging.INFO

# DEBUG
# log_level = logging.DEBUG

# %%
# Portal folder location storing JSON configuration file for each Item
# these are the files getting backed up by this script

items_path = Path(r'D:\arcgisportal\content\items')

if not items_path.is_dir():
    print("Path to Items folder is not valid")
    sys.exit(1)

# %%
# Create names for timestamped folder and zip archive

# Archive folder location
# temporarly folder containing copies of the JSON files are stored here
# this folder is zipped, then deleted

arch_path = Path(r"D:\Backups_portal_items")

if not arch_path.is_dir():
    print("Path to Archive storage folder is not valid")
    sys.exit(1)


arch_name = Path("items_" + datetime.strftime(datetime.today(), r'%Y_%m_%d_%H%M'))
# ex: items_2025_06_27_1447

# new folder storing the copied JSON files (unzipped)
arch_folder = Path(arch_path, arch_name)

# filename of archived folder (zipped)
arch_zip = Path(arch_path, arch_name).with_suffix(".zip")


# %% [markdown]
# ## Log File setup

# %%
# Path to log file
logfile = Path(arch_path, "portal_backup.log")

if not logfile.exists():
    try:
        logfile.touch()  # not really necessary. Logger will create this if it doesn't exist
    except FileNotFoundError:
        print("Unable to create new log file. Path may be invalid.")
        sys.exit(1)


# %% [markdown]
# ## Log Handler setup
#
# There are two Handler objects created below. One will send log messages to the Log file. The other will display log messages to `stderr`
# - each handler has its own logging level defined, but the `log_level` set above is the absolute minimum for all handlers
#   - i.e. to send `DEBUG` logs to the log file or `stderr`, the `log_level` must be changed to `DEBUG` above, and in the handlers below
#

# %%
# create Logger object
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# Set the format of the Log messages
# ex:  Tue 2025-07-08 10:24:07 - INFO     creating ZIP archive: C:\test\Backups_portal_items\items_2025_07_08_1014.zip

# Formatter
fmt_str = "{asctime} - {levelname:<8} {message}"
fmt_date = "%a %Y-%m-%d %H:%M:%S"
fmt_style = "{"

log_formatter = logging.Formatter(fmt=fmt_str, datefmt=fmt_date, style=fmt_style)


# configure the Logger with a File Handler and output Stream Handler

# File Handler (sends log message to log file)
log_handler_file = logging.FileHandler(logfile, mode='a', encoding='UTF-8')
log_handler_file.setFormatter(log_formatter)


# Stream Handler (sends log messages to sys.stderr)
log_handler_stream = logging.StreamHandler()
log_handler_stream.setLevel(logging.DEBUG)
log_handler_stream.setFormatter(log_formatter)


# add the Handlers to the Logger object
logger.addHandler(log_handler_file)
logger.addHandler(log_handler_stream)


# %% [markdown]
# ## Create the archive folder for the daily backup
# - this stores the copied JSON files
# - this folder is later zipped to create the ZIP archive (and save space)

# %%
# check if the current output directory already exists in the backup folder location (it should not).
# If not, create it

if not arch_folder.is_dir():
    try:
        Path.mkdir(arch_folder)

        # log the start time of the backup
        logger.info("backup start")

        logger.info("archive folder created: " + str(arch_folder))
    except:
        logger.critical("unable to create archive folder")


# %% [markdown]
# ## Iterate through all files in the Portal Items Folder
# - find the valid JSON configuration files
# - copy those to the backup folder

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
            logger.debug("file: " + file)

            if len(file) == 32:
                try:
                    # attempt to convert the filename string to an integer
                    test_int = int(file, 16)

                    # copy the file
                    shutil.copy2(os.path.join(root,file), arch_folder)

                    logger.info(str(file) + " copied")

                except ValueError:
                    # the file name is not a valid UUID, which means it's not the Item json we want to copy

                    # pass
                    logger.debug(str(file) + " not copied")

    logger.info("done copying JSON files")

# %%
# Run the function to copy the files...

copy_json_files(items_path)

# %% [markdown]
# ## At this point:
# - the current Portal Item JSON files have been copied from `items_path` to a backup folder `arch_folder`
#
# Next:
# - zip and delete the folder of JSON files
# - delete the oldest zip files to maintain the file retention limit setting
#
# Note: Zip archive file size seems to be about 40% of the unzipped folder size

# %%
# create the zip file and add files to it
logger.info("creating ZIP archive: " + str(arch_zip))

with ZipFile(arch_zip, mode='w', compression=ZIP_DEFLATED, compresslevel=9) as outzip:

    logger.debug("opened ZIP file")

    for itemfile in Path(arch_folder).iterdir():

        # write the Item JSON file to the zip archive
        # by default, this creates a series of subfolders inside the ZIP file, in the same structure as the original
        # this makes it diffcult to browse ZIP files and restore their content (x subfolders deep, etc)
        # strip out the leading path of subfolders by specifying arcname=itemfile.name

        outzip.write(itemfile, arcname=itemfile.name)

        logger.debug(str(itemfile) + " added to ZIP archive")

        # delete the original file
        itemfile.unlink()
        logger.debug(str(itemfile) + " deleted from archive folder")

    outzip.close()
    logger.debug("closed ZIP file")

# remove the empty archive folder
arch_folder.rmdir()

logger.info("archive folder deleted")


# %% [markdown]
# Remove the oldest archive(s) to maintain the retention limit

# %%
# get a list of all zip files in the archive folder

filelist = list(arch_path.glob('*.zip'))

logger.info(str(len(filelist)) + " existing ZIP files")

# Sort the filenames in ascending order
# this is also chronological order, since filenames are based on date and time of archive
filelist.sort()

if len(filelist) > retention_limit:

    # slice off a list of files to drop from the FRONT of the sorted list
    # when sorted alphabetically, the oldest files are first

    dropfiles = filelist[:(len(filelist) - retention_limit)]

    logger.info(str(len(dropfiles)) + " removed to maintain retention limit of " + str(retention_limit) + " ZIP files")

    for file in dropfiles:
        Path.unlink(file)
        logger.debug(str(file) + " deleted")


logger.info("backup complete")
# logging.shutdown()  # this might not be needed when running as a script
