class BusStopNode:
    def __init__(self, name, next, list_passenger_queue=None):
        self.__name = name
        self.__next = next
        self.__list_passenger_queue = [] if not list_passenger_queue else list_passenger_queue
    
    def add_passenger(self, passenger_queue):
        self.__list_passenger_queue.append(passenger_queue)
    
    def remove_passenger(self, passenger_queue):
        pass

    def show_queue(self):
        print(self.__list_passenger_queue)

class RouteHistory:
    def __init__(self, list_stack=None):
        self.__list_stack = [] if not list_stack else list_stack

    def push(self):
        pass

    def pop(self):
        pass

    def show_history(self):
        pass

class RouteTreeNode:
    def __init__(self, name, children):
        self.__name = name

    def add_child(self):
        pass

    def find(self):
        pass

    def show_tree(self):
        pass

class BusJiStation:
    def __init__(self):
        self.__routes = []
        self.__route_tree = []
        self.__history = []

    def add_route():
        pass

    def show_route():
        pass
    
    def add_passenger():
        pass

    def move_bus():
        pass

    def reverse_route():
        pass

    def show_all_routes():
        pass