import pygame

# Szkielet kazdej umiejetnosci
class Ability:
    def __init__(self, owner, name, cooldown = 1.0, mana_cost = 10):
        self.owner = owner
        self.name = name
        self.cooldown = cooldown
        self.mana_cost = mana_cost
        self.current_cooldown = 0

    def update(self, dt):
        if self.current_cooldown > 0:
            self.current_cooldown -= dt

    def can_cast(self):
        if self.current_cooldown > 0:
            return False

        if hasattr(self.owner, 'current_mp'):
            if self.owner.current_mp < self.mana_cost:
                print("Not enough mana!")
                return False

        return True

    def trigger(self):
        if self.can_cast():
            if hasattr(self.owner, 'current_mp'):
                self.owner.current_mp -= self.mana_cost

            # Start Cooldown
            self.current_cooldown = self.cooldown

            # Execute actual logic
            self.activate()
            print(f"Used {self.name}!")

    def activate(self):
        """Override this in child classes."""
        pass