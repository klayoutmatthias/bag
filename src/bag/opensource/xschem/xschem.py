import os
import shutil
import re
import subprocess

def pinlist(schematic_file):

    with open(schematic_file) as file:
        pins = re.findall(r'C {devices\/[io]*pin.sym}.*lab=(.*)}', file.read())

    return pins

def instances(schematic_file):

    # find number of cells
    tcl_command = """puts [xschem get instances]"""
    number_cells = int(call(tcl_command=tcl_command, schematic=schematic_file)[0])

    # populate instance information
    instance_info = {}
    for instance in range(number_cells):

        # get instance name
        tcl_command = f"""puts [xschem getprop instance {instance} name]"""
        instance_name = call(tcl_command=tcl_command, schematic=schematic_file)
        if len(instance_name) > 0:
            instance_name = instance_name[0]
            instance_info[instance_name] = {}

            # get cell and library name
            tcl_command = f"""puts [xschem getprop instance {instance} cell::name]"""
            instance_info_str = call(tcl_command=tcl_command, schematic=schematic_file)[0]
            lib_name = instance_info_str.split('/')[0]
            cell_name = instance_info_str.split('/')[-1].split('.sym')[0]
            instance_info[instance_name]['lib_name'] = lib_name
            instance_info[instance_name]['cell_name'] = cell_name

            # get pins
            tcl_command = f"""puts [xschem instance_pins {instance}]"""
            pins = call(tcl_command=tcl_command, schematic=schematic_file)
            pins = [_.strip('{}') for _ in pins]

            # is subcircuit?
            instance_info[instance_name]['pins'] = {}
            tcl_command = f"""puts [xschem getprop instance {instance} spiceprefix]"""
            spiceprefix = call(tcl_command=tcl_command, schematic=schematic_file)

            if len(spiceprefix) > 0:
                if spiceprefix[0] == "X":

                    tcl_command = f"""puts [xschem pinlist {instance}]"""
                    pins = call(tcl_command=tcl_command, schematic=schematic_file, split=False)

                    tcl_command = f"""puts [xschem instance_nodemap {instance}]"""
                    nodemap_raw = call(tcl_command=tcl_command, schematic=schematic_file)
                    nodemap = {}
                    for i in range(int((len(nodemap_raw ) -1 ) /2)):
                        nodemap[nodemap_raw[ 2 * i +1]] = nodemap_raw[ 2 * i +2]

                    instance_info[instance_name]['pins'] = {}
                    pins = re.findall(r"{ {.*?} }", pins)
                    for pin in pins:

                        pin_name = re.findall(r"name=(\w+)", pin)[0]
                        instance_info[instance_name]['pins'][pin_name] = {}

                        pin_dir = re.findall(r"dir=(\w+)", pin)[0]
                        direction_map = {'in' :'input' ,'out' :'output' ,'inout' :'inputOutput'}
                        instance_info[instance_name]['pins'][pin_name]['direction'] = direction_map[pin_dir]

                        instance_info[instance_name]['pins'][pin_name]['net_name'] = nodemap[pin_name]

                        instance_info[instance_name]['pins'][pin_name]['num_bits'] = 1

    return instance_info

def schematic_filename(lib_name, cell_name):

    schematic_netlist = call(tcl_command=f'puts [abs_sym_path {lib_name}]')[0]

    schematic_netlist = f"{schematic_netlist}/{cell_name}/{cell_name}.sch"
    if not os.path.exists(schematic_netlist):
        schematic_netlist = f"{schematic_netlist}/{cell_name}.sch"

    return schematic_netlist


def call(tcl_command, schematic=None, folder=None, topcell=None, split=True):

    command = "xschem -q -x "

    # specify the output netlist
    if folder:
        command += "-o "
        command += os.getcwd() + "/" + folder + " "

    with open("/tmp/commands.tcl", "w") as file:
        file.write(tcl_command)
    command += "--script /tmp/commands.tcl "

    # include subcircuit definition
    if topcell:
        command += "--tcl set top_subckt 1 -n "

    # add the schematic
    if schematic:
        command += schematic

    # perform netlisting
    status = subprocess.check_output(
        command,
        shell=True,
        # TODO: un-hardcode
        cwd='/p/bootcamp2022/sdf_test/ws.pub.analog.connectivity/ips/main/home/bc.parryt/xschem',
    )

    response_last_line = status.decode("utf-8").split('\n')

    while '' in response_last_line:
        response_last_line.remove('')
    if len(response_last_line) > 0:
        response_last_line = response_last_line[-1]

    if split and isinstance(response_last_line, str):
        output = response_last_line.split(' ')
    else:
        output = response_last_line

    return output
