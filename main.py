"""
program do wynaczania trasy kanalizacji podposadzkowej, oblicza zagłębienie długość tras,
punkt wyjscia KS musi znajduje się na osi x,
sprawdza czy dane z csv są prawidłowe (mieszczą się w obrysie budynku)

jak dalej można rozbudować program:
 - jedno wpięcie w węźle
 - wpięcia tylko pod kątem 45 st
- mam powielone liczenie trasy bo jest w klasie punkt i pipeline

Program ćwiczony na .csv
15, 10, dlugosc i szerokosc budynku
x, y
8, 0, wyjście z budynku musi być (x, 0)
10, 9
1, 5
3, 8
7, 4
1, 7
"""

from points import Point
from pipeline import find_route, zaglebienie, length_route
from drawing import draw_points, draw_coordinates, draw_building, offset

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

#sprawdzenie - czy podane dane są prawidłowe: (wyjscie z budynku y=0!
if x > 0 and y > 0 and all_points[0].y == 0:
    print("Wymiary budynku i pkt wyjścia kanalizacji sanitarnej podane prawidłowo")
for i in all_points:
    if i.x <= x and i.y <= y:
        pass
    else:
        raise ValueError("Nieprawidłowe dane w pliku csv. Proszę podać prawidłowe dane")
print("Punkty wpięcia kanalizacji sanitarnej podane prawidłowo")

last_point = all_points[0]

#najdalej położony punkt
first_route = []
start_point = None

# utworzenie słownika { punkt_startowy : trasa }
all_routes_obj = {}
all_routes_str = {}

#znajduje trasę od najdalszego punktu
for the_point in all_points[1:]:
    route = find_route(the_point, last_point, x, y)
    if route and len(route) > len(first_route):
        first_route = route
        start_point = the_point
        print(f"Najdluzsza trasa zaczyna się w punkcie {start_point.x, start_point.y}")
        longest_length = length_route(first_route)
        print(f'długość najdłuższej trasy {longest_length}')
        print(f"punkty na najdłuższej trasie:")
        for i in first_route:
            print(i.x, i.y)

#zapisanie najdluzszej trasy (first_route) do slownika ze wszystkimi trasami
all_routes_obj[(start_point)] = [point for point in first_route]
all_routes_str[(start_point.x, start_point.y)] = [(point.x, point.y) for point in first_route]
print(all_routes_obj)
print(all_routes_str)


# tyczenie tras dla pozostałych punktów
lista_tras = []
for the_point in all_points[1:]:
    if the_point == start_point:
        continue

    other_route = first_route.copy()[:-1]

    for some_point in first_route[:-1]:
        route = find_route(the_point, some_point, x, y )
        route_to_last = find_route(the_point, start_point, x, y)
        if route and len(route) < len(other_route) and route[-1].y <= route[-2].y:
            #warunek włączenia nie pod górę jeśli punkt koncowy jest na osi x (y=0)
            other_route = route

    # zapisanie do slownika z trasami
    all_routes_obj[(the_point)] = [other_route]
    all_routes_str[(the_point.x, the_point.y)] = [(point.x, point.y) for point in other_route]

    #rysowanie innych tras (w petli żeby była każda)
    draw_points(other_route, to_center, scale)


#zapisanie danych dla wszystkich tras jako obiekty
with open("trasy.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file)
    for point_key, route in all_routes_obj.items():
        csv_writer.writerow([point_key, route])

#zapisanie danych dla wszystkich tras jako string
    with open("trasy_str.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Punkt Startowy", "Trasa"])
        for point_key, route in all_routes_str.items():
            csv_writer.writerow([point_key, route])


#usuwanie powielonych kawalkow tras
nowy_dict = {}
for k, i in all_routes_str.items():
    for g, j in all_routes_str.items():
        if i != j and len(i) >= len(j):
            while j[-1] in i and j[-2] in i:
                del j[-1]
                nowy_dict[g] = j
        else:
            nowy_dict[g] = j

# ilość mb rur do zamówienia
pipe_lenght = 0
for i in nowy_dict.values():
    pipe_lenght += len(i)-1
print(f" Długość rurociągów: {pipe_lenght} mb")



# for point_key, route in all_routes_str.items():
longest_route = []
#sprawdzenie czy najdłuższa trasa nadal jest najdłuższa
for i in nowy_dict.values():
    for j in nowy_dict.values():
        if i != j:
            end_point_i = i[-1]
            index_end_point_j = j.index(end_point_i) if end_point_i in j else None

            if index_end_point_j is not None:
                print(index_end_point_j)
                longest_route_len = (len(j) - index_end_point_j - 1 + len(i) - 1)
                if len(first_route) < longest_route_len:
                    longest_route = i[:-1] + j[index_end_point_j:]

longest_route_len = len(longest_route)
print(f"Najdłuższa trasa{longest_route}")
print(f"Długość tej trasy: {longest_route_len}")
przeglebienie = zaglebienie(longest_route_len)
print(f"Punkt wyjścia z budynku obniżony o {przeglebienie}m względem dna pierwszego punktu")

#jeszcze raz - zapisanie danych dla wszystkich tras jako string
with open("trasy_str.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Punkt Startowy", "Trasa"])
    for point_key, route in nowy_dict.items():
        csv_writer.writerow([point_key, route])
    csv_writer.writerow(["Najdluzsza trasa"])
    csv_writer.writerow([longest_route])

    # Dodaj informacje o długości trasy
    csv_writer.writerow(["Dlugosc trasy"])
    csv_writer.writerow([longest_route_len])

    # Dodaj informacje o przegłębieniu
    csv_writer.writerow(["Przeglebienie"])
    csv_writer.writerow([przeglebienie])

# rysowanie schematu tras
draw_building(x, y, scale)
draw_points(first_route, to_center, scale) #tutaj ta trasa juz nie jest najdluzsza, tylko pierwsza
draw_coordinates(all_points, to_center, scale)

turtle.exitonclick()