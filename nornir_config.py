from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import urllib3
import sys
import yaml
import argparse
import time


urllib3.disable_warnings()

nr = InitNornir(
    core={"num_workers": 100},
    inventory={
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "options": {
            "host_file": "path/to/hosts.yaml",
            "group_file": "path/to/groups.yaml",
        }
    }
)


def main():
    my_parser = argparse.ArgumentParser(prog='nornirconfigpush')
    my_parser.add_argument('filter_type', choices=['group', 'name'], help='type of filter')
    my_parser.add_argument('filter', help='name of device(s) or group(s) to filter on')
    my_parser.add_argument('config_type', help='type of configuration', choices=['merge', 'replace'])
    my_parser.add_argument('config_file', help='path to config file')

    args = my_parser.parse_args()
    ftype = args.filter_type
    device_filter = args.filter
    conf_type = args.config_type
    config_file = args.config_file


    if ftype == 'name':
        device_run = nr.filter(F(name__contains=device_filter))
    elif ftype == 'group':
        device_run = nr.filter(F(groups__contains=device_filter))

    def commit_changes_replace():
        results = device_run.run(task=networking.napalm_configure,
                                 dry_run=True,
                                 filename=config_file,
                                 replace=True)
        print_result(results)
        print("Check over the changes VERY CAREFULLY." + "\n" * 2)
        time.sleep(10)

        commit = input("Type COMMIT to complete configuration. Type anything else to exit." + "\n")
        if "COMMIT" in commit:
            print("Committing changes to device(s) now...")
            results = device_run.run(task=networking.napalm_configure,
                                  dry_run=False,
                                  filename=config_file,
                                  replace=True)
            print_result(results)
        else:
            print("Backing out now.")
            sys.exit()

    def commit_changes_merge():
        results = device_run.run(task=networking.napalm_configure,
                                 dry_run=True,
                                 filename=config_file,
                                 replace=False)
        print_result(results)
        print("Check over the changes VERY CAREFULLY." + "\n" * 2)
        time.sleep(10)

        commit = input("Type COMMIT to complete configuration. Type anything else to exit." + "\n")
        if "COMMIT" in commit:
            print("Committing changes to device(s) now...")
            results = device_run.run(task=networking.napalm_configure,
                                  dry_run=False,
                                  filename=config_file,
                                  replace=False)
            print_result(results)
        else:
            print("Backing out now.")
            sys.exit()

    if conf_type.lower() == 'merge':
        commit_changes_merge()
    elif conf_type.lower() == 'replace':
        commit_changes_replace()
    else:
        sys.exit()


if __name__ == "__main__":
    main()