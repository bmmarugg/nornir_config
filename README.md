# Nornir Configuration Script

## Description:
This is a cript that utilizes Nornir to push configuration files to a single or group of devices that a user can define. User can define whether the configuration push is a full replace or just a merge. The script will perform a dry run first, always, to show what lines of code are being added, omitted, or changed. Users will then be prompted to confirm the commitment of the new code before Nornir will finalize the process.


## Directions for use:
Users will need to define the filter type, filter to apply, configuration type, and path to candidate configuration file, in that order, when they run the command. The syntax for the command is as follows:

python nornir_config.py {group, name} <i>group/device name</i> {replace, merge} <i>path to/name of candidate config</i>
