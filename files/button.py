import pygame

#defining button class
class Button():
    def __init__(self, x, y, image, scale):
        """
        Initizalizes the Button class

        Args:
            x (int): Represents the x-coordinate
            y (int): Represents the y-coordinate
            image (str): Represents the file name of the button iamge
            scale (int): What to scale the image by

        Returns:
            none

   
        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
    
    def draw(self, surface):
        """
        Draws the button object onto the screen

        Args:
            surface: Where to draw the button on

        Returns:
            none

   
        """
        
        action = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return action