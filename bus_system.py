from collections import deque

class BusStopNode:
    def __init__(self, name):
        self.name = name
        self.next = None
        self.list_passenger_queue = deque()

    def add_passenger(self, passenger):
        self.list_passenger_queue.append(passenger)

    def remove_passenger(self):
        if self.list_passenger_queue:
            return self.list_passenger_queue.popleft()
        return None

    def show_queue(self):
        return list(self.list_passenger_queue)

class RouteHistory:
    def __init__(self):
        self.list_stack = []

    def push(self, stop):
        self.list_stack.append(stop)

    def pop(self):
        if self.list_stack:
            return self.list_stack.pop()
        return None

    def show_history(self):
        return self.list_stack.copy()

class RouteTreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def find(self, target_name):
        if self.name == target_name:
            return self
        for child in self.children:
            result = child.find(target_name)
            if result:
                return result
        return None

    def show_tree(self, level=0):
        indent = "  " * level
        result = f"{indent}{self.name}\n"
        for child in self.children:
            result += child.show_tree(level + 1)
        return result

class ZoteeStation:
    def __init__(self):
        self.routes = {}
        self.route_tree = RouteTreeNode("ZOTEE Station")
        self.history = RouteHistory()

    def add_route(self, route_name, stops):
        if route_name in self.routes:
            return False
        head = None
        current = None
        route_node = RouteTreeNode(route_name)
        self.route_tree.add_child(route_node)
        for stop_name in stops:
            stop = BusStopNode(stop_name)
            if head is None:
                head = stop
                current = stop
            else:
                current.next = stop
                current = stop
            route_node.add_child(RouteTreeNode(stop_name))
        self.routes[route_name] = head
        return True

    def show_route(self, route_name):
        if route_name not in self.routes:
            return None
        stops = []
        current = self.routes[route_name]
        while current:
            stops.append(current.name)
            current = current.next
        return stops

    def add_passenger(self, passenger, stop_name):
        for route in self.routes.values():
            current = route
            while current:
                if current.name == stop_name:
                    current.add_passenger(passenger)
                    return True
                current = current.next
        return False

    def move_bus(self, route_name):
        if route_name not in self.routes:
            return False
        current = self.routes[route_name]
        while current:
            while current.list_passenger_queue:
                passenger = current.remove_passenger()
            self.history.push(current.name)
            current = current.next
        return True

    def reverse_route(self, route_name):
        if route_name not in self.routes:
            return False

        reversed_stops = []
        while self.history.list_stack:
            stop = self.history.pop()
            reversed_stops.append(stop)

        if reversed_stops:
            head = None
            current = None
            for stop_name in reversed_stops:
                stop = BusStopNode(stop_name)
                if head is None:
                    head = stop
                    current = stop
                else:
                    current.next = stop
                    current = stop
            self.routes[route_name] = head
        return True

    def show_all_routes(self):
        self.route_tree.show_tree()