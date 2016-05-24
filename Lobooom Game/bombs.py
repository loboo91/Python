import pygame, glob

class Bomb():
    def __init__( self, pos_x, pos_y, time, range_bomb, player, window ):
        self.WINDOW    = window
        self.image     = pygame.image.load( "res/misc/bomb/bomb.png" ).convert_alpha()
        
        self.x         = pos_x
        self.y         = pos_y
        self.tab_x     = ( int )( self.x/32 )*32+16
        self.tab_y     = ( int )( self.y/32 )*32+8
        self.rect      = pygame.Rect(self.tab_x , self.tab_y, 32, 32)
        
        self.time      = time
        self.range     = range_bomb
        
        self.player    = player
        self.explosion = False
        self.set       = False
        self.sound = pygame.mixer.Sound('res/sounds/explosion.wav')
        self.sound.set_volume(0.2)
        self.ani            = glob.glob( "res/misc/bomb/bomb*.png" )
        self.ani_speed_init = 11
        self.ani_speed      = self.ani_speed_init
        self.ani_pos        = 0
        self.ani_max        = len( self.ani )-1
        
        self.image = pygame.image.load( self.ani[0] ).convert_alpha()

        
    def update(self):
        self.ani_speed -= 1
        if self.ani_speed < 0:
            self.image      = pygame.image.load( self.ani[ self.ani_pos ] ).convert_alpha()
            self.ani_speed  = self.ani_speed_init

            if self.ani_pos == self.ani_max:
                self.ani_pos  = 0
            else:
                self.ani_pos += 1
                
        self.time -= 1
        if self.time == 10: self.sound.play(0,0,0)
        if self.time < 0:
            self.explosion = True

        self.WINDOW.blit( self.image, ( self.tab_x, self.tab_y-8 ) )
