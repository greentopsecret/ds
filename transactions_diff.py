#!/usr/bin/env python3

import argparse
import re
import sys
from datetime import datetime
from difflib import unified_diff

from numpy import genfromtxt


def get_buxfer_transactions(file):
    try:
        file = open(file, 'r')
    except:
        print('Cannot read data from the file "%s" (%s)' % (file, sys.exc_info()[0]))
        sys.exit(1)

    data = []
    while True:
        item = file.readline()
        if not item:
            break
        item = clean_commas_from_comments(item.strip())
        data.append(item.split(','))

    data = data[1:]

    return [
        [
            datetime.strptime(item[0], '%Y-%m-%d'),
            float(str.replace(item[3], ',', '.')),
            '%s %s' % (item[1].strip('"'), item[4])
        ]
        for item in data
    ]


def get_commerzbank_main_transactions(file):
    try:
        file = open(file, 'r')
    except:
        print('Cannot read data from the file "%s" (%s)' % (file, sys.exc_info()[0]))
        sys.exit(1)

    data = []
    while True:
        item = file.readline()
        if not item:
            break
        item = item.strip()
        item = clean_commas_from_comments(item)

        data.append(item.split(','))

    return [
        [
            datetime.strptime(line[0], '%d.%m.%Y'),
            float(str.replace(line[4], ',', '.')),
            '%s %s' % (line[3].strip('"'), line[9])
        ]
        for line in data[1:]
    ]


def get_commerzbank_visa_transactions(file):
    try:
        data = genfromtxt(file, delimiter=';', skip_header=1, dtype=str)
    except:
        print('Cannot read data from the file "%s" (%s)' % (file, sys.exc_info()[0]))
        sys.exit(1)

    return [
        [
            datetime.strptime(item[1], '%d.%m.%Y'),
            float(str.replace(item[3], ',', '.')),
            '%s (%s)' % (item[2], item[8])
        ]
        for item in data
    ]


def get_commerzbank_save_transactions(file):
    try:
        data = genfromtxt(file, delimiter=',', skip_header=1, dtype=str)
    except:
        print('Cannot read data from the file "%s" (%s)' % (file, sys.exc_info()[0]))
        sys.exit(1)

    return [
        [
            datetime.strptime(item[1], '%d.%m.%Y'),
            float(item[4]),
            item[3]
        ]
        for item in data
    ]


def get_n26_transactions(file):
    try:
        file = open(file, 'r')
    except:
        print('Cannot read data from the file "%s" (%s)' % (file, sys.exc_info()[0]))
        sys.exit(1)

    data = []
    while True:
        item = file.readline()
        if not item:
            break
        item = clean_commas_from_comments(item.strip())
        data.append(item.split(','))

    data = data[1:]

    return [
        [
            datetime.strptime(line[0].strip('"'), '%Y-%m-%d'),
            float(line[6].strip('"')),
            '%s %s %s' % (line[1].strip('"'), line[4].strip('"'), line[5].strip('"'))
        ]
        for line in data
    ]


def clean_commas_from_comments(line: str) -> str:
    matches = re.findall(r'"[^"]*"', line)
    for match in matches:
        line = line.replace(match, match.replace(',', ';'))

    return line


def build_amounts_by_date_lists(transactions: list):
    transactions = sorted(transactions, key=lambda x: x[1])
    result = {}
    for transaction in transactions:
        date: str = transaction[0]
        amount = transaction[1]
        comment = transaction[2]
        transactions_with_same_amount = result.get(amount, {})
        transactions_with_same_amount_and_date = transactions_with_same_amount.get(date, [])
        transactions_with_same_amount_and_date.append((date, amount, comment))
        transactions_with_same_amount[date] = transactions_with_same_amount_and_date
        result[amount] = transactions_with_same_amount
    return result


def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('compare_to', metavar='compare-to',
                        choices=('commerzbank-main', 'commerzbank-visa', 'commerzbank-save', 'n26'))
    parser.add_argument('--buxfer-file', help='Buxfer transactions source file',
                        default='/Users/maxim/Downloads/transactions-buxfer.csv')
    parser.add_argument('--bank-file', help='Bank transactions source file',
                        default='/Users/maxim/Downloads/transactions-bank.csv')
    # parser.add_argument('--verbose', help='Print debug info', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    return args


def transactions_to_strings(transactions):
    result = []
    for transaction in transactions:
        result.append('%s ; %s ; %s ; %s' % (
            transaction[0].strftime('%Y/%m/%d'),
            transaction[1],
            transaction[2],
            'expense' if transaction[1] < 0 else 'income'
        ))

    return result


def main():
    args = get_args()
    # args.compare_to = 'n26'
    # args.bank_file = '/Users/maxim/Downloads/transactions-n26.csv'
    # args.buxfer_file = '/Users/maxim/Downloads/transactions-buxfer.csv'

    print(args)

    bank_transactions_retrievers = {
        'commerzbank-main': get_commerzbank_main_transactions,
        'commerzbank-visa': get_commerzbank_visa_transactions,
        'commerzbank-save': get_commerzbank_save_transactions,
        'n26': get_n26_transactions
    }

    all_bank_transactions = bank_transactions_retrievers[args.compare_to](args.bank_file)
    buxfer_transactions = get_buxfer_transactions(args.buxfer_file)

    all_bank_transactions = build_amounts_by_date_lists(all_bank_transactions)
    buxfer_transactions = build_amounts_by_date_lists(buxfer_transactions)

    inconsistent_buxfer_transactions = []
    inconsistent_bank_transactions = []
    for amount, bank_transaction_by_date in all_bank_transactions.items():
        if amount in buxfer_transactions.keys():
            buxfer_transactions_with_same_amount = buxfer_transactions[amount]
            for date, bank_transactions in bank_transaction_by_date.items():
                if date in buxfer_transactions_with_same_amount.keys():
                    if len(buxfer_transactions_with_same_amount[date]) != len(bank_transactions):
                        for key, values in buxfer_transactions_with_same_amount.items():
                            inconsistent_buxfer_transactions.extend(transactions_to_strings(values))
                        inconsistent_bank_transactions.extend(transactions_to_strings(bank_transactions))
                else:
                    for key, values in buxfer_transactions_with_same_amount.items():
                        inconsistent_buxfer_transactions.extend(transactions_to_strings(values))
                    inconsistent_bank_transactions.extend(transactions_to_strings(bank_transactions))
        else:
            for key, values in bank_transaction_by_date.items():
                inconsistent_bank_transactions.extend(transactions_to_strings(values))

    for line in unified_diff(
            inconsistent_buxfer_transactions,
            inconsistent_bank_transactions,
            fromfile='buxfer',
            tofile='bank',
            n=0):
        print(line)

if __name__ == '__main__':
    main()
