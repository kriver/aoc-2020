#!/usr/bin/env python3
import re
from typing import List

from util import load

REQ_FLD = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
OPT_FLD = ['cid']

HGT_REGEX = re.compile(r'^(\d+)(cm|in)$')
HCL_REGEX = re.compile(r'^#[0-9a-f]{6}$')
PID_REGEX = re.compile(r'^[0-9]{9}$')
ECL_VALID = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


class Passport:
    def __init__(self):
        self._data = {}

    def __repr__(self):
        return str(self._data)

    def add_data(self, data: List[str]):
        for d in data:
            k, v = d.split(':')
            self._data[k] = v

    def is_valid_1(self):
        for k in REQ_FLD:
            if k not in self._data:
                return False
        return True

    @staticmethod
    def _number_between(val, low, high):
        try:
            num = int(val)
            return low <= num <= high
        except ValueError:
            return False

    def valid_byr(self):
        return self._number_between(self._data['byr'], 1920, 2002)

    def valid_iyr(self):
        return self._number_between(self._data['iyr'], 2010, 2020)

    def valid_eyr(self):
        return self._number_between(self._data['eyr'], 2020, 2030)

    def valid_hgt(self):
        m = re.match(HGT_REGEX, self._data['hgt'])
        if not m:
            return False
        if m.group(2) == 'cm':
            return self._number_between(m.group(1), 150, 193)
        elif m.group(2) == 'in':
            return self._number_between(m.group(1), 59, 76)
        else:
            return False

    def valid_hcl(self):
        return re.match(HCL_REGEX, self._data['hcl'])

    def valid_ecl(self):
        return self._data['ecl'] in ECL_VALID

    def valid_pid(self):
        return re.match(PID_REGEX, self._data['pid'])

    def is_valid_2(self):
        return self.is_valid_1() \
               and self.valid_byr() \
               and self.valid_iyr() \
               and self.valid_eyr() \
               and self.valid_hgt() \
               and self.valid_hcl() \
               and self.valid_ecl() \
               and self.valid_pid()


def parse(data) -> List[Passport]:
    pp_list = []
    pp = None
    for line in data:
        if len(line) == 0:
            if pp:
                pp_list.append(pp)
                pp = None
        else:
            if not pp:
                pp = Passport()
            pp.add_data(line.split(' '))
    if pp:
        pp_list.append(pp)
    return pp_list


if __name__ == "__main__":
    passports = parse(load('day4.txt'))

    valid_pp = list(filter(lambda p: p.is_valid_1(), passports))
    assert len(valid_pp) == 235
    print("Valid passports: %d/%d" % (len(valid_pp), len(passports)))

    valid_pp = list(filter(lambda p: p.is_valid_2(), passports))
    assert len(valid_pp) == 194
    print("Valid passports: %d/%d" % (len(valid_pp), len(passports)))
