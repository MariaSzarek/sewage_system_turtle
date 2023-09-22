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
    route = find_route(the_point, last_point)
    if route and len(route) > len(longest_route):
        longest_route = route
        start_point = the_point
        print(f"Najdluzsza trasa zaczyna się w punkcie {start_point.x, start_point.y}")

# tu wytycza trasy ze wszystkich punktów
for the_point in all_points[1:]:
    other_route = find_route(the_point, last_point)
    draw_points(other_route, to_center, scale)

# DZIAŁA OK tutaj bedzie wyznacznie najkrotszej trasy od jednego z pozostałych punktów

# shortest_route = longest_route
# print(all_points)
# for the_point in longest_route:
#     route = find_route(the_point, all_points[3])
#     if route and len(route) < len(shortest_route):
#         shortest_route = route
#         punkt_wpiecia = the_point


# # a tutaj bedzie wyznaczanie najkrotszej trasy ze wszystkich pozostałych punktów
traski = []

i = 1
print(f"ilosc wszystkich ppunktow {len(all_points)}")
while i < len(all_points):
    print(f"to jest petla nr {i}")
    shortest_route = longest_route.copy()

    for the_point in longest_route:
        print(f"to jest {the_point.x, the_point.y}")
        route = find_route(the_point, all_points[i])
        if route and len(route) < len(shortest_route):
            shortest_route = route
            print("typ shortest_rouute")
            print(type(shortest_route))
            punkt_wpiecia = the_point
            print(f'punkt wpiecia {punkt_wpiecia.x, punkt_wpiecia.y}')

    traski.append(shortest_route)
    for m in traski:
        # draw_points(m, to_center, scale)
        pass
    i += 1

#tutaj rysuje trasy do wszystkich punktów z trasy
# for the_point in longest_route:
#     for rest_point in all_points[1:]:
#         dif_route = find_route(the_point, rest_point)
#         if dif_route:
#             rysuj_punkty(dif_route)
#
# for punkt in dif_route:
#     print("({}, {})".format(punkt.x, punkt.y))

#a tutaj ma narysować tylko najkrótszą możliwą trasę
# shortest_route = []
# for the_point in longest_route:
#     for rest_point in all_points[1:]:
#         dif_route = find_route(the_point, rest_point)
#         if dif_route and len(dif_route) < len(shortest_route):
#             shortest_route = dif_route
# #            start_point = the_point
# rysuj_punkty(dif_route)
# for punkt in dif_route:
#     print("({}, {})".format(punkt.x, punkt.y))



if start_point:
    print("Najkrótsza trasa od {} do {}:".format(start_point, last_point))
    for punkt in longest_route:
        print("({}, {})".format(punkt.x, punkt.y))
else:
    print("Nie można znaleźć trasy od żadnego z punktów startowych do {}.".format(last_point))



draw_building(x, y, scale)
#draw_points(longest_route, to_center, scale)
coordinates(all_points, to_center, scale)
turtle.exitonclick()