# Python archiver for field data projects

This archiver application designed for Bükk National Park Directorate field data collector
system. It can archive the collected data and other important files, for example
QField/QGIS project files.

The application can create an archive from files filtered by list of extensions in a given
folder and its subfolders. In a json file, you can add some options to the application.
The name of the json file can be added as a command-line argument. The configuration file
detailed below.

The conception is quite simple. You can define a root folder, which is an absolute path on
your machine. Somewhere inside this path you can add a data folder. This is, where your
files are being. This path is relative to your root folder, and this will be the created
archive's highest level. The third path is the backup folder, where you will find your
created archive. This is also relative to the root folder. You can filter the files you want
to save by an arrwy of extensions. 

## Installing and running

You can clone the git repository, if you have access rights.
You have to have a Python interpreter and pip installed on the computer.

To run the application, move to the application folder, enter the
`python3 main.py settings.json` or `python main.py settings.json`command in terminal, 
depending on your python installation and/or operating system. In this case, the settings.json
file must be in the application's folder.

### Dependencies

The python dependencies need only for running tests. To install dependencies run the following
command:  
`pip install -r requirements.txt`

### Run the tests

You can run the tests with the following command: `python3 -m pytest` or `python -m pytest`

## Features

- configuration via json
- can work with multiple configurations 
- filter files by extensions
- gzip, bzip2 or lzma output
- logging to file

## Configuration file

You have to create a .json file to define configurations. You can add multiple options as
json list items to the json file. For example:

    [
      {
        "backup_type": "data",
        "root_folder": "/home/data/fieldwork",
        "data_folder": "field/databases/",
        "backup_folder": "backup/",
        "extensions": [
          "gpkg",
          "gpkg-wal",
          "gpkg-shm"
        ],
        "archive_type": "gz"
      },
      {
        "backup_type": "project",
        "root_folder": "/home/data/fieldwork",
        "data_folder": "field/projectfiles/",
        "backup_folder": "backup/",
        "extensions": [
          "qgs",
          "qgz",
          "zip",
          "db"
        ],
        "archive_type": "bz2"
      }
    ]

Using the configuration file above, the application will work in the
`/home/data/fieldwork` folder. The first section will save the geopackage files being
inside the `/home/data/fieldwork/field/databases` folder recursively into the
`/home/data/fieldwork/backup/data` folder as a tar.gz file. The archive file's name will
be `data_yyyy_mm_dd_hh_MM_ss.tar.gz`, where `yyyy_mm_dd_hh_MM_ss` is the archiving date
and time.  

The second section will save recursively all the QGIS projects and related files being
inside the `/home/data/fieldwork/field/projectfiles/` into a
`project_yyyy_mm_dd_hh_MM_ss.tar.bz2` file, which will be inside the
`/home/data/fieldwork/backup/project` folder.

### Backup type
Necessary.  
No default value.  
Type of the files you want to back up (data, project files, etc.) Will create a subfolder
with the backup type name inside backup folder. The name of the file will also contain
the type of backup.

### Root folder
Necessary.  
No default value.  
The root folder of the project. The root folder must contain the 
data and the backup folder.

### Data folder
Necessary.  
No default value.  
The data folder relative to the root folder, you want to back up. This contains the files
to save. The root folder could also be used as data folder.

### Backup folder
Necessary.  
No default value.  
The folder where you will save archives. Relative path to the root folder.

### Extension
Optional.  
Default value: `"*"`
You can add list of extensions, the application will filter and archive only these files.
Don't need to add punctuation marks before extensions.

### Archive type
Optional.  
Default value: `"bz2"`
This option will set the archive format.
There are three values you can use in this field: gz (gzip compression), xz (lzma
compression), bz2 (bzip2 compression).

## Logging

The application logs into a file inside the application folder.
No independent logging configuration implemented.If you want to change logging configuration,
you have to edit the main function inside main.py. In this case, it is recommended to have a 
clear knowledge of python logging, or I suggest you to read the python logging documentations.

There can be found four logging levels in the application: debug, info, warning and critical.
No error level, because all the errors are critical. 
