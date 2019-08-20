# Nornir Configuration Script

## Description:
This is a cript that utilizes Nornir to push configuration files to a single or group of devices that a user can define. User can define whether the configuration push is a full replace or just a merge.

## Replace vs. Merge
It is worth knowing the differences between a configuration replace and a merge. 

  ### Replace:
  1. Creates backup snapshot configuration file prior to new configuration push;
  2. Replaces or deletes <b>all</b> lines of code in running-configuration that are different or don't exist in the candidate configuration. 
  Use with caution. 
