import pygame
import globals

def update_controls(new_controls):
    globals.controls_players = new_controls

def change_key(player_index, control_name, new_key):
    """
    Обновляет конкретное свойство управления (например, "explosion_key") для игрока с индексом player_index.
    """
    try:
        globals.controls_players[player_index][control_name] = new_key
    except (IndexError, KeyError):
        print("Неверный индекс игрока или имя управления.")

# Пример использования: обновляем настройки управления
if __name__ == '__main__':
    new_mapping = [
        {
            "to_left_key": pygame.K_q, 
            "to_right_key": pygame.K_e, 
            "to_up_key": pygame.K_z, 
            "to_down_key": pygame.K_c, 
            "explosion_key": pygame.K_p
        },
        {
            "to_left_key": pygame.K_LEFT, 
            "to_right_key": pygame.K_RIGHT, 
            "to_up_key": pygame.K_UP, 
            "to_down_key": pygame.K_DOWN, 
            "explosion_key": pygame.K_RETURN
        }
    ]
    update_controls(new_mapping)
    print("Новые настройки управления применены:", globals.controls_players)
    print("Настройки до изменения:", globals.controls_players)
    change_key(1, "explosion_key", pygame.K_m)
    print("Настройки после изменения:", globals.controls_players)
