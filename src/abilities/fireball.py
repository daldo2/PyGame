from src.abilities.ability import Ability
from src.entities.projectile import Projectile

class Fireball(Ability):
    def __init__(self, owner, projectile_list):
        super().__init__(owner, "fireball", cooldown = 0.5, mana_cost = 10)
        self.projectile_list = projectile_list

    def activate(self):
        spawn_y = self.owner.rect.centery - 8

        if self.owner.facing_right:
            spawn_x = self.owner.rect.right
            direction = 1
        else:
            spawn_x = self.owner.rect.left - 16
            direction = -1

        new_fireball = Projectile(spawn_x, spawn_y, direction)
        self.projectile_list.append(new_fireball)
        print("Fireball Cast!")