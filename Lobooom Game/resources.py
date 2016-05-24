import pygame

class Resources():
    def __init__(self):
 
        self.WINDOW_SIZE = ( 1280, 720 )
        self.map_types   = [ 'CASTLE', 'ICELAND', 'JUNGLE' ]

        # FONTS
        self.font_small         = pygame.font.Font( "fonts/tt0246m_.ttf", 15 )
        self.font_medium        = pygame.font.Font( "fonts/tt0246m_.ttf", 20 )
        self.font               = pygame.font.Font( "fonts/tt0246m_.ttf", 25 )
        self.font_large         = pygame.font.Font( "fonts/tt0246m_.ttf", 45 )

        # COLORS
        self.WHITE       = ( 255 , 255 , 255 )
        self.BLACK       = ( 0   , 0   , 0   )
        self.GREEN       = ( 0   , 255 , 0   )
        self.GREEN2      = ( 0   , 139 , 0   )
        self.GREEN_OLIVE = ( 85  , 107 , 47  )
        self.GREY_LIGHT  = ( 150 , 150 , 150 )        
        self.GREY        = ( 91  , 91  , 91  )
        self.GREY2       = ( 61  , 61  , 61  )
        self.GREY_DARK2  = ( 42  , 42  , 42  )
        self.GREY_DARK   = ( 22  , 22  , 22  )
        self.RED         = ( 176 , 23  , 31  )
        self.BLUE_LIGHT  = ( 135 , 206 , 250 )
        self.BLUE        = ( 0   , 0   , 139 )
        self.BLUE2       = ( 16  , 78  , 139 )
        self.BROWN       = ( 139 , 69  , 19  )
        
        # TRANSPARENT COLORS
        self.BLACK_A     = ( 0   , 0   , 0   , 100 )
        self.BLACK2_A    = ( 0   , 0   , 0   , 110 )
        self.BLACK3_A    = ( 0   , 0   , 0   , 160 )
        self.GREY_A      = ( 21  , 21  , 21  , 200 )
        self.RED_A       = ( 176 , 23  , 31  , 50 )
        self.BLUE_A      = ( 0   , 0   , 139 , 50 )
        
        # IMAGES
        
        self.icon_bomb  = pygame.image.load( 'res/misc/hud/bomb_icon.png'  ).convert_alpha()
        self.icon_fire  = pygame.image.load( 'res/misc/hud/fire_icon.png'  ).convert_alpha()
        self.icon_speed = pygame.image.load( 'res/misc/hud/speed_icon.png' ).convert_alpha()
        self.icon_shield= pygame.image.load( 'res/misc/hud/shield_icon.png' ).convert_alpha()

        self.menu_bg                    = pygame.image.load( "res/misc/menu_bg.gif"              ).convert()
        self.image_button               = pygame.image.load( "res/misc/button_long.gif"          ).convert()
        self.image_button_active        = pygame.image.load( "res/misc/button_long_active.gif"   ).convert()
        self.image_button_medium        = pygame.image.load( "res/misc/button_medium.gif"        ).convert() 
        self.image_button_medium_active = pygame.image.load( "res/misc/button_medium_active.gif" ).convert()
        self.image_arrow_r              = pygame.image.load( "res/misc/arrow_r.png"              ).convert_alpha()
        self.image_arrow_l              = pygame.image.load( "res/misc/arrow_l.png"              ).convert_alpha()
        self.logo                       = pygame.image.load( "res/misc/logo.png"                 ).convert_alpha()
