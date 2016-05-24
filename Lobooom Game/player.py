import random, pygame, time, mapson, glob, menu, resources

class Player(object):
    def __init__( self, pos_x, pos_y, keys, hero, params,player_id ):
        self.stand         = []
        self.other_players = []
        self.stand.append(pygame.image.load( hero+"/s_l.png" ).convert_alpha())
        self.stand.append(pygame.image.load( hero+"/s_u.png" ).convert_alpha())
        self.stand.append(pygame.image.load( hero+"/s_r.png" ).convert_alpha())
        self.stand.append(pygame.image.load( hero+"/s_d.png" ).convert_alpha())
        
        
        self.image = pygame.image.load( hero+"/s_u.png" ).convert_alpha()

        self.ani_pos        = 0
        self.ani_speed_init = 8
        self.ani_speed      = self.ani_speed_init
        self.ani_u          = glob.glob( hero+"/u*.png" )
        self.ani_d          = glob.glob( hero+"/d*.png" )
        self.ani_r          = glob.glob( hero+"/r*.png" )
        self.ani_l          = glob.glob( hero+"/l*.png" ) 
        self.ani_max        = len( self.ani_u )-1
        self.img_u          = pygame.image.load(self.ani_u[0]).convert_alpha()
        self.img_d          = pygame.image.load(self.ani_d[0]).convert_alpha()
        self.img_r          = pygame.image.load(self.ani_r[0]).convert_alpha()
        self.img_l          = pygame.image.load(self.ani_l[0]).convert_alpha()


        self.stand_flag = True
        self.id       = player_id
        self.x        = pos_x
        self.y        = pos_y
        self.rect     = pygame.Rect( pos_x,   pos_y,   30, 30 )
        self.min_rect = pygame.Rect( pos_x+4, pos_y+4, 15, 15 )
        
        self.speed_exp_bomb = 180
        self.counter_bomb   = 0
        self.buf_immortal   = False
        self.buf_immortal_time = 260
        self.first_bomb_collision = False
        
        self.speed          = params[0] 
        self.range          = (int) ( params[1] )
        self.bombs          = (int) ( params[2] )
        self.max_speed      = params[3] 
        self.max_range      = (int) ( params[4] )
        self.max_bombs      = (int) ( params[5] )

        self.keys           = keys
        self.key_up   = (int)(self.keys[0])
        self.key_down = (int)(self.keys[1])
        self.key_left = (int)(self.keys[2])
        self.key_right= (int)(self.keys[3])
        self.key_use  = (int)(self.keys[4])

        self.points = 0
        self.life = 1
        self.block = [True,True,True,True]
        
        
        
    def move( self, dir_x, dir_y, speed, walls, chests, bombs):
        if   self.speed == 1.2: self.ani_speed_init = 7
        elif self.speed == 1.4: self.ani_speed_init = 6.4
        elif self.speed == 1.6: self.ani_speed_init = 6.2
        elif self.speed == 1.8: self.ani_speed_init = 6
        elif self.speed == 2:   self.ani_speed_init = 5.8
        elif self.speed == 2.2: self.ani_speed_init = 5.6

        self.ani_speed -= 1
        if self.ani_speed < 0:
            
            if   dir_x == -1 and dir_y == -1:
                self.image = pygame.image.load( self.ani_d[ self.ani_pos ] )
                    
            elif dir_x ==  1 and dir_y == -1:
                self.image = pygame.image.load( self.ani_d[ self.ani_pos ] )

            elif dir_x == -1 and dir_y ==  1:
                self.image = pygame.image.load( self.ani_u[ self.ani_pos ] )
                    
            elif dir_x ==  1 and dir_y ==  1:
                self.image = pygame.image.load( self.ani_u[ self.ani_pos ] )

            elif dir_x ==  0 and dir_y ==  1:
                self.image = pygame.image.load( self.ani_u[ self.ani_pos ] )

            elif dir_x ==  0 and dir_y == -1:
                self.image = pygame.image.load( self.ani_d[ self.ani_pos ] )
                    
            elif dir_x ==  1 and dir_y ==  0:
                self.image = pygame.image.load( self.ani_r[ self.ani_pos ] )
                    
            elif dir_x == -1 and dir_y ==  0:
                self.image = pygame.image.load( self.ani_l[ self.ani_pos ] )

            self.ani_speed = self.ani_speed_init
            
            if self.ani_pos == self.ani_max:
                self.ani_pos  = 0
            else:
                self.ani_pos += 1
                

        rect = pygame.Rect( self.x - 1 * speed, self.y,             27, 27 )
        if not ( rect.collidelist(walls)==-1 and rect.collidelist(chests) == -1 ): self.block[0] = False
        else: self.block[0] = True

        rect = pygame.Rect( self.x,             self.y - 1 * speed, 27, 27 )
        if not ( rect.collidelist(walls)==-1 and rect.collidelist(chests) == -1 ): self.block[1] = False
        else: self.block[1] = True

        rect = pygame.Rect( self.x + 1 * speed, self.y,             27, 27 )
        if not ( rect.collidelist(walls)==-1 and rect.collidelist(chests) == -1 ): self.block[2] = False
        else: self.block[2] = True

        rect = pygame.Rect( self.x,             self.y + 1 * speed, 27, 27 )
        if not ( rect.collidelist(walls)==-1 and rect.collidelist(chests) == -1 ): self.block[3] = False
        else: self.block[3] = True
        
        

        if   dir_x == 1  and self.block[2] == True:  self.x=self.x + ( dir_x * speed )
        elif dir_x == 1  and dir_y == 0 and dir_y == 0 and self.block[1] == True and self.block[3] == True and  13.9 <= self.y % 32 <= 32:   self.y=self.y - ( 0.3 * speed )
        elif dir_x == 1  and dir_y == 0 and dir_y == 0 and self.block[1] == True and self.block[3] == True and  0    <= self.y % 32 <= 13.8: self.y=self.y + ( 0.3 * speed )
  
        if   dir_x == -1 and self.block[0] == True:  self.x=self.x + ( dir_x * speed )
        elif dir_x == -1 and dir_y == 0 and dir_y == 0 and self.block[1] == True and self.block[3] == True and 13.9 <= self.y % 32 <= 32:    self.y=self.y - ( 0.3 * speed )
        elif dir_x == -1 and dir_y == 0 and dir_y == 0 and self.block[1] == True and self.block[3] == True and 0    <= self.y % 32 <= 13.8:  self.y=self.y + ( 0.3 * speed )
        
        if   dir_y == 1  and self.block[3] == True:  self.y=self.y + ( dir_y * speed )
        elif dir_y == 1  and dir_x == 0 and dir_x == 0 and self.block[0] == True and self.block[2] == True and 17.9 <= self.x % 32 <=32:     self.x=self.x - ( 0.3 * speed )
        elif dir_y == 1  and dir_x == 0 and dir_x == 0 and self.block[0] == True and self.block[2] == True and 0    <= self.x % 32 <=17:     self.x=self.x + ( 0.3 * speed )
      
        if   dir_y == -1 and self.block[1] == True:  self.y=self.y + ( dir_y * speed )
        elif dir_y == -1 and dir_x == 0 and dir_x == 0 and self.block[0] == True and self.block[2] == True and 17.9 <= self.x % 32 <=32:     self.x=self.x - ( 0.3 * speed )
        elif dir_y == -1 and dir_x == 0 and dir_x == 0 and self.block[0] == True and self.block[2] == True and 0    <= self.x % 32 <=17:     self.x=self.x + ( 0.3 * speed )
      
        
        self.rect     = pygame.Rect( self.x,   self.y,   26, 26 )
        self.min_rect = pygame.Rect( self.x+4, self.y+4, 15, 15 )
        
        for other in self.other_players:
            if self.rect.colliderect(other.rect):

                self.x        = self.x - ( dir_x * speed )
                self.y        = self.y - ( dir_y * speed )
                self.rect     = pygame.Rect( self.x,   self.y,   30, 30 )
                self.min_rect = pygame.Rect( self.x+4, self.y+4, 15, 15 )
                
        for bomb in bombs:
            if bomb.set==True and self.rect.colliderect(bomb):
                self.x        = self.x - ( dir_x * speed )
                self.y        = self.y - ( dir_y * speed )
                self.rect     = pygame.Rect( self.x,   self.y,   30, 30 )
                self.min_rect = pygame.Rect( self.x+4, self.y+4, 15, 15 )
                
        if self.buf_immortal == True:
            self.buf_immortal_time -= 1
            if self.buf_immortal_time < 0:
                self.buf_immortal      = False
                self.buf_immortal_time = 260
        
    def updateKeys(self, keys):
        self.keys = keys
        self.key_up   = (int)(self.keys[0])
        self.key_down = (int)(self.keys[1])
        self.key_left = (int)(self.keys[2])
        self.key_right= (int)(self.keys[3])
        self.key_use  = (int)(self.keys[4])
