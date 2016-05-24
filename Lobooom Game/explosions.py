import pygame, glob

class Explosion():
    def __init__( self, pos_x, pos_y, range_bomb, mapa, window ):
        self.WINDOW   = window
        self.mapa     = mapa
        self.range    = range_bomb
        
        self.x        = ( int )( pos_x/32 )*32+20
        self.y        = ( int )( pos_y/32 )*32+12
        self.tab_x    = ( int )( ( pos_x-208+16 )/32 )
        self.tab_y    = ( int )( ( pos_y-8+8 )/32 )
        
        self.tab_rect = []
        self.time     = 41
        self.exp_time = False
        
        self.ani_speed_init  = 8
        self.ani_pos         = 0
        self.ani_speed       = self.ani_speed_init
        self.ani             = glob.glob( "res/explosion/explosion_s*.gif"  )
        self.ani_rs          = glob.glob( "res/explosion/explosion_rs*.gif" )
        self.ani_u           = glob.glob( "res/explosion/explosion_u*.gif"  )
        self.ani_er          = glob.glob( "res/explosion/explosion_er*.gif" )
        self.ani_el          = glob.glob( "res/explosion/explosion_el*.gif" )
        self.ani_eu          = glob.glob( "res/explosion/explosion_eu*.gif" )
        self.ani_ed          = glob.glob( "res/explosion/explosion_ed*.gif" )
        
        self.ani_max         = len( self.ani )-1
        self.img             = pygame.image.load( self.ani[0]    )
        self.img_rs          = pygame.image.load( self.ani_rs[0] )
        self.img_u           = pygame.image.load( self.ani_u[0]  )
        self.img_er          = pygame.image.load( self.ani_er[0] )
        self.img_el          = pygame.image.load( self.ani_el[0] )
        self.img_eu          = pygame.image.load( self.ani_eu[0] )
        self.img_ed          = pygame.image.load( self.ani_ed[0] )
        
        
        self.range_u = 0
        self.range_d = 0
        self.range_l = 0
        self.range_r = 0
        
        self.rangeModify()

            
    def rangeModify( self ):
        end_u = True
        end_d = True
        end_l = True
        end_r = True
        
        for rang in range( 1, self.range ):
            if  self.tab_y + rang <= 21:  
                if   self.mapa[ self.tab_y+rang ][ self.tab_x ] == '0' and end_d: self.range_d += 1
                elif self.mapa[ self.tab_y+rang ][ self.tab_x ] == '#' and end_d:
                    self.range_d += 1
                    end_d         = False
                else: end_d       = False
            
            if   self.mapa[ self.tab_y-rang ][ self.tab_x ] == '0' and end_u: self.range_u += 1
            elif self.mapa[ self.tab_y-rang ][ self.tab_x ] == '#' and end_u:
                self.range_u +=1
                end_u         = False
            else: end_u       = False
            
            if   self.mapa[ self.tab_y ][ self.tab_x-rang ] == '0' and end_l: self.range_l += 1
            elif self.mapa[ self.tab_y ][ self.tab_x-rang ] == '#' and end_l:
                self.range_l +=1
                end_l = False
            else: end_l =False
            
            if  self.tab_x + rang <= 26:    
                if   self.mapa[ self.tab_y ][ self.tab_x+rang ] == '0' and end_r: self.range_r += 1
                elif self.mapa[ self.tab_y ][ self.tab_x+rang ] == '#' and end_r:
                    self.range_r +=1
                    end_r         = False
                else: end_r       = False
        
    def update( self, pos ):
        self.time -= 1
        if self.time<0: self.exp_time = True
            
        if pos != 0:
            self.ani_speed -= 1
            
            if self.ani_speed == 0: 
                self.img = pygame.image.load( self.ani[ self.ani_pos ] )
                
                if self.range > 1:
                    self.img_rs = pygame.image.load( self.ani_rs[ self.ani_pos ] )
                    self.img_u  = pygame.image.load( self.ani_u[  self.ani_pos ] )
                    
                self.img_er    = pygame.image.load( self.ani_er[ self.ani_pos ] )
                self.img_el    = pygame.image.load( self.ani_el[ self.ani_pos ] )
                self.img_eu    = pygame.image.load( self.ani_eu[ self.ani_pos ] )
                self.img_ed    = pygame.image.load( self.ani_ed[ self.ani_pos ] )
                
                self.ani_speed = self.ani_speed_init
                
                if self.ani_pos == self.ani_max:
                    self.ani_pos  = 0
                else:
                    self.ani_pos += 1
       
        for rang in range( 1, self.range ):
            if rang == 1: self.tab_rect.append( pygame.Rect( self.x, self.y, 20, 20 ) )
            if self.range_r > rang:
                self.WINDOW.blit( self.img_rs, ( self.x-4+rang*32, self.y-4 ) )
                rect = pygame.Rect( self.x+rang*32, self.y, 20, 20 )
                if self.tab_rect.count( rect ) < 1:
                    self.tab_rect.append( rect )
         
            if self.range_l > rang:
                self.WINDOW.blit( self.img_rs, ( self.x-4-rang*32, self.y-4 ) )
                rect = pygame.Rect( self.x-rang*32, self.y, 20, 20 )
                if self.tab_rect.count( rect ) < 1:
                    self.tab_rect.append( rect )
 
            if self.range_d > rang:
                self.WINDOW.blit( self.img_u, ( self.x-4, self.y-4+rang*32 ) )
                rect = pygame.Rect( self.x, self.y+rang*32, 20, 20 )
                if self.tab_rect.count( rect )<1:
                    self.tab_rect.append( rect )
          
            if self.range_u > rang:
                self.WINDOW.blit( self.img_u, (self.x-4, self.y-4-rang*32 ) )
                rect = pygame.Rect( self.x, self.y-rang*32, 20, 20 )
                if self.tab_rect.count( rect ) < 1:
                    self.tab_rect.append( rect )
  
        if self.range_r != 0:
            self.WINDOW.blit( self.img_er, (self.x-4+self.range_r*32, self.y-4 ) )
            rect = pygame.Rect( self.x+self.range_r*32, self.y, 20, 20 )
            if self.tab_rect.count( rect ) < 1:
                self.tab_rect.append( rect )
                
        if self.range_l != 0:
            self.WINDOW.blit( self.img_el,( self.x-4-self.range_l*32, self.y-4 ) )
            rect = pygame.Rect( self.x-self.range_l*32, self.y, 20, 20 )
            if self.tab_rect.count( rect ) < 1:
                self.tab_rect.append( rect )     

        if self.range_u != 0:
            self.WINDOW.blit( self.img_eu,( self.x-4, self.y-2-self.range_u*32 ) )
            rect = pygame.Rect( self.x, self.y-self.range_u*32, 20, 20 )
            if self.tab_rect.count( rect ) < 1:
                self.tab_rect.append( rect )
                
        if self.range_d != 0:
            self.WINDOW.blit( self.img_ed,( self.x-4, self.y-5+self.range_d*32 ) )       
            rect = pygame.Rect( self.x, self.y+self.range_d*32, 20, 20 )
            if self.tab_rect.count( rect ) < 1:
                self.tab_rect.append( rect )

        self.WINDOW.blit( self.img, ( self.x-4, self.y-4 ) )
        
