#!/usr/bin/env python3

from numpy import genfromtxt, string_
from datetime import datetime
from difflib import unified_diff
import sys, re, argparse

def get_commerzbank_main_transactions(file):
    data = genfromtxt(file, delimiter=';', skip_header=1, dtype=str)
    try:
        data = genfromtxt(file, delimiter=';', skip_header=1, dtype=str)
    except:
        print('Cannot read data from the file "%s" (%s)' % (file, sys.exc_info()[0]))
        sys.exit(1)

    # data = data[data[:,4].argsort()]
    # print(data)

    data = [
        [datetime.strptime(line[0], '%d.%m.%Y').strftime('%Y-%m-%d'), float(str.replace(line[4], ',', '.'))]
        for line in data
    ]

    data = sorted(data, key=lambda x: x[1])

    return ['%s => %s' % (line[0], line[1]) for line in data]

def get_commerzbank_visa_transactions(file):
    try:
        data = genfromtxt(file, delimiter=';', skip_header=1, dtype=str)
    except:
        print('Cannot read data from the file "%s" (%s)' % (file, sys.exc_info()[0]))
        sys.exit(1)

    data = [
        [datetime.strptime(line[0], '%d.%m.%Y').strftime('%Y-%m-%d'), float(str.replace(line[3], ',', '.')), line[2], line[8]]
        for line in data
    ]

    data = sorted(data, key=lambda x: x[1])

    return ['%s => %s' % (line[0], line[1]) for line in data]

def get_buxfer_transactions(file):
    try:
        file = open(file, 'r')
    except:
        print('Cannot read data from the file "%s" (%s)' % (file, sys.exc_info()[0]))
        sys.exit(1)

    data = []
    while True:
        line = file.readline()
        if not line:
            break
        line = line.strip()
        line = re.sub(r'"([^"]+)"', r'xxxxx', line)
        data.append(line.split(','))

    data = data[1:]

    data = [
        [datetime.strptime(line[0], '%Y-%m-%d').strftime('%Y-%m-%d'), float(str.replace(line[3], ',', '.'))]
        for line in data
    ]

    data = sorted(data, key=lambda x: x[1])

    return [
        '%s => %s' % (line[0], line[1])
        for line in data
    ]

def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('compare_to', metavar='compare-to', choices=('commerzbank-main', 'commerzbank-visa'))
    parser.add_argument('--buxfer-file', help='Buxfer transactions source file', default='/Users/maxim/Downloads/transactions-buxfer.csv')
    parser.add_argument('--bank-file', help='Bank transactions source file', default='/Users/maxim/Downloads/transactions-commerzbank.csv')
    # parser.add_argument('--verbose', help='Print debug info', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    return args

args = get_args()

print(args)

bank_transactions_retrievers = {
    'commerzbank-main': get_commerzbank_main_transactions,
    'commerzbank-visa': get_commerzbank_visa_transactions
}

bank_transactions = bank_transactions_retrievers[args.compare_to](args.bank_file)

# if args.compare_to == 'commerzbank-main':
#     bank_transactions = get_commerzbank_main_transactions(args.commerzbank_main_file)
# elif args.compare_to == 'commerzbank-visa':
#     bank_transactions = get_commerzbank_visa_transactions(args.commerzbank_visa_file)

buxfer_transactions = get_buxfer_transactions(args.buxfer_file)

# print('buxfer_transactions: %s' % buxfer_transactions)
# print('bank_transactions: %s' % bank_transactions)
for line in unified_diff(buxfer_transactions, bank_transactions, fromfile='buxfer', tofile='bank', n=0):
    print(line)