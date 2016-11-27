from heapq import heappop, heappush
from ways.graph import load_map_from_csv, Junction, Link, AbstractLink
from ways.tools import timed


class Node:
    def __init__(self, state, parent, cost):
        self.state = state
        self.parent = parent
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)


def _expand(state, roads_junctions):
    for link in roads_junctions[state].links:
        yield link


def _path(node: Node):
    path = []
    current = node
    while current is not None:
        path.insert(0, current.state)
        current = current.parent
    return path


# From heapq.py, since _siftdown is not meant to be used.
# Used for performance reasons
def _siftdown(heap, start_position, position):
    new_item = heap[position]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while position > start_position:
        parent_position = (position - 1) >> 1
        parent = heap[parent_position]
        if new_item < parent:
            heap[position] = parent
            position = parent_position
            continue
        break
    heap[position] = new_item


def _decrease_key(heap, index, new_key):
    heap[index].cost = new_key
    _siftdown(heap, 0, index)


def _uniform_cost_search_aux(source, roads_junctions, result_function, result_item, cost_function,
                             goal_test, centers=None, target=None, solution_limit=1):
    open_heapq = [Node(source, None, 0)]
    open_set = {source}
    close = set()
    result_list = []

    while open_heapq:
        next = heappop(open_heapq)
        open_set.discard(next.state)

        close.add(next.state)

        if goal_test(next, centers, source, target):
            result_list.append(result_item(next))
            if len(result_list) >= solution_limit:
                break
            else:
                continue

        for link in _expand(next.state, roads_junctions):
            if link.target not in close:
                new_cost = next.cost + cost_function(link)
                if link.target in open_set:
                    open_set.discard(link.target)
                    old_node_index = open_heapq.index(Node(link.target, None, None))
                    old_node = open_heapq[old_node_index]
                    if old_node.cost > new_cost:
                        old_node.parent = next
                        _decrease_key(open_heapq, old_node_index, new_cost)
                else:
                    heappush(open_heapq, Node(link.target, next, new_cost))
                    open_set.add(link.target)
    return result_function(source, result_list, roads_junctions, close)


def uniform_cost_search(source, target, cost_function, roads_junctions):
    def result_item(next):
        return _path(next)

    def goal_test(next, centers, source, target):
        return next.state == target

    def result_function(source, result_list, roads_junctions, close):
        if len(result_list) > 0:
            return (result_list[0], len(close))
        else:
            return None, len(close)

    return _uniform_cost_search_aux(
        source, roads_junctions, result_function, result_item, cost_function, goal_test, target=target
    )


def make_abstract_junction(source, roads_junctions, centers, solution_limit):
    def result_item(next):
        return AbstractLink(path=_path(next), target=next.state, cost=next.cost, highway_type=-1)

    def goal_test(next, centers, source, target):
        return next.state in centers and next.state != source

    def result_function(source, result_list, roads_junctions, close):
        return Junction(
            index=source, lat=roads_junctions[source].lat, lon=roads_junctions[source].lon, links=result_list
        ), len(close)

    def cost_function(link):
        return link.distance

    return _uniform_cost_search_aux(
        source, roads_junctions, result_function, result_item, cost_function,
        goal_test, centers=centers, solution_limit=solution_limit
    )


#TODO change result_item to return only next.state
def find_dataset_neighbour(source, roads_junctions):
    def result_item(next):
        return next.state, _path(next)

    def goal_test(next, centers, source, target):
        return next.cost >= 200

    def result_function(source, result_list, roads_junctions, close):
        if len(result_list) > 0:
            return result_list[0]
        else:
            return None

    def cost_function(link):
        return 1

    return _uniform_cost_search_aux(
        source, roads_junctions, result_function, result_item, cost_function, goal_test
    )