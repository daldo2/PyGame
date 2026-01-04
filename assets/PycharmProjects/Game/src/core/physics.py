import pygame


def move_and_slide(rect, velocity, tiles, dt):
    """
    Przesuwa prostokąt (rect) o zadaną prędkość (velocity) w czasie (dt),
    rozwiązując kolizje z listą kafelków (tiles).
    """
    collisions = {'top': False, 'bottom': False, 'left': False, 'right': False}

    # 1. Ruch w poziomie (Oś X)
    rect.x += velocity.x * dt

    # Sprawdź kolizję z każdym kafelkiem
    # Tworzymy listę tylko tych kafelków, z którymi faktycznie się zderzyliśmy
    hit_list = [tile for tile in tiles if rect.colliderect(tile)]

    for tile in hit_list:
        if velocity.x > 0:  # Ruch w prawo -> uderzenie lewą stroną ściany
            rect.right = tile.left
            collisions['right'] = True
        elif velocity.x < 0:  # Ruch w lewo -> uderzenie prawą stroną ściany
            rect.left = tile.right
            collisions['left'] = True

    # 2. Ruch w pionie (Oś Y)
    rect.y += velocity.y * dt

    # Sprawdź kolizję ponownie po ruchu w Y
    hit_list = [tile for tile in tiles if rect.colliderect(tile)]

    for tile in hit_list:
        if velocity.y > 0:  # Spadanie w dół -> uderzenie w podłogę
            rect.bottom = tile.top
            collisions['bottom'] = True
        elif velocity.y < 0:  # Skok w górę -> uderzenie w sufit
            rect.top = tile.bottom
            collisions['top'] = True

    return rect, collisions