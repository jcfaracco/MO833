#!/usr/bin/python3

import paramiko
import argparse


def get_hosts(filename):
    data = list()
    with open(filename) as fp:
        data = fp.readlines()
    return data

def get_result(lines):
    result = list()
    capture = False
    for line in lines:
        if capture:
            result.append(line)
        if "End of simulation" in line:
            capture = True
    return result

def generate_hostfile(hostnames, slots=0, hmax=None):
    hoststr = ""
    i = 0
    for hostname in hostnames[1:]:
        if (hmax and i == hmax):
            break
        if slots:
            hoststr += ("%s slots=%s\n" % (hostname[:-1], slots))
        else:
            hoststr += ("%s\n" % hostname[:-1])
        i += 1
    return hoststr

class Results(object):
    def __init__(self):
        self.count = 0
        self.total_t = 0.0
        self.solver_t = 0.0
        self.assembly_t = 0.0
        self.assembly_f = 0.0
        self.linear_t = 0.0
        self.linear_f = 0.0
        self.linear_s_t = 0.0
        self.linear_s_f = 0.0
        self.update_t = 0.0
        self.update_f = 0.0
        self.output_t = 0.0
        self.o_well_t = 0.0
        self.o_well_f = 0.0
        self.o_lineariza_t = 0.0
        self.o_lineariza_f = 0.0
        self.o_newton_t = 0.0
        self.o_newton_f = 0.0
        self.o_linear_t = 0.0
        self.o_linear_f = 0.0

    def __get_float(self, result):
        data = result.split(":", 1)
        return float(data[1].lstrip().rstrip().split(' ')[0])

    def __get_failed(self, result):
        data = result.split(":", 1)
        data = data[1].lstrip().rstrip()
        return float(data.split(":", 1)[1].split(";")[0].lstrip().rstrip())

    def print_total(self, results):
        print(self.__get_float(results[1])-self.__get_float(results[7]))

    def append(self, results):
        self.count += 1
        total_t       = self.__get_float(results[1])
        solver_t      = self.__get_float(results[2])
        assembly_t    = self.__get_float(results[3])
        assembly_f    = self.__get_failed(results[3])
        linear_t      = self.__get_float(results[4])
        linear_f      = self.__get_failed(results[4])
        linear_s_t    = self.__get_float(results[5])
        linear_s_f    = self.__get_failed(results[5])
        update_t      = self.__get_float(results[6])
        update_f      = self.__get_failed(results[6])
        output_t      = self.__get_float(results[7])
        o_well_t      = self.__get_float(results[8])
        o_well_f      = self.__get_failed(results[8])
        o_lineariza_t = self.__get_float(results[9])
        o_lineariza_f = self.__get_failed(results[9])
        o_newton_t    = self.__get_float(results[10])
        o_newton_f    = self.__get_failed(results[10])
        o_linear_t    = self.__get_float(results[11])
        o_linear_f    = self.__get_failed(results[11])

        self.total_t       += total_t
        self.solver_t      += solver_t
        self.assembly_t    += assembly_t
        self.assembly_f    += assembly_f
        self.linear_t      += linear_t
        self.linear_f      += linear_f
        self.linear_s_t    += linear_s_t
        self.linear_s_f    += linear_s_f
        self.update_t      += update_t
        self.update_f      += update_f
        self.output_t      += output_t
        self.o_well_t      += o_well_t
        self.o_well_f      += o_well_f
        self.o_lineariza_t += o_lineariza_t
        self.o_lineariza_f += o_lineariza_f
        self.o_newton_t    += o_newton_t
        self.o_newton_f    += o_newton_f
        self.o_linear_t    += o_linear_t
        self.o_linear_f    += o_linear_f

    def average(self):
        self.total_t       = self.total_t/self.count
        self.solver_t      = self.solver_t/self.count
        self.assembly_t    = self.assembly_t/self.count
        self.assembly_f    = self.assembly_f/self.count
        self.linear_t      = self.linear_t/self.count
        self.linear_f      = self.linear_f/self.count
        self.linear_s_t    = self.linear_s_t/self.count
        self.linear_s_f    = self.linear_s_f/self.count
        self.update_t      = self.update_t/self.count
        self.update_f      = self.update_f/self.count
        self.output_t      = self.output_t/self.count
        self.o_well_t      = self.o_well_t/self.count
        self.o_well_f      = self.o_well_f/self.count
        self.o_lineariza_t = self.o_lineariza_t/self.count
        self.o_lineariza_f = self.o_lineariza_f/self.count
        self.o_newton_t    = self.o_newton_t/self.count
        self.o_newton_f    = self.o_newton_f/self.count
        self.o_linear_t    = self.o_linear_t/self.count
        self.o_linear_f    = self.o_linear_f/self.count

    def print(self):
        print("Tests: %s" % self.count)
        print("Total time (seconds): %s" % self.total_t)
        print("Solver time (seconds): %s" % self.solver_t)
        print("Assembly time (seconds): %s\tFailed: %s" % (self.assembly_t, self.assembly_f))
        print("Linear solve time (seconds): %s\tFailed: %s" % (self.linear_t, self.linear_f))
        print("Linear solve setup time (seconds): %s\tFailed: %s" % (self.linear_s_t, self.linear_s_f))
        print("Update time (seconds): %s\tFailed: %s" % (self.update_t, self.update_f))
        print("Output time (seconds): %s" % self.output_t)
        print("Overall Well Iterations: %s\tFailed: %s" % (self.o_well_t, self.o_well_f))
        print("Overall Linearizations: %s\tFailed: %s" % (self.o_lineariza_t, self.o_lineariza_f))
        print("Overall Newton Iterations: %s\tFailed: %s" % (self.o_newton_t, self.o_newton_f))
        print("Overall Linear Iterations: %s\tFailed: %s" % (self.o_linear_t, self.o_linear_f))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", "-k", type=str,
                        help="key file to use secure connection")
    parser.add_argument("--mpi", action="store_true",
                        help="enable mpi")
    parser.add_argument("--slots", "-s", type=int, default=0,
                        help="number of each slot executed in each host")
    parser.add_argument("--max", type=int, default=-1,
                        help="number of each slot executed in each host")
    parser.add_argument("hostfile", type=str,
                        help="file with all hostnames used by this test")

    args = parser.parse_args()

    key = None
    if (args.key):
        key = paramiko.RSAKey.from_private_key_file(args.key)

    hostnames = get_hosts(args.hostfile)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting into %s" % hostnames[0])

    client.connect(hostname=hostnames[0], username="ubuntu", pkey=key)

    results = Results()

    if (args.max < 0):
        hmax = len(hostnames[1:])
    else:
        hmax = args.max

    if (len(hostnames) > 1 and hmax >= 1):
        hostfile = generate_hostfile(hostnames, args.slots, hmax)
        print(hostfile)

        command = ("echo -n '%s' > /home/ubuntu/opm/hostfile" % hostfile)
        stdin, stdout, stderr = client.exec_command(command)

        command = ("mpirun --hostfile /home/ubuntu/opm/hostfile -np %s sudo flow /home/ubuntu/opm/opm-data/spe1/SPE1CASE1.DATA" % hmax)
    else:
        command = "flow /home/ubuntu/opm/opm-data/spe1/SPE1CASE1.DATA"

    print(command)
    for i in range(0, 100):
        stdin, stdout, stderr = client.exec_command(command)
        result = get_result(stdout.read().decode("utf-8").split('\n'))
        results.print_total(result)
        results.append(result)

    results.average()
    results.print()
    
    client.close()
