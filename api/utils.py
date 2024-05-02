from decimal import Decimal


# Algoritmo Ray casting
def ray_casting_algorithm(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]

    for i in range(n + 1):
        p2x, p2y = polygon[i % n]

        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_intersect = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= x_intersect:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


# Bordes
def point_inside_polygon(point, polygon):
    x, y = point
    n = len(polygon)

    for i in range(n):
        if x == polygon[i][0] and y == polygon[i][1]:
            return True

    return ray_casting_algorithm(point, polygon)


univalle = [
    [Decimal('-76.537502'), Decimal('3.380173')],
    [Decimal('-76.537022'), Decimal('3.371275')],
    [Decimal('-76.529775'), Decimal('3.367670')],
    [Decimal('-76.529068'), Decimal('3.379543')],
    [Decimal('-76.537502'), Decimal('3.380173')],
]


# Cálculo de la distancia entre dos puntos:
# raiz( (x2-x1)^2 + (y2-y1)^2 )
def distance(A, B):
    x_distance = (Decimal(f'{B[0]}') - Decimal(f'{A[0]}')) ** 2
    y_distance = (Decimal(f'{B[1]}') - Decimal(f'{A[1]}')) ** 2
    suma = x_distance + y_distance
    distance = Decimal(f'{(suma.sqrt())}')
    return distance
