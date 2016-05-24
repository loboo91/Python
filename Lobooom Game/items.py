import pygame, random

class Chest():
    def __init__( self, pos_x, pos_y, center_map_x, center_map_y, path, window ):
        self.WINDOW = window
        
        choice = random.randint(1,4)
        if   choice == 1: self.image = pygame.image.load( path + "chest.gif"  ).convert()
        elif choice == 2: self.image = pygame.image.load( path + "chest2.gif" ).convert()
        else:             self.image = pygame.image.load( path + "chest1.gif" ).convert()
            
        self.x      = ( int ) ( pos_x )*32 + center_map_x
        self.y      = ( int ) ( pos_y )*32 + center_map_y
        self.tab_x  = pos_x
        self.tab_y  = pos_y
        
        self.rect   = pygame.Rect( self.x, self.y, 32, 32 )
        
    def update( self ):
        self.WINDOW.blit( self.image, ( self.x, self.y ) )


class Extras():
    def __init__( self, pos_x, pos_y, window ):
        self.WINDOW     = window
        self.x          = pos_x
        self.y          = pos_y
        self.rect       = pygame.Rect( self.x, self.y, 30, 30 )
        self.image      = pygame.image.load( "res/extras/fire.png" ).convert()
        self.choice     = random.randint(0,100)
        self.time_spawn = 50
        
    def update( self ):
        if not self.time_spawn==0:
            self.time_spawn-=1
            
        if   0 <= self.choice <= 29:
            self.image = pygame.image.load( "res/extras/fire.png"       ).convert_alpha()
            
        elif 30 <= self.choice <= 59:
            self.image = pygame.image.load( "res/extras/speed.png"       ).convert_alpha()
            
        elif 60 <= self.choice <= 84:
            self.image = pygame.image.load( "res/extras/bomb.png"        ).convert_alpha()
            
        elif 85 <= self.choice <= 89:
            self.image = pygame.image.load( "res/extras/immortality.png" ).convert_alpha()
            
        elif 90 <= self.choice < 100:
            self.image = pygame.image.load( "res/extras/death.png"       ).convert_alpha()
            
        self.WINDOW.blit( self.image, ( self.x,self.y+1 ) )
