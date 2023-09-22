"""
wyznaczanie punktów znajdujących się na najkrótszej trasie między punktem początkowym a końcowym
algorytm A*
(uproszczenie - koszt każdego ruchu = 1)
"""

import heapq
from points import Point


def find_route(the_point, last_point):
    open_list = [(0, the_point)]  # punkty do sprawdzenia
    closed_list = set()  # zbiór punktów sprawdzonych
    previous = {}  # dict z poprzednikami w ścieżce
    costs = {the_point: 0}  # dict z kosztami dotarcia do punktu

    while open_list:
        cost, current_point = heapq.heappop(open_list)

        if current_point == last_point:
            route = [last_point]
            while route[-1] != the_point:
                route.append(previous[route[-1]])
            route.reverse()
            return route

        if current_point in closed_list:
            continue

        closed_list.add(current_point)

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                x, y = current_point.x, current_point.y
                nx, ny = x + dx, y + dy

                if 0 <= nx < 10 and 0 <= ny < 10:
                    neighbor = Point(nx, ny)
                    new_cost = costs[current_point] + 1

                    if neighbor not in costs or new_cost < costs[neighbor]:
                        costs[neighbor] = new_cost
                        priority = new_cost + neighbor.distance(last_point)
                        previous[neighbor] = current_point
                        heapq.heappush(open_list, (priority, neighbor))

    return None





