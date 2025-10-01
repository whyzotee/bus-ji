import os
import curses

from curses import wrapper
from src.core import BusJiStation

class MenuOption:
    ADD_ROUTE = "Add RoutRoute"
    ADD_PASSENGER = "Add passenger"
    PICKUP_PASSENGER = "Picke"
    SHOW_ROUTE = "Show up passenger"
    SEARCH_ROUTE = "Search Route"
    SHOW_ALL_ROUTES = "Show all routes"

class App():
    def __init__(self):
        self.bus_station = BusJiStation()
        self.menu = [
            MenuOption.ADD_ROUTE,
            MenuOption.SHOW_ROUTE,
            MenuOption.ADD_PASSENGER,
            MenuOption.PICKUP_PASSENGER,
            MenuOption.SEARCH_ROUTE,
            MenuOption.SHOW_ALL_ROUTES
        ]
        self.current_selection = 0

    def showMenu(self, stdscr: curses.window) -> None:
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        
        stdscr.keypad(True)

        key = None
        
        while key != ord('q'):
            stdscr.clear()
            stdscr.box()

            if key == curses.KEY_UP and self.current_selection > 0:
                self.current_selection -= 1

            if key == curses.KEY_DOWN and self.current_selection < len(self.menu) - 1:
                self.current_selection += 1

            if key == ord('\n') or key == curses.KEY_ENTER:
                self.handle_selection(stdscr)

            
            stdscr.addstr(0, 2, " Bus Ji Station ", curses.A_BOLD)
            stdscr.addstr(1, 5, """
            .-------------------------------------------------------------.
            '------..-------------..----------..----------..----------..--.|
            |       \\            ||          ||          ||          ||  ||
            |        \\           ||          ||          ||          ||  ||
            |    ..   ||  _    _  ||    _   _ || _    _   ||    _    _||  ||
            |    ||   || //   //  ||   //  // ||//   //   ||   //   //|| /||
            |_.------"''----------''----------''----------''----------''--'|
            |)|      |       |       |       |    |         |      ||==|  |
            | |      |  _-_  |       |       |    |  .-.    |      ||==| C|
            | |  __  |.'.-.' |   _   |   _   |    |.'.-.'.  |  __  | "__=='
            '---------'|( )|'----------------------'|( )|'----------""                          
            """, curses.A_BOLD)
            
            stdscr.addstr(14, 2, " Main Menu ", curses.A_BOLD)
            start_y = 16
            for i in range(len(self.menu)):
                if i == self.current_selection:
                    stdscr.addstr(start_y + i, 2, f"> {self.menu[i]} ", curses.A_REVERSE)
                else:
                    stdscr.addstr(start_y + i, 2, f"  {self.menu[i]} ")

            height, _ = stdscr.getmaxyx()
            stdscr.addstr(height - 1, 2, " '↑↓' Navigate | 'Enter' Select | 'Q' Quit ")

            stdscr.refresh()

            key = stdscr.getch()
        else:
            print("Good bye!")

    def add_route_page(self, stdscr: curses.window):
        route_name = self.get_input(stdscr, "Enter route name: ")
        stops_input = self.get_input(stdscr, "Enter bus stops (comma separated): ")
        stops = [s.strip() for s in stops_input.split(',') if s.strip()]

        stdscr.clear()

        if not route_name or not stops:
            stdscr.addstr(2, 2, "Invalid input.")
            return
            
        success = self.bus_station.add_route(route_name, stops)
        stdscr.addstr(2, 2, f"Route '{route_name}' {"added successfully." if success else " already exists."}")
    
    def show_route_page(self, stdscr: curses.window):
        GREEN = curses.color_pair(1)

        route_name = self.get_input(stdscr, "Enter route name: ")
        stops = self.bus_station.show_route(route_name)
        
        stdscr.clear()

        if not stops:
            stdscr.addstr(2, 2, f"Route '{route_name}' not found.")
            return
            
        key = None

        while key != ord('q'):
            stdscr.clear()
            stdscr.box()
            height, _ = stdscr.getmaxyx()
            position = self.bus_station.get_current_position(route_name)
            route_str = f"Route '{route_name}' (Bus position: {position}):"
            stdscr.addstr(2, 2, route_str)

            y = 4
            visited = set(stop.name for stop in self.bus_station.histories[route_name].show_history())

            for i in range(len(stops)):
                if stops[i] in visited:
                    stdscr.addstr(y, 4, f"o {stops[i]}", GREEN)
                    y += 1
                    if i < len(stops) - 1:
                        stdscr.addstr(y, 4, "|", GREEN)
                        y += 1
                        stdscr.addstr(y, 4, "|", GREEN)
                        y += 1
                    continue

                if stops[i] == position:
                    stdscr.addstr(y, 4, f"o {stops[i]}", GREEN)
                else:
                    stdscr.addstr(y, 4, f"o {stops[i]}")

                y += 1
                if i < len(stops) - 1:
                    stdscr.addstr(y, 4, "|")
                    y += 1
                    stdscr.addstr(y, 4, "|")
                    y += 1

            stdscr.addstr(height - 1, 2, " 'M' Move bus | 'Q' Quit ")

            stdscr.refresh()

            key = stdscr.getch()
              
            if key in (ord('m'), ord('M')):
                current_pos = self.bus_station.current_positions.get(route_name)
                if current_pos and current_pos.next:
                    self.bus_station.current_positions[route_name] = current_pos.next
                    self.bus_station.histories[route_name].push(current_pos)
                else:
                    stdscr.addstr(height-3, 2, "Bus reached end of route!")
                    stdscr.refresh()
                    curses.napms(1000)
        else:
            return stdscr.clear()
    
    def add_passenger_page(self, stdscr: curses.window):
        passenger = self.get_input(stdscr, "Enter passenger name: ")
        stop_name = self.get_input(stdscr, "Enter bus stop name: ")
        success = self.bus_station.add_passenger(passenger, stop_name)

        if success:
            stdscr.addstr(2, 2, f"Adding '{passenger}' to '{stop_name}' success.")
        else:
            stdscr.addstr(2, 2, f"Bus Stop '{stop_name}' not found.")
    
    def pickup_passenger_page(self, stdscr: curses.window):
        stop_name = self.get_input(stdscr, "Enter bus stop name: ")
        passenger = self.bus_station.remove_passenger(stop_name)

        stdscr.clear()
        
        if passenger:
            stdscr.addstr(2, 2, f"Picked up passenger '{passenger}' from '{stop_name}'.")
        else:
            stdscr.addstr(2, 2, f"No passengers at '{stop_name}'.")

    def search_route_page(self, stdscr: curses.window):
        stop_name = self.get_input(stdscr, "Enter bus bus stop name: ")
        routes = self.bus_station.find_routes_by_stop(stop_name)

        stdscr.clear()

        if not routes:
            stdscr.addstr(2, 2, f"No routes found for stop '{stop_name}'.")
            return
            
        stdscr.addstr(2, 2, f"Routes containing '{stop_name}':")
        y = 4
        for route in routes:
            stdscr.addstr(y, 4, f"- {route}:")
            y += 1
            stops = self.bus_station.show_route(route)
            for stop in stops:
                stdscr.addstr(y, 6, f"o {stop}")
                y += 1
            y += 1

    def handle_selection(self, stdscr: curses.window) -> None:
        option = self.menu[self.current_selection]
        self.perform_action(stdscr, "", option)

    def get_input(self, stdscr: curses.window, prompt: str) -> str:
        stdscr.clear()
        stdscr.box()

        curses.echo()
        stdscr.addstr(2, 2, prompt)
        input_str = stdscr.getstr().decode('utf-8')
        curses.noecho()
        return input_str

    def perform_action(self, stdscr: curses.window, category: str, option: str) -> None:
        stdscr.clear()
        stdscr.box()

        if option == MenuOption.ADD_ROUTE:
            self.add_route_page(stdscr)
        
        if option == MenuOption.SHOW_ROUTE:
            self.show_route_page(stdscr)

        if option == MenuOption.ADD_PASSENGER:
            self.add_passenger_page(stdscr)
        
        if option == MenuOption.PICKUP_PASSENGER:
            self.pickup_passenger_page(stdscr)

        if option == MenuOption.SEARCH_ROUTE:
            self.search_route_page(stdscr)

        if option == MenuOption.SHOW_ALL_ROUTES:
            routes = self.bus_station.show_all_routes()
            stdscr.addstr(2, 2, routes if routes else "No routes available.")
        
        height, _ = stdscr.getmaxyx()

        stdscr.addstr(height - 1, 2, " Press any key to continue ")
        stdscr.getch()
        stdscr.clear()

    def generate_route(self):
        simple = [
            "Lat Krabang", 
            "KMITL Central Library", 
            "KMITL Faculty of Engineering", 
            "KMITL Faculty of Science", 
            "KMITL Faculty of IT", 
            "KMITL Dormitory"
        ]

        self.bus_station.add_route("R001", simple)
        simple.reverse()
        self.bus_station.add_route("R002", simple)

    def run(self):
        self.generate_route()
        wrapper(self.showMenu)

if __name__ == "__main__":
    os.system('color')
    os.system('clear')

    app = App()
    app.run()