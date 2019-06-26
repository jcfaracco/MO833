#!/usr/bin/python3

#!/usr/bin/python3

import argparse

def get_result(lines):
    result = list()
    capture = False
    for line in lines:
        if capture:
            result.append(line)
        if "End of simulation" in line:
            capture = True
    return result

class Results(object):
    def __init__(self):
        self.count = 0
        self.core_t = 0.0
        self.wall_t = 0.0
        self.perc_t = 0.0
        self.core_p = 0.0
        self.wall_p = 0.0

    def __get_numbers(self, results, line, index):
        res = list()
        data = results[line][:-1].split(":")[1].lstrip().split(" ")
        for d in data:
            if len(d) > 0:
                res.append(d)
        return res[index]

    def print_total(self, results):
        print("%s,%s,%s,%s" % (self.__get_numbers(results, 0, 0),
                               self.__get_numbers(results, 0, 1),
                               self.__get_numbers(results, 2, 0),
                               self.__get_numbers(results, 2, 1)))

    def append(self, results):
        self.count += 1
        core_t = float(self.__get_numbers(results, 0, 0))
        wall_t = float(self.__get_numbers(results, 0, 1))
        perc_t = float(self.__get_numbers(results, 0, 2))
        core_p = float(self.__get_numbers(results, 2, 0))
        wall_p = float(self.__get_numbers(results, 2, 1))

        self.core_t += core_t
        self.wall_t += wall_t
        self.perc_t += perc_t
        self.core_p += core_p
        self.wall_p += wall_p

    def average(self):
        self.core_t = self.core_t/self.count
        self.wall_t = self.wall_t/self.count
        self.perc_t = self.perc_t/self.count
        self.core_p = self.core_p/self.count
        self.wall_p = self.wall_p/self.count

    def print(self):
        print("Tests: %s" % self.count)
        print("Core time (seconds): %s" % self.core_t)
        print("Wall time (seconds): %s" % self.wall_t)
        print("Performance: (Core/Wall): %s %s" % (self.core_p, self.wall_p))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=str,
                        help="Output file to generate report")

    args = parser.parse_args()

    if (not args.file):
        print("No input file...")

    results = Results()

    with open(args.file) as fp:
        lines = fp.readlines()
        result = list()
        capture = False
        for line in lines:
            if capture:
                result.append(line)
            if "Core t (s)" in line:
                capture = True
            if "End of test" in line:
                capture = False
                results.print_total(result)
                results.append(result)
                result = list()

    results.average()
    results.print()
