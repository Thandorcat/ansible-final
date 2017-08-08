#!/usr/bin/python
import virtualbox
import vagrant
import json
import os.path
from ansible.module_utils.basic import *

def start(vm):
    status = vm.status()[0][1]
    if (status != "running"):
        vm.up()
        if (vm.status()[0][1] == "running"):
            return False, True, "VM started!"
        else:
            return True, False, "VM start failed!"
    else:
        return False, False, "Already up!"


def stop(vm):
    status = vm.status()[0][1]
    if (status == "poweroff"):
        return False, False, "Already stopped!"
    elif (status == "running"):
        vm.halt()
        if (vm.status()[0][1] == "poweroff"):
            return False, True, "VM stopped!"
        else:
            return True, False, "VM stop failed!"
    elif (status == "not_created"):
        vm.up()
        vm.halt()
        if (vm.status()[0][1] == "poweroff"):
            return False, True, "VM stopped!"
        else:
            return True, False, "VM stop failed!"


def destroy(vm):
    status = vm.status()[0][1]
    if (status == "not_created"):
        return False, False, "Already destroyed!"
    elif (status == "running" or status == "poweroff"):
        vm.destroy()
        if (vm.status()[0][1] == "not_created"):
            return False, True, "VM destroyed!"
        else:
            return True, False, "VM destroy failed!"


def output(msg, state=None,
           address=None, port=None, path_to_ssh=None,
           username=None, os_name=None, ram=None):
    output = {}
    output['msg'] = msg
    if (state is not None):
        output['state'] = state
    if (address is not None):
        output['address'] = address
    if (port is not None):
        output['port'] = port
    if (path_to_ssh is not None):
        output['path_to_ssh'] = path_to_ssh
    if (username is not None):
        output['username'] = username
    if (os_name is not None):
        output['os_name'] = os_name
    if (ram is not None):
        output['ram'] = ram

    return output


def main():
    fields = {
        "path": {"required": True, "type": "str"},
        "state": {"required": True, "type": "str"},
        }

    module = AnsibleModule(argument_spec=fields)

    file = module.params['path']

    if os.path.isfile(file):
        file[:file.rfind('/')]
    elif (os.path.exists(file + "/Vagrantfile")):
        pass
    else:
        result = output("Vagrantfile not exists1!")
        module.exit_json(changed=False, failed=True, data=result)

    state = module.params['state']

    vm = vagrant.Vagrant(file)
    vbox = virtualbox.VirtualBox()

    if (state == "started"):
        failed, changed, msg = start(vm)
    elif (state == "stopped"):
        failed, changed, msg = stop(vm)
    elif (state == "destroyed"):
        failed, changed, msg = destroy(vm)
    else:
        failed, changed, msg = True, False, "Wrong state parameter, expected: started|stopped|destroyed"

    state = vm.status()[0][1]
    if (state == "running"):
        address = vm.hostname()
        port = vm.port()
        username = vm.user()
        path_to_ssh = vm.keyfile()
        vm_id_file = open(path_to_ssh[:path_to_ssh.rfind('/')] + '/id')
        vm_id = vm_id_file.read()
        os_name = vbox.find_machine(vm_id).os_type_id
        ram = vbox.find_machine(vm_id).memory_size

        result = output(msg, state, address, port, path_to_ssh, username, os_name, ram)
    else:
        result = output(msg, state)

    module.exit_json(changed=changed, failed=failed, data=result)



if __name__ == '__main__':
    main()
