import pygame, mapson, configparser, glob, resources
from pygame.locals import *
from sys import exit

class Menu(object):
    def __init__(self, TILE_SIZE, WINDOW_SIZE, WINDOW):
        pygame.init()
        pygame.mouse.set_visible( 1 )

        self.WINDOW             = WINDOW
        self.WINDOW_SIZE        = WINDOW_SIZE
        
        self.level              = mapson.Level(TILE_SIZE)
        self.res                = resources.Resources()
        self.clock              = pygame.time.Clock()
        self.Parser             = configparser.ConfigParser()

        self.WINDOW_SIZE = WINDOW_SIZE
        self.level.readFromTxt('lvl_1.txt')

        self.surface_mini_map   = self.level.drawMiniMap( 0, 0, None )
        self.surface_menu       = pygame.Surface((self.res.WINDOW_SIZE))
        self.surface_shadow     = pygame.Surface((self.res.WINDOW_SIZE), pygame.SRCALPHA)

        self.mm_x               = self.WINDOW_SIZE[0]/2-28*15/2
        self.mm_y               = self.WINDOW_SIZE[1]/2-23*15
        
        self.mm_index           = 0
        self.mm_type_index      = 0
        self.tab_keys           = []

        self.menu_click   = pygame.mixer.Sound('res/sounds/menu_key.wav')
        
        self.Parser.read('config.ini')
        self.options            = self.Parser.options( 'config' )
        
        for option in self.options:
            self.tab_keys.append( self.Parser.get( "config", option ))

        self.surface_shadow.fill( self.res.GREY_A )
        
        
    def startMenu(self):
        pygame.mouse.set_visible( 1 )
        self.surface_menu.blit( self.res.menu_bg, (0,0) )
        
        tab_labels  = []
        tab_buttons = []
        
        tab_labels.append( self.res.font.render('NEW GAME', 0, self.res.WHITE, None ))
        tab_labels.append( self.res.font.render('OPTIONS' , 0, self.res.WHITE, None ))
        tab_labels.append( self.res.font.render('CREDITS' , 0, self.res.WHITE, None ))
        tab_labels.append( self.res.font.render('EXIT'    , 0, self.res.WHITE, None ))

        for i in range(4):
            tab_buttons.append( pygame.Rect(( self.WINDOW_SIZE[0]/2-210, self.WINDOW_SIZE[1]/2+15+60*i, 406, 50 )))

        for i in range(4):
            self.surface_menu.blit( self.res.image_button, ( self.WINDOW_SIZE[0]/2-210, self.WINDOW_SIZE[1]/2+15+60*i ))
            
        for i in range(4):
            self.surface_menu.blit( tab_labels[i], ( self.WINDOW_SIZE[0]/2-180, self.WINDOW_SIZE[1]/2+24+60*i ))
        
        while True:
            for event in pygame.event.get():

                if event.type == MOUSEMOTION:
                    for i, button in enumerate( tab_buttons ):
                        
                        if button.collidepoint( pygame.mouse.get_pos() ):
                            self.surface_menu.blit( self.res.image_button_active, ( self.WINDOW_SIZE[0]/2-210, self.WINDOW_SIZE[1]/2+15+60*i ) )
                            self.surface_menu.blit( tab_labels[i],                ( self.WINDOW_SIZE[0]/2-180, self.WINDOW_SIZE[1]/2+24+60*i ) )                        
                        else:
                            self.surface_menu.blit( self.res.image_button,        ( self.WINDOW_SIZE[0]/2-210, self.WINDOW_SIZE[1]/2+15+60*i ) )
                            self.surface_menu.blit( tab_labels[i],                ( self.WINDOW_SIZE[0]/2-180, self.WINDOW_SIZE[1]/2+24+60*i ) )
        
                            
                if event.type == MOUSEBUTTONDOWN:
                    for i, button in enumerate( tab_buttons ):
                        if button.collidepoint(pygame.mouse.get_pos()):
                            self.menu_click.play()
                            if i<=2 : return i+1
                            else    : self._quit_()
                                      
            self.WINDOW.blit(self.surface_menu, (0,0))  
            pygame.display.flip()

            
    def optionsMenu(self):
        pygame.mouse.set_visible( 1 )
        self.surface_menu.fill(self.res.GREY)
        self.surface_menu.blit( self.surface_shadow, ( 0, 0 ) )

        labels_players_keys = []
        tab_buttons         = []
        labels_keys         = []
        
        label_p1 = self.res.font.render( 'PLAYER 1', 0, self.res.WHITE, None )
        label_p2 = self.res.font.render( 'PLAYER 2', 0, self.res.WHITE, None )
        
        labels_keys.append( self.res.font.render( 'MOVE UP'   , 0, self.res.WHITE, None ) )
        labels_keys.append( self.res.font.render( 'MOVE DOWN' , 0, self.res.WHITE, None ) )
        labels_keys.append( self.res.font.render( 'MOVE LEFT' , 0, self.res.WHITE, None ) )
        labels_keys.append( self.res.font.render( 'MOVE RIGHT', 0, self.res.WHITE, None ) )
        labels_keys.append( self.res.font.render( 'USE'       , 0, self.res.WHITE, None ) )

        self.surface_menu.blit( label_p1,  ( 750 , 80 ) )
        self.surface_menu.blit( label_p2,  ( 1025, 80 ) )

        for j in range (2):
            for i in range(5):
                labels_players_keys.append( self.res.font.render ( pygame.key.name( (int)( self.tab_keys[i+j*5] ) ), 0, self.res.WHITE, None ) )   

        for j in range(2):
            for i in range(5):
                tab_buttons.append( pygame.Rect ( 675+j*275, 160+i*60, 280, 50) )
                   
        for i in range(5):
            self.surface_menu.blit( labels_keys[i], ( 450, 160+60*i ) )

        for j in range (2):
            for i in range(5):
                self.surface_menu.blit( self.res.image_button_medium, ( 650+j*300, 150+i*60 ) )
                
        for j in range(2):
            for i in range(5):
                self.surface_menu.blit( labels_players_keys[i+j*5],   ( 675+300*j, 160+i*60 ) )

        pygame.event.set_blocked(pygame.MOUSEMOTION)
        
        while True:
            for event in pygame.event.get():
                
                if event.type == KEYDOWN and event.key==K_ESCAPE: 
                    file = open( 'config.ini', 'w' )
                    
                    for i, option in enumerate( self.options ):
                        self.Parser.set( 'config', option, ''+(str)( self.tab_keys[i])+'' )
                        
                    self.Parser.write( file )
                    file.close()
            
                    pygame.event.set_allowed( pygame.MOUSEMOTION )
                    return 'back'
                
                j=0
                
                for i, button in enumerate( tab_buttons ):
                    if button.collidepoint( pygame.mouse.get_pos() ) and event.type == MOUSEBUTTONUP:
                            try:
                                self.menu_click.play()
                                if i>4: j=1
                                pygame.mouse.set_visible( 0 )
                                
                                labels_players_keys[i] = self.res.font.render( '_', 0, self.res.WHITE, None )
                                self.surface_menu.blit( self.res.image_button_medium_active,  ( 650+300*j, 150+60*( i%5 ) ) )
                                self.surface_menu.blit( labels_players_keys[i],               ( 675+300*j, 160+60*( i%5 ) ) )
                                    
                                self.WINDOW.blit( self.surface_menu, ( 0, 0 ) )

                                pygame.display.flip()
                                    
                                event = pygame.event.wait()
                                self.tab_keys[i] = event.key
                                         
                                labels_players_keys[i] = self.res.font.render( pygame.key.name( event.key ), 0, self.res.WHITE, None)
                                self.surface_menu.blit( self.res.image_button_medium, ( 650+300*j, 150+60*( i%5 ) ) )
                                self.surface_menu.blit( labels_players_keys[i],       ( 675+300*j, 160+60*( i%5 ) ) )
                                    
                                pygame.mouse.set_visible( 1 )
                                
                            except AttributeError:
                                pygame.mouse.set_visible( 1 )
                                self.surface_menu.blit( self.res.image_button_medium, ( 650+300*j, 150+60*( i%5 ) ) )
                                self.surface_menu.blit( labels_players_keys[i],       ( 675+300*j, 160+60*( i%5 ) ) )                    
                            
            self.WINDOW.blit( self.surface_menu, ( 0, 0 ) )
            pygame.display.flip()

        
    def selectMap(self):
        self.surface_menu.fill(self.res.GREY)
        self.surface_menu.blit( self.surface_shadow, ( 0, 0 ) )
        
        tab_button          = []
        save_flag           = False
        end_loop            = True
        
        label_type          = self.res.font.render( 'CASTLE', 0, self.res.WHITE, None )
        label_random        = self.res.font.render( 'RANDOM', 0, self.res.WHITE, None )
        label_save          = self.res.font.render( 'SAVE',   0, self.res.GREY,  None )
        label_play          = self.res.font.render( 'PLAY',   0, self.res.WHITE, None )
                           
        button_prev_type    = pygame.Rect( ( self.WINDOW_SIZE[0]/2-245, self.WINDOW_SIZE[1]/2+25 ,30,  40 ) )
        button_next_type    = pygame.Rect( ( self.WINDOW_SIZE[0]/2+210, self.WINDOW_SIZE[1]/2+25 ,30,  40 ) )
        
        button_random_map   = pygame.Rect( ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+85 ,406, 50 ) )
        button_save_map     = pygame.Rect( ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+145,406, 50 ) )
        button_play         = pygame.Rect( ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+280,406, 50 ) )
        button_prev         = pygame.Rect( ( self.WINDOW_SIZE[0]/2-245, 170, 30,40))
        button_next         = pygame.Rect( ( self.WINDOW_SIZE[0]/2+210, 170, 30,40))
        
        self.surface_menu.blit( self.res.image_arrow_l, ( self.WINDOW_SIZE[0]/2-245, 170))
        self.surface_menu.blit( self.res.image_arrow_r, ( self.WINDOW_SIZE[0]/2+210, 170))
        self.surface_menu.blit( self.res.image_arrow_l, ( self.WINDOW_SIZE[0]/2-245, self.WINDOW_SIZE[1]/2+25  ) )
        self.surface_menu.blit( self.res.image_arrow_r, ( self.WINDOW_SIZE[0]/2+210, self.WINDOW_SIZE[1]/2+25  ) )
        
        self.surface_menu.blit( self.res.image_button,  ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+15  ) )
        self.surface_menu.blit( self.res.image_button,  ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+75  ) )
        self.surface_menu.blit( self.res.image_button,  ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+135 ) )
        self.surface_menu.blit( self.res.image_button,  ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+280 ) )
        
        self.surface_menu.blit( label_random,  ( self.WINDOW_SIZE[0]/2-178, self.WINDOW_SIZE[1]/2+85  ) )
        self.surface_menu.blit( label_save,    ( self.WINDOW_SIZE[0]/2-178, self.WINDOW_SIZE[1]/2+145 ) )
        self.surface_menu.blit( label_play,    ( self.WINDOW_SIZE[0]/2-178, self.WINDOW_SIZE[1]/2+290 ) )

        while end_loop:
            for event in pygame.event.get():
                if event.type==QUIT: self._quit_()
                elif event.type == KEYDOWN and event.key==K_ESCAPE: return 'back', 'back'
                
                if event.type == MOUSEMOTION:
                    if  button_random_map.collidepoint( pygame.mouse.get_pos() ):
                        self.surface_menu.blit( self.res.image_button_active, ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+75 ) )
                        self.surface_menu.blit( label_random,                 ( self.WINDOW_SIZE[0]/2-178, self.WINDOW_SIZE[1]/2+85 ) )
                    else:
                        self.surface_menu.blit( self.res.image_button,        ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+75 ) )
                        self.surface_menu.blit( label_random,                 ( self.WINDOW_SIZE[0]/2-178, self.WINDOW_SIZE[1]/2+85 ) )

                    if button_save_map.collidepoint( pygame.mouse.get_pos() ):
                        self.surface_menu.blit( self.res.image_button_active,     ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+135 ) )
                    else:
                        self.surface_menu.blit( self.res.image_button,        ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+135 ) )          

                    if button_play.collidepoint( pygame.mouse.get_pos() ):
                        self.surface_menu.blit( self.res.image_button_active, ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+280 ) )
                        self.surface_menu.blit( label_play,                   ( self.WINDOW_SIZE[0]/2-178, self.WINDOW_SIZE[1]/2+290 ) )
                    else:
                        self.surface_menu.blit( self.res.image_button,        ( self.WINDOW_SIZE[0]/2-212, self.WINDOW_SIZE[1]/2+280 ) )
                        self.surface_menu.blit( label_play,                   ( self.WINDOW_SIZE[0]/2-178, self.WINDOW_SIZE[1]/2+290 ) )
                    
                elif event.type == MOUSEBUTTONDOWN:
                    if button_prev.collidepoint( pygame.mouse.get_pos() ) and not self.mm_index == 0:
                        self.menu_click.play()
                        self.mm_index -= 1
                        save_flag      = False
                        self.level.drawMiniMap( self.mm_index, self.mm_type_index, None )
                        
                    if button_next.collidepoint( pygame.mouse.get_pos() ) and  self.mm_index < self.level.mm_index_max:
                        self.menu_click.play()
                        self.mm_index += 1
                        save_flag      = False
                        self.level.drawMiniMap( self.mm_index, self.mm_type_index, None )
                          
                    if button_prev_type.collidepoint( pygame.mouse.get_pos() ) and  not self.mm_type_index == 0:
                        self.menu_click.play()
                        self.mm_type_index -= 1
                        
                    if button_next_type.collidepoint( pygame.mouse.get_pos() ) and  self.mm_type_index < ( len( self.res.map_types ) -1 ):
                        self.menu_click.play()
                        self.mm_type_index += 1 

                    if button_random_map.collidepoint( pygame.mouse.get_pos() ):
                        self.menu_click.play()
                        self.mm_index  = 1
                        save_flag      = True
                        self.level.createRandomMap()

                    if button_save_map.collidepoint( pygame.mouse.get_pos() ) and save_flag:
                        self.menu_click.play()
                        save_flag      = False
                        self.level.saveMap(self.level.map)
                        
                    if button_play.collidepoint( pygame.mouse.get_pos() ):
                        self.menu_click.play()
                        end_loop=False             
        
                    if save_flag: label_save   = self.res.font.render( 'SAVE', 0, self.res.WHITE, None )
                    else:         label_save   = self.res.font.render( 'SAVE', 0, self.res.GREY,  None )
                
                    self.surface_mini_map = self.level.drawMiniMap( None, self.mm_type_index, self.level.map )
                    label_type            = self.res.font.render( self.res.map_types[ self.mm_type_index ], 0, self.res.WHITE, None )
                    
            self.surface_menu.blit( label_save, ( self.WINDOW_SIZE[0]/2-178, self.WINDOW_SIZE[1]/2+145 ) )
            
            self.WINDOW.blit( self.surface_menu,    ( 0, 0 ) )
            self.WINDOW.blit( self.surface_mini_map,( self.mm_x, self.mm_y+10 ) )
            self.WINDOW.blit( label_type,            ( self.WINDOW_SIZE[0]/2-178, self.WINDOW_SIZE[1]/2+25 ) )
            
            pygame.display.flip()
            
        return self.level.map, self.mm_type_index

    
    def selectHeroes(self, idtype):

        self.surface_line_shadow = pygame.Surface( ( self.res.WINDOW_SIZE[0], 350 ), pygame.SRCALPHA )
        
        surface_avatar_min_rdy   = pygame.Surface( ( 50 , 50 ),  pygame.SRCALPHA)
        surface_avatar_rdy       = pygame.Surface( ( 200, 200 ), pygame.SRCALPHA)
        
        self.surface_line_shadow.fill( self.res.BLACK_A )
        surface_avatar_rdy.fill( self.res.BLACK2_A )
        
        type_map          = self.res.map_types[idtype]
        tab_button_heroes = []
        tab_label_legend  = []
        p1                = 0
        p2                = 1
        p1_status         = True
        p2_status         = True
        render            = True
        heroes            = glob.glob( "res/player/*" )
        heroes_max        = len( heroes )
        
        tab_label_legend.append( self.res.font_small.render( 'START VALUE',      0, self.res.WHITE, None ) )
        tab_label_legend.append( self.res.font_small.render( 'BONUS MAP: START', 0, self.res.WHITE, None ) )
        tab_label_legend.append( self.res.font_small.render( 'MAX VALUE',        0, self.res.WHITE, None ) )
        tab_label_legend.append( self.res.font_small.render( 'BONUS MAP: MAX',   0, self.res.WHITE, None ) )
                                
        for x in range( heroes_max ):
            rect = pygame.Rect( ( 450+( 60*x ), self.WINDOW_SIZE[1]/2+180, 50, 50 ) )
            tab_button_heroes.append( rect )
        
        while True:
            for event in pygame.event.get():
                
                if event.type == KEYDOWN and event.key == (int)(self.tab_keys[3]) and p1 < heroes_max-1 and p1_status:
                    self.menu_click.play()
                    p1     += 1
                    render  = True

                elif event.type == KEYDOWN and event.key == (int)(self.tab_keys[2]) and p1 > 0 and p1_status:
                    self.menu_click.play()
                    p1     -= 1
                    render  = True

                elif event.type == KEYDOWN and event.key == (int)(self.tab_keys[8]) and p2 < heroes_max-1 and p2_status:
                    self.menu_click.play()
                    p2     += 1
                    render  = True

                elif event.type == KEYDOWN and event.key == (int)(self.tab_keys[7]) and p2 > 0 and p2_status:
                    self.menu_click.play()
                    p2     -= 1
                    render  = True

                elif event.type == KEYDOWN and event.key == (int)(self.tab_keys[4]) :
                    self.menu_click.play()
                    render    = True
                    p1_status = False

                elif event.type == KEYDOWN and event.key == (int)(self.tab_keys[9]):
                    self.menu_click.play()
                    render    = True
                    p2_status = False

                elif event.type == KEYDOWN and event.type == QUIT: self._quit_()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:  return 'back', 'back', 'back', 'back'
                    
            if render:
                    self.surface_menu.fill(self.res.GREY)
                    self.surface_menu.blit( self.surface_shadow,      ( 0, 0 ) )
                    self.surface_menu.blit( self.surface_line_shadow, ( 0, 75 ) )
                    
                    pygame.draw.rect( self.surface_menu, self.res.GREEN2, (200, 20, 20, 20 ) )
                    pygame.draw.rect( self.surface_menu, self.res.BLUE2,  (450, 20, 20, 20 ) )
                    pygame.draw.rect( self.surface_menu, self.res.GREY2,  (700, 20, 20, 20 ) )
                    pygame.draw.rect( self.surface_menu, self.res.GREY,   (950, 20, 20, 20 ) )
                
                    for i, label in enumerate( tab_label_legend ):
                        self.surface_menu.blit( label, ( 235+250*i, 20 ) )
                        
                    avatar_p1   = pygame.image.load( heroes[p1]+'/avatarr.gif' ).convert()
                    avatar_p2   = pygame.image.load( heroes[p2]+'/avatarr.gif' ).convert()
                    avatar_min  = pygame.image.load( heroes[0] +'/avatarr.gif' ).convert()

                    select_p1   = pygame.Rect( ( 468+p1*60,          self.WINDOW_SIZE[1]/2+178, 54,  54  ) )
                    select_p2   = pygame.Rect( ( 468+p2*60,          self.WINDOW_SIZE[1]/2+178, 54,  54  ) )
                    
                    self.Parser.read(heroes[p1]+"/hero.ini")
                    name_p1 = self.Parser.get("hero", "name")
                    
                    start_speed_p1 = (float)( self.Parser.get("hero", "start_speed"))
                    start_bombs_p1 = (float)( self.Parser.get("hero", "start_bombs"))
                    start_range_p1 = (float)( self.Parser.get("hero", "start_range"))
                    
                    max_speed_p1 = (float)( self.Parser.get("hero", "max_speed"))
                    max_bombs_p1 = (float)( self.Parser.get("hero", "max_bombs"))
                    max_range_p1 = (float)( self.Parser.get("hero", "max_range"))

                    map_bonus_p1 = ( self.Parser.get("hero", "best_map"))

                    if (map_bonus_p1.upper() == type_map):
                        bonus_start_speed_p1 = (float)( self.Parser.get("hero", "bonus_start_speed"))
                        bonus_start_bombs_p1 = (float)( self.Parser.get("hero", "bonus_start_bombs"))
                        bonus_start_range_p1 = (float)( self.Parser.get("hero", "bonus_start_range"))
                        bonus_max_speed_p1 =   (float)( self.Parser.get("hero", "bonus_max_speed"))
                        bonus_max_bombs_p1 =   (float)( self.Parser.get("hero", "bonus_max_bombs"))
                        bonus_max_range_p1 =   (float)( self.Parser.get("hero", "bonus_max_range"))
                    else:
                        bonus_start_speed_p1 = 0
                        bonus_start_bombs_p1 = 0
                        bonus_start_range_p1 = 0
                        bonus_max_speed_p1 =  0
                        bonus_max_bombs_p1 =  0
                        bonus_max_range_p1 =  0                   
                        
                    self.Parser.read(heroes[p2]+"/hero.ini")
                    
                    name_p2 = self.Parser.get("hero", "name")
             
                    start_speed_p2 =(float)( self.Parser.get("hero", "start_speed"))
                    start_bombs_p2 =(float)( self.Parser.get("hero", "start_bombs"))
                    start_range_p2 =(float)( self.Parser.get("hero", "start_range"))
                    
                    max_speed_p2 =(float)( self.Parser.get("hero", "max_speed"))
                    max_bombs_p2 =(float)( self.Parser.get("hero", "max_bombs"))
                    max_range_p2 =(float)( self.Parser.get("hero", "max_range"))

                    map_bonus_p2 = ( self.Parser.get("hero", "best_map"))

                    if (map_bonus_p2.upper() == type_map):
                        bonus_start_speed_p2 = (float)( self.Parser.get("hero", "bonus_start_speed"))
                        bonus_start_bombs_p2 = (float)( self.Parser.get("hero", "bonus_start_bombs"))
                        bonus_start_range_p2 = (float)( self.Parser.get("hero", "bonus_start_range"))
                        bonus_max_speed_p2 =   (float)( self.Parser.get("hero", "bonus_max_speed"))
                        bonus_max_bombs_p2 =   (float)( self.Parser.get("hero", "bonus_max_bombs"))
                        bonus_max_range_p2 =   (float)( self.Parser.get("hero", "bonus_max_range"))
                    else:
                        bonus_start_speed_p2 = 0
                        bonus_start_bombs_p2 = 0
                        bonus_start_range_p2 = 0
                        bonus_max_speed_p2 =  0
                        bonus_max_bombs_p2 =  0
                        bonus_max_range_p2 =  0
                        
                    label_versus    = self.res.font.render( 'VERSUS',     0, self.res.WHITE, None )
                    label_player1   = self.res.font.render( 'PLAYER 1',   0, self.res.WHITE, None )
                    label_player2   = self.res.font.render( 'PLAYER 2',   0, self.res.WHITE, None ) 
                    label_name_p1   = self.res.font.render( name_p1,      0, self.res.WHITE, None )
                    label_name_p2   = self.res.font.render( name_p2,      0, self.res.WHITE, None )
                    
                    self.surface_menu.blit( avatar_p1,        ( self.WINDOW_SIZE[0]/2-300, self.WINDOW_SIZE[1]/2-230 ) )
                    self.surface_menu.blit( avatar_p2,        ( self.WINDOW_SIZE[0]/2+100, self.WINDOW_SIZE[1]/2-230 ) )
                
                    self.surface_menu.blit( label_versus,  ( self.WINDOW_SIZE[0]/2-50,  self.WINDOW_SIZE[1]/2-130 ) )
                    self.surface_menu.blit( label_player1, ( 170, 120) )
                    self.surface_menu.blit( label_player2, ( 1000, 120) )
                    self.surface_menu.blit( label_name_p1, ( self.WINDOW_SIZE[0]/2-290, 345) )
                    self.surface_menu.blit( label_name_p2, ( self.WINDOW_SIZE[0]/2+110, 345) )
                    
                    for i in range (2):
                        pygame.draw.rect(self.surface_menu, self.res.GREY_DARK, (130+840*i,160,185,33))
                        pygame.draw.rect(self.surface_menu, self.res.GREY_DARK, (130+840*i,200,185,33))
                        pygame.draw.rect(self.surface_menu, self.res.GREY_DARK, (130+840*i,240,185,33))

                        self.surface_menu.blit(self.res.icon_speed, (135+840*i,161))
                        self.surface_menu.blit(self.res.icon_fire,  (135+840*i,201))
                        self.surface_menu.blit(self.res.icon_bomb,  (135+840*i,241))

                    pygame.draw.rect(self.surface_menu, self.res.GREY2, (170, 164, 12 * ( max_speed_p1 + bonus_max_speed_p1 - 0.99)*10 +7 , 25 ) )
                    pygame.draw.rect(self.surface_menu, self.res.GREY2, (170, 204, 6  * ( max_range_p1  + bonus_max_range_p1)          +7 , 25 ) )
                    pygame.draw.rect(self.surface_menu, self.res.GREY2, (170, 244, 12 * ( max_bombs_p1  + bonus_max_bombs_p1)          +7 , 25 ) )

                    pygame.draw.rect(self.surface_menu, self.res.GREY2, (170+840, 164, 12 * ( max_speed_p2 + bonus_max_speed_p2 - 0.99 )*10 +7 , 25 ))
                    pygame.draw.rect(self.surface_menu, self.res.GREY2, (170+840, 204, 6  * ( max_range_p2 + bonus_max_range_p2 )           +7 , 25 ))
                    pygame.draw.rect(self.surface_menu, self.res.GREY2, (170+840, 244, 12 * ( max_bombs_p2 + bonus_max_bombs_p2 )           +7 , 25 ))
                    
                    pygame.draw.rect(self.surface_menu, self.res.GREY_DARK2, (170, 164, 12 * (max_speed_p1 - 0.99)*10 +7 , 25 ) )
                    pygame.draw.rect(self.surface_menu, self.res.GREY_DARK2, (170, 204, 6  * max_range_p1             +7 , 25 ) )
                    pygame.draw.rect(self.surface_menu, self.res.GREY_DARK2, (170, 244, 12 * max_bombs_p1             +7 , 25 ) )

                    pygame.draw.rect(self.surface_menu, self.res.GREY_DARK2, (170+840, 164, 12 * (max_speed_p2 - 0.99)*10 +7 , 25 ) )
                    pygame.draw.rect(self.surface_menu, self.res.GREY_DARK2, (170+840, 204, 6  * max_range_p2             +7 , 25 ) )
                    pygame.draw.rect(self.surface_menu, self.res.GREY_DARK2, (170+840, 244, 12 * max_bombs_p2             +7 , 25 ) )

                    for i in range((int)((start_speed_p1-0.99) *10)):
                        pygame.draw.rect(self.surface_menu, self.res.GREEN2, (175+12*i,166,9,21))
                    for j in range((int)(bonus_start_speed_p1 * 10)):
                        pygame.draw.rect(self.surface_menu, self.res.BLUE2,  (175+12*(i+1)+12*j, 166,9,21))
                        
                    for i in range((int)(start_range_p1/2)):
                        pygame.draw.rect(self.surface_menu, self.res.GREEN2, (175+12*i,206,9,21))
                    for j in range((int)(bonus_start_range_p1/2)):
                        pygame.draw.rect(self.surface_menu, self.res.BLUE2,  (175+12*(i+1)+12*j, 206,9,21))
                        
                    for i in range((int)(start_bombs_p1)):
                        pygame.draw.rect(self.surface_menu, self.res.GREEN2, (175+12*i,246,9,21))
                    for j in range((int)(bonus_start_bombs_p1)):
                        pygame.draw.rect(self.surface_menu, self.res.BLUE2,  (175+12*(i+1)+12*j, 246,9,21))


                    for i in range((int)((start_speed_p2-0.99) *10)):
                        pygame.draw.rect(self.surface_menu, self.res.GREEN2, (175+840+12*i,166,9,21))
                    for j in range((int)(bonus_start_speed_p2 * 10)):
                        pygame.draw.rect(self.surface_menu, self.res.BLUE2,  (175+840+12*(i+1)+12*j, 166,9,21))
                        
                    for i in range((int)(start_range_p2/2)):
                        pygame.draw.rect(self.surface_menu, self.res.GREEN2, (175+840+12*i,206,9,21))
                    for j in range((int)(bonus_start_range_p2/2)):
                        pygame.draw.rect(self.surface_menu, self.res.BLUE2,  (175+840+12*(i+1)+12*j, 206,9,21))
                        
                    for i in range((int)(start_bombs_p2)):
                        pygame.draw.rect(self.surface_menu, self.res.GREEN2, (175+840+12*i,246,9,21))
                    for j in range((int)(bonus_start_bombs_p2)):
                        pygame.draw.rect(self.surface_menu, self.res.BLUE2,  (175+840+12*(i+1)+12*j, 246,9,21))

                    pygame.draw.rect( self.surface_menu, self.res.BLUE, select_p2 )
                    pygame.draw.rect( self.surface_menu, self.res.RED,  select_p1 )


            if p1 == p2:
                select_p2 = pygame.Rect ( ( 467+p2*60, self.WINDOW_SIZE[1]/2+177, 56, 56 ) )
            else:
                select_p2 = pygame.Rect ( ( 468+p2*60, self.WINDOW_SIZE[1]/2+178, 54, 54 ) )
                
            select_p1 = pygame.Rect ( ( 468+p1*60, self.WINDOW_SIZE[1]/2+178, 54, 54 ) )
            
            pygame.draw.rect( self.surface_menu, self.res.BLUE, select_p2 )
            pygame.draw.rect( self.surface_menu, self.res.RED,  select_p1 )
            
            for i in range( heroes_max ):
                avatar_min = pygame.image.load( heroes[i]+'/avatar_min.gif' ).convert()
                self.surface_menu.blit( avatar_min, ( 470+( 60*i ), self.WINDOW_SIZE[1]/2+180 ) )

            if not p1_status:
                self.surface_menu.blit( surface_avatar_rdy, ( self.WINDOW_SIZE[0]/2-300, self.WINDOW_SIZE[1]/2-230 ) )
                surface_avatar_min_rdy.fill( self.res.RED_A )
                self.surface_menu.blit( surface_avatar_min_rdy, ( 470+( 60*p1 ), self.WINDOW_SIZE[1]/2+180 ) )
                
            if not p2_status:
                self.surface_menu.blit( surface_avatar_rdy, ( self.WINDOW_SIZE[0]/2+100, self.WINDOW_SIZE[1]/2-230 ) )
                surface_avatar_min_rdy.fill( self.res.BLUE_A )
                self.surface_menu.blit( surface_avatar_min_rdy, ( 470+( 60*p2 ), self.WINDOW_SIZE[1]/2+180 ) )
                
            self.WINDOW.blit( self.surface_menu, ( 0, 0 ) )
            pygame.display.flip()

            if not p1_status and not p2_status:
                max_speed_p1 += bonus_max_speed_p1
                max_range_p1 += bonus_max_range_p1
                max_bombs_p1 += bonus_max_bombs_p1
                start_speed_p1 += bonus_start_speed_p1
                start_range_p1 += bonus_start_range_p1
                start_bombs_p1 += bonus_start_bombs_p1
                
                max_speed_p2 += bonus_max_speed_p2
                max_range_p2 += bonus_max_range_p2
                max_bombs_p2 += bonus_max_bombs_p2
                start_speed_p2 += bonus_start_speed_p2
                start_range_p2 += bonus_start_range_p2
                start_bombs_p2 += bonus_start_bombs_p2
                
                return heroes[p1], heroes[p2], [start_speed_p1, start_range_p1, start_bombs_p1, max_speed_p1, max_range_p1, max_bombs_p1], [start_speed_p2, start_range_p2, start_bombs_p2, max_speed_p2, max_range_p2, max_bombs_p2]

                
    def _quit_ ( self ):
        pygame.quit()
        exit( 0 )
        
