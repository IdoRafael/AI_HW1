from ways.graph import load_map_from_csv
from uniform_cost_search import uniform_cost_search
from ways.tools import timed
from abstract_space_creation import make_abstract_space
import pickle


def base_with_information(source, target):
    roads_junctions = load_map_from_csv().junctions()

    # returns (path, number_closed, cost).
    # if no path found, returns (None, number_closed, None)
    return uniform_cost_search(source, target, lambda link: link.distance, roads_junctions)


def better_waze_with_information(source, target, abstractMap):
    roads_junctions = load_map_from_csv().junctions()
    centers = abstractMap.keys()

    # watch uniform cost search. can run it on abstract space by defining proper input
    # cost function(link): link.cost ((ABSTRACT_LINK))
    # and abstractMap as the roads_junctions (as it is a dict with junctions. same as roads_junctions)

if __name__ == '__main__':
    with open('files/abstractSpace_0.0001.pkl', 'rb') as f:
        aspace = pickle.load(f)
    print(839471 in aspace.keys())

