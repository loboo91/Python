import pygame, resources

class Hud():
    def __init__(self, avatar_path, avatar2_path, WINDOW_SIZE, _score):
        self.res         = resources.Resources()
        self.surface_hud = pygame.Surface(WINDOW_SIZE)
        
        self.label_p1  = self.res.font_medium.render( 'PLAYER 1', 0, self.res.WHITE, None ) 
        self.label_p2  = self.res.font_medium.render( 'PLAYER 2', 0, self.res.WHITE, None )
        self.score_p1  = self.res.font_small.render( 'points: ' + (str)(_score[0]), 0, self.res.GREY_LIGHT, None )
        self.score_p2  = self.res.font_small.render( 'points: ' + (str)(_score[1]), 0, self.res.GREY_LIGHT, None )
        self.avatar_p1  =  pygame.image.load( avatar_path  ).convert()
        self.avatar_p2  =  pygame.image.load( avatar2_path ).convert()


    def update(self, tab_players):
        self.surface_hud.fill( self.res.GREY_DARK )
        
        self.surface_hud.blit( self.avatar_p1, ( 15,   10 ) )
        self.surface_hud.blit( self.label_p1,  ( 85,   8  ) )
        self.surface_hud.blit( self.avatar_p2, ( 1085, 10 ) )
        self.surface_hud.blit( self.label_p1,  ( 1155, 8  ) )
        self.surface_hud.blit( self.score_p1,  ( 85,   33 ) )        
        self.surface_hud.blit( self.score_p2,  ( 1155, 33 ) )        
        
        for i in range (2):
            pygame.draw.rect( self.surface_hud, self.res.GREY_DARK2, ( 15+1070*i, 80,  185, 33 ) )
            pygame.draw.rect( self.surface_hud, self.res.GREY_DARK2, ( 15+1070*i, 120, 185, 33 ) )
            pygame.draw.rect( self.surface_hud, self.res.GREY_DARK2, ( 15+1070*i, 160, 185, 33 ) )

            self.surface_hud.blit( self.res.icon_speed,  ( 20+1070*i, 81  ) )
            self.surface_hud.blit( self.res.icon_fire,   ( 20+1070*i, 121 ) )
            self.surface_hud.blit( self.res.icon_bomb,   ( 20+1070*i, 161 ) )

        for i, player in enumerate( tab_players ):
            pygame.draw.rect( self.surface_hud, self.res.GREY2, (55+1070*i, 84,  12 * ( ( player.max_speed-0.99 ) * 10 ) +7 , 25 ) )
            pygame.draw.rect( self.surface_hud, self.res.GREY2, (55+1070*i, 124, 6  * player.max_range                   +7 , 25 ) )
            pygame.draw.rect( self.surface_hud, self.res.GREY2, (55+1070*i, 164, 12 * player.max_bombs                   +7 , 25 ) )
        
        for j, player in enumerate( tab_players ):
            for i in range( ( int ) ( ( player.speed - 0.98 ) * 10 ) ):
                pygame.draw.rect( self.surface_hud, self.res.GREEN2, ( 60+1070*j+12*i, 86,  9, 21 ) )
            for i in range( ( int ) ( player.range / 2 ) ):
                pygame.draw.rect( self.surface_hud, self.res.GREEN2, ( 60+1070*j+12*i, 126, 9, 21 ) )
            for i in range( ( int ) ( player.bombs ) ):
                pygame.draw.rect( self.surface_hud, self.res.GREEN2, ( 60+1070*j+12*i, 166, 9, 21 ) )

            if player.buf_immortal: self.surface_hud.blit( self.res.icon_shield, ( 50+1070*j, 40 ) )
        
        return self.surface_hud
