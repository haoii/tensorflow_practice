# input_data.py

import xlrd
import random

NUM_OF_XFILE = 30
PATF_OF_XFILE = 'SourceData/data{}.xlsx'
PATH_OF_LABEL_FILE = 'SourceData/Labels.xlsx'

NUM_OF_TYPE = 9


def read_labels():
    Labels = {}
    label_table = xlrd.open_workbook(PATH_OF_LABEL_FILE).sheet_by_index(0)
    types = label_table.col_values(0)
    curves = label_table.col_values(2)
    for i, v in enumerate(curves):
        curve = int(v)
        if not curve in Labels:
            Labels[curve] = [types[i]]
        else:
            Labels[curve].append(types[i])
    return Labels


def get_label_type(label):
    label_type = [0] * NUM_OF_TYPE
    label_type[int(label - 1)] = 1
    return label_type


def read_data_set():
    labels = read_labels()
    # xData = []
    # labelData = []
    all_data = [[[],[]],[[],[]]]
    for curve in range(1, NUM_OF_XFILE + 1):
        if curve in labels:
            xData_table = xlrd.open_workbook(
                PATF_OF_XFILE.format(curve)).sheet_by_index(0)
            for i in range(len(labels[curve])):
                speed_target = xData_table.col_values(8 + i*5)
                speed_actual = xData_table.col_values(11 + i*5)
                speed_offset = map(lambda x: x[1]-x[0], 
                                   zip(speed_actual[1:41], speed_target[1:41]))

                if random.random() < 0.7:
                    all_data[0][0].append(speed_offset)
                    all_data[0][1].append(get_label_type(labels[curve][i]))
                else:
                    all_data[1][0].append(speed_offset)
                    all_data[1][1].append(get_label_type(labels[curve][i]))

    # return xData, labelData
    return all_data

#read_data_set()