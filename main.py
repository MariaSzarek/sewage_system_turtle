from points import Point
from pipeline import find_route
from drawing import draw_points, coordinates, draw_building, offset

import csv
import turtle

scale = 30
x=0
y=0

#odczytanie pliku (wymiary budynku i punkty wpięcia kanalizacji sanitarnej)

with open("points.csv", "r") as file:
    reader = csv.reader(file)
    dimension = next(reader)
    next(reader)
    all_points = [Point(int(i[0]), int(i[1])) for i in reader]
    x = int(dimension[0])
    y = int(dimension[1])
    to_center = offset(x, y, scale)


last_point = all_points[0]

#najdalej położony punkt
longest_route = []
start_point = None


#znajduje trasę od najdalszego punktu
for the_point in all_points[1:]:
    route = find_route(the_point, last_point, x, y)
    if route and len(route) > len(longest_route):
        longest_route = route
        start_point = the_point
        print(f"Najdluzsza trasa zaczyna się w punkcie {start_point.x, start_point.y}")

        for i in longest_route:
            print(i.x, i.y)

# # tu wytycza trasy ze wszystkich punktów / to jest zbyt proste, chociaż na łądnym przykladzie dobrze wyglaa
# for the_point in all_points[1:]:
#     other_route = find_route(the_point, last_point)
#     draw_points(other_route, to_center, scale)


# # a tutaj bedzie wyznaczanie najkrotszej trasy ze wszystkich pozostałych punktów
traski = []

i = 1
while i < len(all_points):
    shortest_route = longest_route.copy()

    for the_point in longest_route[:-1]:
        route = find_route(the_point, all_points[i], x, y)
        if route and len(route) < len(shortest_route):
            shortest_route = route
            punkt_wpiecia = the_point
            print(f'punkt wpiecia {punkt_wpiecia.x, punkt_wpiecia.y}')

    #traski.append(shortest_route)
    traski.append((punkt_wpiecia, shortest_route))

    for n, m in traski:
        draw_points(m, to_center, scale)
    i += 1








if start_point:
    print("Najkrótsza trasa od {} do {}:".format(start_point, last_point))
    for punkt in longest_route:
        print("({}, {})".format(punkt.x, punkt.y))
else:
    print("Nie można znaleźć trasy od żadnego z punktów startowych do {}.".format(last_point))



draw_building(x, y, scale)
draw_points(longest_route, to_center, scale)
coordinates(all_points, to_center, scale)
turtle.exitonclick()