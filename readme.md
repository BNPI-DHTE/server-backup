# Python archiver for field data projects

This archiver application designed for Bükk National Park Directorate field data collector
system. It can archive the collected data and other important files, for example
QField/QGIS project files.

The application can create an archive from files filtered by list of extensions in a given
folder and its subfolders. In a json file, you can add some options to the application.
The name of the json file can be added as a command-line argument. The configuration file
detailed below.

To run the application, move to the application folder, enter the
`python3 backup.py settings.json` or `python3 backup.py settings.json`command in terminal.
In this case, the settings.json file will be in the application's folder.

## Configuration file

You have to create a .json file to define configurations. You can add multiple options as
json list items to the json file. For example:

    [
      {
        "backup_type": "data"
        "root_folder": "/home/data/fieldwork"
        "data_folder": "field/databases/"
        "backup_folder": "backup/"
        "extension": [
          "gpkg",
          "gokg-wal",
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
to save.

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