# Backup Scripts

## Basic Purpose

Scripts that are used for backing up folders of data.  More will be added as they are developed.

## Specific Scripts

`portal_item_backup.ipynb`

### Purpose

- this is used specifically for ArcGIS Portal servers
- copies the JSON configuration files for each Item in the Portal
- these files can be used in the future to restore or examine a Portal Item's configuration if something goes wrong

### Functionality

- Scheduled to run regularly on a server with **Portal for ArcGIS** installed as a Task in Windows Task Scheduler
- Required Inputs:
  - the location of the folder containing the Portal Item configurations (ex: `D:\arcgisportal\content\items`)
  - the location where archived files are stored (ex: `D:\Backups_portal_items`)
  - the number of zipped archive files to retain. If the task is scheduled to run daily, this will be the number of days that are archived. Oldest file gets deleted when the retention limit is reached.
  - debug level to store in log file. Normally, this would be `INFO` to, but can be changed to `DEBUG` if problems occur.
    
