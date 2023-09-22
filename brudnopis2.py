from points import Point
from pipeline import find_route

import csv
import drawing


#odczytanie punktów
with open("points.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    all_points = [Point(int(i[0]), int(i[1])) for i in reader]

last_point = all_points[0]

#najdalej położony punkt
longest_route = []
start_point = None

# Turtle rysowanie
def rysuj_punkty(punkty, rozmiar=10):
    t = turtle.Turtle()
    t.speed(15)  # Ustaw prędkość żółwika
    t.penup()
    t.goto(punkty[0].x * 30 - 150, punkty[0].y * 30 - 150)
    for punkt in punkty:
        t.pendown()
        t.goto(punkt.x * 30 - 150, punkt.y * 30 - 150)
        t.dot(rozmiar)  # Rozmiar punktu można dostosować


#znajduje trasę od najdalszego punktu
for the_point in all_points[1:]:
    route = find_route(the_point, last_point)
    if route and len(route) > len(longest_route):
        longest_route = route
        start_point = the_point

# # tu wytycza trasy ze wszystkich punktów
# for the_point in all_points[1:]:
#     other_route = find_route(the_point, last_point)
#     rysuj_punkty(other_route)

# DZIAŁA OK tutaj bedzie wyznacznie najkrotszej trasy od jednego z pozostałych punktów

# shortest_route = longest_route
# print(all_points)
# for the_point in longest_route:
#     route = find_route(the_point, all_points[3])
#     if route and len(route) < len(shortest_route):
#         shortest_route = route
#         punkt_wpiecia = the_point

print("to są moje punkty")
for i in all_points:
    print(i.x, i.y)


# # a tutaj bedzie wyznaczanie najkrotszej trasy ze wszystkich pozostałych punktów
traski = []

i = 1
while i < len(all_points):
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
    print("to są traski wydrukowane")
    print(traski)

    i += 1
for i in traski:
    rysuj_punkty(i)


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



rysuj_punkty(longest_route)
turtle.exitonclick()