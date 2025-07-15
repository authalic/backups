# %% [markdown]
# # Zip the GIS Enterprise Reporter output reports
#
# 1. Call the executable to run the GIS Enterprise Reporter
# 2. Create a ZIP file archive with a filename formatted to include the Portal name and the date stamp
# 3. Delete the original files (now archived)

# %%
import os
import subprocess

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime

# %% [markdown]
# Call the GIS Enterprise Reporter executable, with the `er.config` file as the first argument
# - `er.config` contains the info needed to run the reports

# %%
subprocess.run(["C:\Esri\gis_enterprise_reporter\gis_enterprise_reporter\er.exe", "C:\Esri\er.config"])

# %% [markdown]
# After the reports have run, create a ZIP file

# %%
# use the same output directory in "C:\Esri\er.config"

OutputDirectory = Path(r"C:\Esri\output")

date_str = datetime.strftime(datetime.today(), r'%Y%m%d')  # 20250715

# get the first filename in the output directory, for building the name if the ZIP archive
for file in os.listdir(OutputDirectory):

    # skip any file that ends in .zip
    if file[-4:] != ".zip":
        report = file
        break

report_words = report.split('_')  # split the filename into a list

indx_portal = report_words.index('portal')  # find out where the word 'portal' is located (hint, it's 4)
report_words = report_words[0:indx_portal+1]  # get the first 5 words in the filename (to include 'portal')
report_words.append(date_str)  # append the date stamp to the list
zipfile = '_'.join(report_words)

# build the full path and filename of the ZIP archive
arch_zip = Path(OutputDirectory, zipfile).with_suffix(".zip")

# %% [markdown]
# Add the output reports to the ZIP file and delete the originals

# %%
# add files to the ZIP file
with ZipFile(arch_zip, mode='w', compression=ZIP_DEFLATED, compresslevel=9) as outzip:

    for itemfile in Path(OutputDirectory).iterdir():

        if str(itemfile)[-4:] != ".zip":

            print(itemfile)

            # add the file to the ZIP archive
            outzip.write(itemfile, arcname=itemfile.name)

            # delete the original file
            itemfile.unlink()
