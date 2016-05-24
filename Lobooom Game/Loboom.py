import random, pygame, time, mapson, menu, resources, player, bombs, explosions, hud, items, copy
from pygame.locals import *
from sys import exit

TILE_SIZE   = (32,32)
WINDOW_SIZE = (1280, 720)
WINDOW      = pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF)
CLOCK       = pygame.time.Clock()
_score      = [0,0,0,0]
pygame.display.set_caption('Lobooom')

class Game(object):
    def __init__(self, tab_map, map_type, p1, p2, state_p1, state_p2, players_keys):

        self.res         = resources.Resources()
        self.level       = mapson.Level(TILE_SIZE)
        self.type        = map_type
        self.map         = tab_map
        self.tab_players = []
        self.p1          = p1
        self.p2          = p2 
        self.state_p1    = state_p1
        self.state_p2    = state_p2
        self.option      = 3
        
        self.surface_shadow = pygame.Surface( ( self.res.WINDOW_SIZE ), pygame.SRCALPHA)
        self.surface_shadow.fill( self.res.BLACK_A )
        
        self.path_avatar_p1 = self.p1 + '/avatar_min.gif'
        self.path_avatar_p2 = self.p2 + '/avatar_min.gif'
        self.path           = 'res/levels/' + self.res.map_types[ self.type ] + '/'
        self.players_keys   = players_keys
        
        self.hud = hud.Hud( self.path_avatar_p1, self.path_avatar_p2, WINDOW_SIZE, _score )
        self.level.readLevelFromObject( self.map, self.path )
        self.image, self.mapa = self.level.render()
        
        self.center_map_x = WINDOW_SIZE[0]/2 - self.level.width *  TILE_SIZE[0]/2;
        self.center_map_y = WINDOW_SIZE[1]/2 - self.level.height * TILE_SIZE[1]/2;

        self.walls, self.chests = self.level.get_walls_rect( self.center_map_x, self.center_map_y )

        player1 = player.Player( self.center_map_x + TILE_SIZE[0], self.center_map_y + TILE_SIZE[1],
                                 self.players_keys[0:5], self.p1, self.state_p1, 1 )
        
        player2 = player.Player( self.center_map_x-TILE_SIZE[0] * 2 + TILE_SIZE[0] * self.level.width,
                                 self.center_map_y-TILE_SIZE[1] * 2 + TILE_SIZE[1] * self.level.height,
                                 self.players_keys[5:10], self.p2, self.state_p2, 2 )
        
        self.tab_players.append( player1 )
        self.tab_players.append( player2 )

        for pl in self.tab_players:
            pl.other_players = copy.copy( self.tab_players )
            pl.other_players.remove( pl )
            
        self.gameLoop()


    def gameLoop(self):
        
        tab_bombs      = []
        tab_chests     = []
        tab_explosion  = []
        tab_extras     = []
        tmp_map        = []
        direction      = 0
        newStr         = ''
        bomb_explosion = True
        
        pygame.mouse.set_visible( 0 )
   
        self.readyTime( self.image, [ self.center_map_x,self.center_map_y ] )
        
        avatar_path  =  self.p1 + '/avatar_min.gif'
        avatar2_path =  self.p2 + '/avatar_min.gif'
        
        for y, line in enumerate( self.mapa ):
            for x, key in enumerate( line ):
                if key == '#':
                    chest = items.Chest( x, y, self.center_map_x, self.center_map_y, self.path, WINDOW )
                    tab_chests.append( chest )
                    
        pygame.mixer.music.load('res/sounds/bgfightsound2.mp3')
        pygame.mixer.music.play(-1, 3.0)
        
        while 1:
            
            WINDOW.blit( self.hud.update( self.tab_players ), ( 0, 0 ) )
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == QUIT:
                    
                    x = self.pause( self.image, [ self.center_map_x, self.center_map_y ] )
                    if x == 2:
                        menu.optionsMenu()
                        for i, player in enumerate( self.tab_players ):
                            player.updateKeys( menu.tab_keys[ 0 + 5 * i : 5 + 5 * i ] )
                            
                    if x == 3:
                        self.option = 0
                        return 0
                    
                    elif x == 4: exitGame()
                    
            
            for player in self.tab_players:
                
                key = pygame.key.get_pressed()
              
                if    key[ player.key_right ] and key[ player.key_up   ]: player.move( 1,-1,  player.speed, self.walls, tab_chests, tab_bombs )
                elif  key[ player.key_left  ] and key[ player.key_up   ]: player.move(-1,-1,  player.speed, self.walls, tab_chests, tab_bombs )
                elif  key[ player.key_right ] and key[ player.key_down ]: player.move( 1, 1,  player.speed, self.walls, tab_chests, tab_bombs )
                elif  key[ player.key_left  ] and key[ player.key_down ]: player.move(-1, 1,  player.speed, self.walls, tab_chests, tab_bombs )
                elif  key[ player.key_right ]:
                    player.move(  1, 0, player.speed, self.walls, tab_chests, tab_bombs )
                    direction = 2
                    
                elif  key[ player.key_left  ]:
                    player.move( -1, 0, player.speed, self.walls, tab_chests, tab_bombs )
                    direction = 0
                    
                elif  key[player.key_up]:
                    player.move( 0, -1, player.speed, self.walls, tab_chests, tab_bombs )
                    direction = 3
                    
                elif  key[player.key_down]:
                    player.move( 0,  1, player.speed, self.walls, tab_chests, tab_bombs )
                    direction = 1
                    
                elif  not ( player.image in ( player.stand ) ): player.image = player.stand[ direction ]
                
                if key[ player.key_use ] and player.counter_bomb < player.bombs and player.min_rect.collidelist( tab_bombs ) == -1:
                    bomb = bombs.Bomb( player.x, player.y, player.speed_exp_bomb, player.range, self.tab_players.index( player ), WINDOW )
                    tab_bombs.append( bomb )
                    player.counter_bomb += 1
                        
            WINDOW.blit( self.image,( self.center_map_x, self.center_map_y ) )

            for chest in tab_chests:
                chest.update()
                for explosion in tab_explosion: 
                    if not chest.rect.collidelist( explosion.tab_rect ) == -1:
                        try:
                            tab_chests.remove( chest )
                            if random.choice( [ 1, 0, 0, 0 ] ) == 1:
                                extras = items.Extras( chest.x, chest.y, WINDOW )
                                tab_extras.append( extras )
                        except ValueError:
                            continue
                        
                        for y, line in enumerate( self.mapa ):
                            if y == chest.tab_y:    
                                for x, key in enumerate( line ):
                                    if x == chest.tab_x and y == chest.tab_y:
                                        newStr += '0'
                                    else:
                                        newStr += key
                                break
                            
                        self.mapa[ chest.tab_y ] = newStr
                        newStr = ''
                
            for bomb in tab_bombs:
                bomb.update()
                if bomb.rect.collidelist( self.tab_players ) == -1 and bomb.set == False:
                    bomb.set = True
                
                if bomb.explosion:
                    explosion = explosions.Explosion( bomb.x, bomb.y, bomb.range, self.mapa, WINDOW )
                    tab_explosion.append( explosion )
                    tab_bombs.remove( bomb )
                    
                    try:
                        if   bomb.player == 0: self.tab_players[ 0 ].counter_bomb -= 1
                        elif bomb.player == 1: self.tab_players[ 1 ].counter_bomb -= 1
                    except IndexError:
                        continue
                    
                for explosion in tab_explosion:
                    if not bomb.rect.collidelist( explosion.tab_rect ) == -1:
                        bomb.time = 0
           
            
            for i, player in enumerate( self.tab_players ):
                WINDOW.blit( player.image, ( player.x-2, player.y-5 ) )
                if  player.life == 0:
                    player.life =  2
                    for j, player in enumerate( self.tab_players ):
                        if player.life == 1:
                            _score[j] += 1
                    pygame.mixer.music.fadeout( 1400 )
                    time.sleep( 1 )
                    x = self.endRound(self.image, [ self.center_map_x, self.center_map_y ], self.tab_players )
                    self.option = x
                    return 0
                    
            for extras in tab_extras:
                extras.update()
                for player in self.tab_players:      
                    if player.rect.colliderect(extras.rect):
            
                        if    0 <= extras.choice <= 29 and player.range <= player.max_range: player.range += 1
                        elif 30 <= extras.choice <= 59 and player.speed <= player.max_speed: player.speed += 0.1
                        elif 60 <= extras.choice <= 84 and player.bombs <= player.max_bombs: player.bombs += 1
                        elif 85 <= extras.choice <= 89 :   player.buf_immortal = True
                        elif 90 <= extras.choice <= 100:   player.life = 0
                        tab_extras.remove( extras )
                        
            for explosion in tab_explosion:
                explosion.update( 1 )
                
                for player in self.tab_players:      
                    if not player.rect.collidelist( explosion.tab_rect ) == -1 and player.buf_immortal == False:
                        player.life = 0
                for extra in tab_extras:
                    if not  extra.rect.collidelist( explosion.tab_rect ) == -1 and extra.time_spawn == 0:
                        tab_extras.remove( extra ) 
                if explosion.exp_time:
                    tab_explosion.remove( explosion )
       
            pygame.display.flip()
            CLOCK.tick(60)

    def readyTime ( self , surface, pos_map ):
        time      = 180
        fps       = 60
        timer     = self.res.font_large.render( '3',    0, self.res.WHITE, None )
        label_rdy = self.res.font.render(       'READY IN ',    0, self.res.WHITE, None )
        self.time_sound = pygame.mixer.Sound('res/sounds/time.wav')
        self.go_sound   = pygame.mixer.Sound('res/sounds/go.wav')
        circle     = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.circle(circle, self.res.BLACK3_A, (100,100), 100)
        self.time_sound.play(0,0,0)
        while True:
            CLOCK.tick(60)
            
            WINDOW.blit( surface,             ( pos_map[0], pos_map[1] ) )
            WINDOW.blit( self.surface_shadow, ( 0,   0   ) )
            WINDOW.blit( circle,              ( 540, 235 ) )
            WINDOW.blit( timer,               ( 624, 340 ) )
            WINDOW.blit( label_rdy,           ( 580, 300 ) )
            
            time -= 1
            pygame.display.flip()
            
            if time < 0 : return 1
            elif time == 120:
                self.time_sound.play( 0, 0, 0 )
                timer = self.res.font_large.render( '2',    0, self.res.WHITE, None )
            elif time == 60:
                self.time_sound.play( 0, 0, 0 )
                timer = self.res.font_large.render( '1',    0, self.res.WHITE, None )
            elif time == 30:
                self.go_sound.play  ( 0, 0, 0 )


    
    def pause ( self , surface, pos_map):

        image_button_medium        = pygame.image.load( "res/misc/button_medium.gif"        ).convert()
        image_button_medium_active = pygame.image.load( "res/misc/button_medium_active.gif" ).convert()
        logo                       = pygame.image.load( "res/misc/logo.png"                 ).convert_alpha()
        
        tab_labels = []
        tab_buttons = []
        
        tab_labels.append( self.res.font.render( 'RESUME',    0, self.res.WHITE, None ) )
        tab_labels.append( self.res.font.render( 'OPTIONS',   0, self.res.WHITE, None ) )
        tab_labels.append( self.res.font.render( 'MAIN MENU', 0, self.res.WHITE, None ) )
        tab_labels.append( self.res.font.render( 'EXIT GAME', 0, self.res.WHITE, None ) )

        WINDOW.blit( surface, ( pos_map[0], pos_map[1] ) )
        WINDOW.blit( self.surface_shadow, ( 0, 0 ) )
        WINDOW.blit( logo,( 300,-100 ) )

        for i in range(4):
            tab_buttons.append( pygame.Rect(  ( WINDOW_SIZE[0]/2-150, WINDOW_SIZE[1]/2 + 40 + 60 * i, 280, 50 ) ) )

        for i in range(4):
            WINDOW.blit( image_button_medium, ( WINDOW_SIZE[0]/2-150, WINDOW_SIZE[1]/2 + 40 + 60 * i ) )
            
        for i in range(4):
            WINDOW.blit( tab_labels[i],       ( WINDOW_SIZE[0]/2-117, WINDOW_SIZE[1]/2+  50 + 60 * i ) )

        pygame.mouse.set_visible( 1 )
        
        while True:
            for event in pygame.event.get():
                
                if event.type == QUIT: exitGame()
                elif event.type == KEYDOWN and event.key==K_ESCAPE:
                    pygame.mouse.set_visible( 0 )
                    return 0

                if event.type == MOUSEMOTION:
                    for i, button in enumerate( tab_buttons ):
                        
                        if button.collidepoint( pygame.mouse.get_pos() ):
                            WINDOW.blit( image_button_medium_active, ( WINDOW_SIZE[0]/2-150, WINDOW_SIZE[1]/2+40+60*i ) )
                            WINDOW.blit( tab_labels[i],  ( WINDOW_SIZE[0]/2-117, WINDOW_SIZE[1]/2+50+60*i ) )
                        else:
                            WINDOW.blit( image_button_medium, ( WINDOW_SIZE[0]/2-150, WINDOW_SIZE[1]/2+40+60*i ) )
                            WINDOW.blit( tab_labels[i],  ( WINDOW_SIZE[0]/2-117, WINDOW_SIZE[1]/2+50+60*i ) )

                if event.type == MOUSEBUTTONDOWN:
                    for i, button in enumerate( tab_buttons ):
                        if button.collidepoint( pygame.mouse.get_pos() ):
                            if i<=2 :
                                pygame.mouse.set_visible( 0 )
                                return i+1
                            else: exitGame()
                            
           
            pygame.display.flip()

    def endRound ( self , surface, pos_map, players):
            image_button_medium = pygame.image.load( "res/misc/button_medium.gif" ).convert()
            image_button_medium_active = pygame.image.load( "res/misc/button_medium_active.gif" ).convert()
            circle_surface     = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, self.res.BLACK3_A, (80,80), 80)
            tab_labels = []
            tab_buttons = []

            for winner in players:
                if winner.life == 1:
                    winner_id = winner.id
            
            tab_labels.append( self.res.font.render( 'REVENGE',   0, self.res.WHITE, None ))
            tab_labels.append( self.res.font.render( 'MAIN MENU', 0, self.res.WHITE, None ))
            tab_labels.append( self.res.font.render( 'EXIT GAME', 0, self.res.WHITE, None ))
            tab_labels.append( self.res.font.render( 'PLAYER 1' , 0, self.res.WHITE, None ))
            tab_labels.append( self.res.font.render( 'PLAYER 2' , 0, self.res.WHITE, None ))            
            tab_labels.append( self.res.font_large.render( 'WINNER' , 0, self.res.WHITE, None ))
            tab_labels.append( self.res.font_large.render((str)(_score[0]) , 0, self.res.WHITE, None ))
            tab_labels.append( self.res.font_large.render((str)(_score[1]) , 0, self.res.WHITE, None ))
       
            WINDOW.blit( surface, ( pos_map[0], pos_map[1] ) )
            WINDOW.blit( self.surface_shadow, ( 0, 0 ) )
            WINDOW.blit( self.surface_shadow, ( 0, 0 ) )

            for i in range(3):
                tab_buttons.append( pygame.Rect( ( WINDOW_SIZE[0]/2-150, WINDOW_SIZE[1]/2+70+60*i, 280, 50 )))

            for i in range(3):
                WINDOW.blit( image_button_medium, ( WINDOW_SIZE[0]/2-150, WINDOW_SIZE[1]/2+70+60*i ))
                
            for i in range(3):
                WINDOW.blit( tab_labels[i], ( WINDOW_SIZE[0]/2-117, WINDOW_SIZE[1]/2+80+60*i ))

            WINDOW.blit( circle_surface,              ( 375, 200 ) )
            WINDOW.blit( circle_surface,              ( 735, 200 ) )
            WINDOW.blit(tab_labels[5], ( winner_id*363,80))
            WINDOW.blit(tab_labels[3], ( 400,150))
            WINDOW.blit(tab_labels[4], ( 760,150))
            
            WINDOW.blit(tab_labels[6], ( 440,250))
            WINDOW.blit(tab_labels[7], ( 800,250))
            
            pygame.mouse.set_visible( 1 )
            
            while True:
                for event in pygame.event.get():
                    
                    if event.type==QUIT: exitGame()
                    elif event.type == KEYDOWN and event.key==K_ESCAPE:
                        pygame.mouse.set_visible( 0 )
                        return 0

                    if event.type == MOUSEMOTION:
                        for i, button in enumerate( tab_buttons ):
                            
                            if button.collidepoint( pygame.mouse.get_pos() ):
                                WINDOW.blit( image_button_medium_active, ( WINDOW_SIZE[0]/2-150, WINDOW_SIZE[1]/2+70+60*i ))
                                WINDOW.blit( tab_labels[i],  ( WINDOW_SIZE[0]/2-117, WINDOW_SIZE[1]/2+80+60*i ))
                            else:
                                WINDOW.blit( image_button_medium, ( WINDOW_SIZE[0]/2-150, WINDOW_SIZE[1]/2+70+60*i ))
                                WINDOW.blit( tab_labels[i],  ( WINDOW_SIZE[0]/2-117, WINDOW_SIZE[1]/2+80+60*i ))

                    if event.type == MOUSEBUTTONDOWN:
                        for i, button in enumerate( tab_buttons ):
                            if button.collidepoint( pygame.mouse.get_pos() ):
                                if   i == 0 : return 1
                                elif i == 1 : return 0     
                                else: exitGame()
  
                pygame.display.flip()


def exitGame():
        pygame.quit()
        exit(0)

if __name__=='__main__':
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        menu = menu.Menu(TILE_SIZE, WINDOW_SIZE, WINDOW)
    
        while 1:
            _score = [0,0,0,0]
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load('res/sounds/bgfightsound.mp3') 
                pygame.mixer.music.play(-1, 1.0)
            m1 = menu.startMenu()
            m2 = 1
            if m1 == 1: 
                while m2:
                    if m2 == 1:
                        tab_map, type_map = menu.selectMap()
                        if tab_map == 'back' or type_map == 'back': break
                        else: m2 = 2                    
                    elif m2 == 2:
                        p1, p2, state_p1, state_p2 = menu.selectHeroes(type_map)
                        if p1 == 'back' or p2 == 'back': m2 = 1 
                        else: m2 = 3
                    elif m2 == 3:
                        play = Game (tab_map, type_map, p1,p2,state_p1,state_p2, menu.tab_keys)
                        m2 = play.option
       
            elif m1 == 2: menu.optionsMenu()
            elif m1 == 4: exitGame()
               
   
