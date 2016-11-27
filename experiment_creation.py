from algorithms import base_with_information_and_already_loaded,\
    bw_with_information_and_already_loaded
from ways.tools import dbopen
import pickle
from ways.graph import load_map_from_csv


def base_experiment(i, j, roads_junctions):
    path, num_closed, cost = base_with_information_and_already_loaded(i, j, roads_junctions)
    return num_closed, cost


def bw_experiment(i, j, abstract_map, roads_junctions):
    path, num_closed, cost = bw_with_information_and_already_loaded(i, j, abstract_map, roads_junctions)
    return num_closed, cost


def experiment_row(i, j, abstract_map, roads_junctions):
    num_closed, cost = base_experiment(i, j, roads_junctions)
    result = [i, j, num_closed, cost]
    for k in [0.0025, 0.005, 0.01, 0.05]:
        print(k)
        num_closed, cost = bw_experiment(i, j, abstract_map[k], roads_junctions)
        result.append([num_closed, cost])
    return result


def create_experiment_csv():
    roads_junctions = load_map_from_csv().junctions()
    K = {0.0025, 0.005, 0.01, 0.05}
    abstract_map_name = {k: 'abstractSpace_{}.pkl'.format(k) for k in K}
    import csv
    with dbopen('dataSet.csv', 'rt') as f:
        dataset = [(int(row[0]), int(row[1])) for row in csv.reader(f)]

    abstract_map = {}
    for k in K:
        with dbopen(abstract_map_name[k], 'rb') as f:
            abstract_map[k] = pickle.load(f)

    with dbopen('experiment.csv', 'wt'):
        for i, j in dataset:
            line = experiment_row(i, j, abstract_map, roads_junctions)
            #f.write((','.join(map(str, line)) + '\n'))
            print((','.join(map(str, line)) + '\n'))


if __name__ == '__main__':
    create_experiment_csv()
