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


class DataSetGenerate:
    def __init__(self, all_data):
        self.all_data = all_data

    def next_shuffle(self, percent):
        all_data_shuffle = [[[],[]],[[],[]]]
        for i in range(len(self.all_data[0])):
            if random.random() < percent:
                all_data_shuffle[0][0].append(self.all_data[0][i])
                all_data_shuffle[0][1].append(self.all_data[1][i])
            else:
                all_data_shuffle[1][0].append(self.all_data[0][i])
                all_data_shuffle[1][1].append(self.all_data[1][i])
        return all_data_shuffle


def get_speed_offset_ratio(target, actual, max, min):
    offset_ratio = []
    for i in range(len(target)):
        if actual[i] > target[i]:
            offset_ratio.append((actual[i] - target[i])/(max[i] - target[i]))
        else:
            offset_ratio.append(-(actual[i] - target[i])/(min[i] - target[i]))
    return offset_ratio

def read_data_set():
    labels = read_labels()
    all_data = [[],[]]
    for curve in range(1, NUM_OF_XFILE + 1):
        if curve in labels:
            xData_table = xlrd.open_workbook(
                PATF_OF_XFILE.format(curve)).sheet_by_index(0)
            for i in range(len(labels[curve])):
                speed_target = xData_table.col_values(8 + i*5)[1:41]
                speed_actual = xData_table.col_values(11 + i*5)[1:41]
                speed_max = xData_table.col_values(9 + i*5)[1:41]
                speed_min = xData_table.col_values(10 + i*5)[1:41]
                speed_offset_ratio = get_speed_offset_ratio(
                    speed_target, speed_actual, speed_max, speed_min)
                
                all_data[0].append(speed_offset_ratio)
                all_data[1].append(get_label_type(labels[curve][i]))
    return DataSetGenerate(all_data)



#read_data_set()