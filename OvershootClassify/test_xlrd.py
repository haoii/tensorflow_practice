# test_xlrd.py

import xlrd

def main():
    data = xlrd.open_workbook('SourceData/data1.xlsx')
    table = data.sheets()[0]

    print(table.row_values(1))


if __name__ == '__main__':
    main()