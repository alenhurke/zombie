from league import *
import pygame

class Zombie(Character):

    """This is a sample class for a zombie object.  A zombie
    is a character, is a drawable, and an updateable object.
    This class should handle everything a zombie does, such as
    moving, attacking, collisions, etc.  It was hastily
    written as a demo but should direction.
    """
    
    def __init__(self, player, z = 0, x = 0, y = 0):
    
        super().__init__(z, x, y)
        # This unit's health
        self.health = 100
        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()
        # A unit-less value.  Bigger is faster.
        self.delta = 512
        # Where the player is positioned
        self.x = x
        self.y = y
        # The image to use. This will change frequently
        # in an animated Zombie class.
        self.image = pygame.image.load('./assets/zombie_right.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_circle
        self.collisions = []
        # For collision detection, we need to compare our sprite
        # with collideable sprites.  However, we have to remap
        # the collideable sprites coordinates since they change.
        # For performance reasons I created this sprite so we
        # don't have to create more memory each iteration of
        # collision detection.
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()
        # Overlay
        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.overlay = self.font.render(str(self.health) + "        4 lives", True, (0,0,0))
        
        #Zombie uses player object to find x y location on map and go after him
        self.player = player

    def move_left(self, time):

        self.image = pygame.image.load('./assets/zombie_left.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        
        self.collisions = []
        amount = self.delta * time
        try:
            if self.x - amount < 0:
                raise OffScreenLeftException
            else:
                self.x = self.x - amount
                self.update(0)
                while(len(self.collisions) != 0):
                    self.x = self.x + amount
                    self.update(0)
        except:
            pass

    def move_right(self, time):

        self.image = pygame.image.load('./assets/zombie_right.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        
        self.collisions = []
        amount = self.delta * time
        try:
            if self.x + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenRightException
            else:
                self.x = self.x + amount
                self.update(0)
                while(len(self.collisions) != 0):
                    self.x = self.x - amount
                    self.update(0)
        except:
            pass

    def move_up(self, time):

        self.image = pygame.image.load('./assets/zombie_up.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        
        self.collisions = []
        amount = self.delta * time
        try:
            if self.y - amount < 0:
                raise OffScreenTopException
            else:
                self.y = self.y - amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y + amount
                    self.update(0)
                    self.collisions = []
        except:
            pass

    def move_down(self, time):

        self.image = pygame.image.load('./assets/zombie_down.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        
        self.collisions = []
        amount = self.delta * time
        try:
            if self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.y = self.y + amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y - amount
                    self.update(0)
                    self.collisions = []
        except:
            pass

    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        for sprite in self.blocks:
            self.collider.rect.x= sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)

    def ouch(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            self.health = self.health - 10
            self.last_hit = now
            
    # Same thing using only pygame utilities
    def move_towards_player(self, time):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(self.player.x - self.x, self.player.y - self.y)
        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        if dirvect.x > 0:
            return self.move_right(time)
        elif dirvect.x < 0:
            return self.move_left(time)
        #elif dirvect.y = 0:
            #self.move_up(time)
        #elif dirvect.x = -1:
            #self.move_down(time)
            