import pygame

class Supervisor:
    def __init__(self):
        self.alertes = {}
        self.min_vies = 2  # Nombre de vies critiques pour déclencher une alerte
    

    def check_vie(self, joueur, num_joueur):
        if joueur.vies <= self.min_vies and joueur.vies > 0:
           self.alertes[f"Alerte {num_joueur}"] = f"{num_joueur} vie basse ({joueur.vies}) !"
        elif joueur.vies < 1:
            self.alertes[f"Alerte {num_joueur}"] = f"{num_joueur} !! VIE CRITIQUE ({joueur.vies}) !!"
        else:
            self.alertes.pop(num_joueur, None) 
            
    
    def draw_alertes(self, screen, resolution, text_screen_fn):
        if not self.alertes:
            return
        y_base = resolution[1] - 100
        for i, msg in enumerate(self.alertes.values()):
            text_screen_fn(
                msg,
                22,
                pygame.Color(255, 0, 0),
                screen,
                (resolution[0] // 2, y_base + i * 30)
            )
    
    def reset_alertes(self):
        self.alertes.clear()
