class BusStopNode:
    def __init__(self, name, next=None):
        self.name = name
        self.next = {}
        self.list_passenger_queue = []

    def add_passenger(self, passenger):
        self.list_passenger_queue.append(passenger)

    def remove_passenger(self):
        if self.list_passenger_queue:
            return self.list_passenger_queue.pop(0)
        
        return None

    def show_queue(self):
        return list(self.list_passenger_queue)

class RouteHistory:
    def __init__(self):
        self.list_stack = []

    def push(self, stopNode: BusStopNode):
        self.list_stack.append(stopNode)

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

class BusJiStation:
    def __init__(self):
        self.routes = {}
        self.route_tree = RouteTreeNode("BusJi Station")
        self.history = RouteHistory()

    def add_route(self, route_name, stops):
        if route_name in self.routes:
            return False
        route_node = RouteTreeNode(route_name)
        self.route_tree.add_child(route_node)
        stop_nodes = []
        for stop_name in stops:
            stop = BusStopNode(stop_name)
            stop_nodes.append(stop)
            route_node.add_child(RouteTreeNode(stop_name))
        self.routes[route_name] = stop_nodes
        return True

    def show_route(self, route_name):
        if route_name not in self.routes:
            return None
        return [stop.name for stop in self.routes[route_name]]

    def add_passenger(self, passenger, stop_name):
        for stops in self.routes.values():
            for stop in stops:
                if stop.name == stop_name:
                    stop.add_passenger(passenger)
                    return True
        return False

    def move_bus(self, route_name):
        if route_name not in self.routes:
            return False
        for stop in self.routes[route_name]:
            while stop.list_passenger_queue:
                passenger = stop.remove_passenger()
            self.history.push(stop.name)
        return True

    def reverse_route(self, route_name):
        if route_name not in self.routes:
            return False

        reversed_stops = list(reversed(self.history.list_stack))
        self.history.list_stack.clear()  # Clear history after reversing

        if reversed_stops:
            self.routes[route_name] = [BusStopNode(name) for name in reversed_stops]
        return True

    def show_all_routes(self):
        result = ""
        for route_name, stops in self.routes.items():
            result += f"Route: {route_name}\n"
            for i, stop in enumerate(stops):
                result += f"o {stop.name}\n"
                if i < len(stops) - 1:
                    result += "|\n"
            result += "\n"
        return result

    def find_routes_by_stop(self, stop_name):
        routes = []
        for name, stops in self.routes.items():
            if any(stop.name == stop_name for stop in stops):
                routes.append(name)
        return routes

    def show_passengers(self, stop_name):
        for stops in self.routes.values():
            for stop in stops:
                if stop.name == stop_name:
                    return stop.show_queue()
        return None

    def auto_generate_route(self):
        import random
        stops = ["Lat Krabang", "KMITL Central Library", "KMITL Faculty of Engineering", "KMITL Faculty of Science", "KMITL Faculty of IT", "KMITL Dormitory"]
        random_stops = random.sample(stops, random.randint(3, 6))
        route_name = f"Auto_{len(self.routes) + 1}"
        self.add_route(route_name, random_stops)
        return route_name