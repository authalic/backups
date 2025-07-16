# Backup Scripts

Scripts that are used for backing up data.  More will be added as they are developed.

## **`portal_item_backup.ipynb`**

### Purpose

- this is used specifically for **ArcGIS Portal** servers
- copies the JSON configuration files for each Item in the Portal
- these files can be used in the future to restore or examine a Portal Item's configuration if something goes wrong

### Functionality

- Scheduled to run regularly on a server with **Portal for ArcGIS** installed as a Task in Windows Task Scheduler
- Required Inputs:
  - the location of the folder containing the Portal Item configurations (ex: `D:\arcgisportal\content\items`)
  - the location where archived files are stored (ex: `D:\Backups_portal_items`)
  - the number of zipped archive files to retain. If the task is scheduled to run daily, this will be the number of days that are archived. Oldest file gets deleted when the retention limit is reached.
  - debug level to store in log file. Normally, this would be `INFO` to, but can be changed to `DEBUG` if problems occur.


## **`gis_enterprise_reporter.ipynb`**

### Purpose

- this is used to run **GIS Enterprise Reporter** as a scheduled task on Portal machines, and handle the output reports to make them easier to archive by Deployment and Date
   - developed by Danny Krouk, Esri
   - see github repo: [GIS Enterprise Reporter](https://github.com/dannykrouk/gisenterprisereporter)


### Functionality

- schedule this Python script to run regularly as a Task in Windows Task Scheduler on a server with **Portal for ArcGIS** installed
  - in order to get complete reports, run the exe on the Enterprise server with Portal for ArcGIS installed
  - when run from another machine, some info won't get compiled into the reports, even if it can access the portal
- this Python script calls the `er.exe` executable, with the file `er.config` as its argument
- `er.exe` runs GIS Enterprise Reporter, based on the parameters set in `er.config` and outputs 3 Excel files and a log file
  - this can take 10 to 30+ minutes, depending on the size of the deployment
- script then creates a ZIP archive file, with the name formatted: `central_udot_utah_gov_portal_20250715`
zips the output files, names the zip file with the name of the Portal and a datestamp for the date on which the reports were run
- original output files are then deleted
  - ex: `C:\Esri\output\central_udot_utah_gov_portal_20250715.zip`
- script then deletes the original output files, retaining them in the Zip
- Outside of this script: Zip files are uploaded to a [Google Drive Folder](https://drive.google.com/drive/folders/17uM-3eBTG5Xg6OSzAvYZ2XAj_QfwgS_4)
  - this folder is shared with Jim Mcabee at Esri (jmcabee@esri.com) for his use in planning/optimizing the Enterprise deployments
