class BusStopNode:
    def __init__(self, name):
        self.name: str = name
        self.next: BusStopNode = None
        self.list_passenger_queue: list[str] = []

    def add_passenger(self, passenger: str):
        self.list_passenger_queue.append(passenger)

    def remove_passenger(self):
        if self.list_passenger_queue:
            return self.list_passenger_queue.pop(0)

        return None

    def show_queue(self):
        return self.list_passenger_queue

class RouteHistory:
    def __init__(self):
        self.list_stack: list[BusStopNode] = []

    def push(self, stopNode: BusStopNode):
        self.list_stack.append(stopNode)

    def pop(self):
        if self.list_stack:
            return self.list_stack.pop()
        return None

    def show_history(self) -> list[BusStopNode]:
        return self.list_stack

class RouteTreeNode:
    def __init__(self, name):
        self.name: str = name
        self.children: list[RouteTreeNode] = []

    def add_child(self, child):
        self.children.append(child)

    def find(self, target_name: str):
        routes = []

        if target_name.strip() == "":
            return routes

        for route_node in self.children:
            if any(target_name.lower() in stop.name.lower() for stop in route_node.children):
                routes.append(route_node.name)

        return routes

    def show_tree(self, indent=0):
        print("  " * indent + self.name)
        for child in self.children:
            child.show_tree(indent + 1)

class BusJiStation:
    def __init__(self):
        self.routes: dict[str, BusStopNode] = {}
        self.route_tree = RouteTreeNode("BusJi Station")
        self.histories: dict[str, RouteHistory] = {}
        self.current_positions: dict[str, BusStopNode] = {}

    def add_route(self, route_name, bus_stops):
        if route_name in self.routes:
            return False

        if not bus_stops:
            return False

        head = BusStopNode(bus_stops[0])
        current = head

        for stop in bus_stops[1:]:
            current.next = BusStopNode(stop)
            current = current.next

        self.routes[route_name] = head
        self.current_positions[route_name] = head
        self.histories[route_name] = RouteHistory()

        route_node = RouteTreeNode(route_name)
        self.route_tree.add_child(route_node)

        for stop in bus_stops:
            route_node.add_child(RouteTreeNode(stop))

        return True

    def show_route(self, route_name):
        if route_name not in self.routes:
            return []

        stops = []
        current = self.routes[route_name]

        while current:
            stops.append(current.name)
            current = current.next

        return stops

    def add_passenger(self, passenger, stop_name):
        for route_head in self.routes.values():
            current = route_head

            while current:
                if current.name == stop_name:
                    current.add_passenger(passenger)
                    return True
                current = current.next
        
        return False

    def show_queue(self, stop_name):
        for route_head in self.routes.values():
            current = route_head
            
            while current:
                if current.name == stop_name:
                    return current.show_queue()
                current = current.next

        return []

    def move_bus(self):
        moved = False
        new_positions = {}

        for route_name, current in self.current_positions.items():
            if current:
                self.histories[route_name].push(current)
                if current.next:
                    new_positions[route_name] = current.next
                moved = True

        self.current_positions = new_positions

        return moved

    def reverse_route(self):
        pass

    def show_all_routes(self):
        return self._tree_to_string(self.route_tree)

    def _tree_to_string(self, node: RouteTreeNode, indent=0):
        result = "  " * indent + node.name + "\n"

        for child in node.children:
            result += self._tree_to_string(child, indent + 1)

        return result

    def find_routes_by_stop(self, stop_name):
        return self.route_tree.find(stop_name)

    def remove_passenger(self, stop_name):
        for route_head in self.routes.values():
            current = route_head
            while current:
                if current.name == stop_name:
                    return current.remove_passenger()
                current = current.next

        return None

    def show_history(self, route_name):
        if route_name not in self.histories:
            return []
        
        return [stop.name for stop in self.histories[route_name].show_history()]
        
    def get_current_position(self, route_name):
        if route_name not in self.current_positions:
            return None
        
        return self.current_positions[route_name].name