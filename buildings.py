import pygame 
"""
Initializing Buildings as Buttons
"""
class Building: 
    def __init__(self, name, x, y, width, height, color, hover_color, level=1):
        self.name = name
        self.color = color
        self.hover_color = hover_color
        self.level = level
        self.clicked = False
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, font, mouse_pos):
        # Change color if hovered
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        # Building name & level text
        text = font.render(f"{self.name}", True, (0, 0, 0))
        screen.blit(text, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event, callback=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.clicked = True
                if callback:
                    callback(self)  # Run an action (like open popup)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.clicked = False



    def create_buildings():
        buildings = []
        buildings.append(Button("NRV Dorms", 60, 120, 120, 100, (173, 216, 230), (0, 255, 0)))
        buildings.append(Button("Leutner",100, 65, 80, 50, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Wyant", 250, 65, 50, 40, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("DiSanto Field", 250, 125, 50, 40, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("PBL", 100, 300, 80, 70, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Tink", 140, 360, 90, 120, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("KSL", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Ford", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Fribley", 300, 150, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Veale Center", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Rockefellar", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Strosacker", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Millis Schmitt", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Bingham", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Olin", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("White", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Glennan", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Nord", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Sears", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Tomlinson", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("Crawford", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))
        buildings.append(Building("SRV Dorms", 200, 300, 120, 80, (173, 216, 230), (0, 255, 0)))

        return buildings

def add_faculty():
    return 1

def add_students():
    return 1

def upgrade_building():
    return 1

def get_building_name():
    return 1

"""
Main Loop 
"""
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Kaler Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

buildings = create_buildings()

def on_building_click(building):
    print(f"You clicked on {building.name}!")
    # Later: trigger popup or building upgrade here

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for b in buildings:
            b.handle_event(event, callback=on_building_click)

    # Draw background
    screen.fill((230, 230, 255))

    # Draw all building buttons
    for b in buildings:
        b.draw(screen, font, mouse_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
