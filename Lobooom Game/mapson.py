import configparser, pygame, random, glob, resources

class Level(object):
    def __init__(self, tile_size):
        self.res            = resources.Resources()
        
        self.walls          = []
        self.chests         = []
        self.tmp_check_list = []
        self.tile_size      = tile_size
        self.path_maps      = glob.glob('levels/lvl_*.txt')
        self.mm_index_max   = (len(self.path_maps))-1


    def readFromTxt(self, filename):
        self.parser      = configparser.ConfigParser()
        self.parser.read('levels/'+filename)
        
        self.map         = self.parser.get("level", "map").split('\n')
        self.width       = len(self.map[0])
        self.height      = len(self.map)
        
        self.mini_map_surface = pygame.Surface((self.width*15, self.height*15))

        
    def readLevelFromObject(self, mapa, path):
        self.map         = mapa
        self.width       = len(self.map[0])
        self.height      = len(self.map)        
        self.path        = path
        
        self.map_surface = pygame.Surface((self.width*self.tile_size[0], self.height*self.tile_size[1]))

        
    def render(self):
        for y,line in enumerate(self.map):
            for x,key in enumerate(line):

                
                if (key == '0' or key == '#') and line2[x] == '1' and line[x+1] == '1':
                    tile = pygame.image.load(self.path+'floor_shadow_up.gif').convert()
                   
                elif (key == '0' or key == '#') and line2[x] == '1' and line2[x+1] == '1':
                    tile = pygame.image.load(self.path+'floor_shadow_uf.gif').convert()
                 
                elif (key == '0' or key == '#') and line2[x] == '1':
                    tile = pygame.image.load(self.path+'floor_shadow_u.gif').convert()
                  
                elif (key == '0' or key == '#') and line[x+1] == '1' and line2[x+1] == '1':
                    tile = pygame.image.load(self.path+'floor_shadow_pf.gif').convert()
                 
                elif (key == '0' or key == '#') and line[x+1] == '1':
                    tile = pygame.image.load(self.path+'floor_shadow_p.gif').convert()
                   
                elif (key == '0' or key == '#') and line2[x+1] == '1':
                    tile = pygame.image.load(self.path+'floor_shadow_c.gif').convert()

                elif key == '1':
                    tile = pygame.image.load(self.path+'floor_shadow.gif').convert()
                    
                elif key == '0' or key == '#':
                    tile = pygame.image.load(self.path+'floor.gif').convert()

                self.map_surface.blit( tile,( x * self.tile_size[0], y * self.tile_size[1] ))
                
                if key == '1':
                    choice = random.randint(1,8)
                    if   choice == 1:   tile = pygame.image.load(self.path+'wall_1.gif').convert()
                    elif choice == 2:   tile = pygame.image.load(self.path+'wall_2.gif').convert()
                    else:               tile = pygame.image.load(self.path+'wall.gif').convert()

                    self.map_surface.blit( tile, ( x * self.tile_size[0], y * self.tile_size[1] ))

                
            line2 = line
            
        return self.map_surface, self.map


    def get_walls_rect(self,center_map_x,center_map_y):
        for y,line in enumerate(self.map):
            for x,key in enumerate(line):

                if key == '1':
                    rect=pygame.Rect((x*self.tile_size[0]+center_map_x,y*self.tile_size[1]+center_map_y)+(self.tile_size[0],self.tile_size[1]))
                    self.walls.append(rect)

                elif key == '#':
                    rect=pygame.Rect((x*self.tile_size[0]+center_map_x,y*self.tile_size[1]+center_map_y)+(self.tile_size[0],self.tile_size[1]))
                    self.chests.append(rect)
                    
        return self.walls,self.chests


    def drawMiniMap(self, index, type_index, tab_map):

        if not tab_map:
            self.parser       = configparser.ConfigParser() 
            self.parser.read( self.path_maps[index] )
            self.map          = self.parser.get("level", "map").split('\n')
            
        else:
            self.map          = tab_map

        if type_index == 0:
            COLOR_1 = self.res.GREY_LIGHT
            COLOR_2 = self.res.WHITE
            COLOR_3 = self.res.BROWN
            
        elif type_index == 1:
            COLOR_1 = self.res.BLUE_LIGHT
            COLOR_2 = self.res.WHITE
            COLOR_3 = self.res.GREY_LIGHT
            
        elif type_index == 2:
            COLOR_1 = self.res.GREEN_OLIVE
            COLOR_2 = self.res.WHITE
            COLOR_3 = self.res.GREY
            
        else:
            COLOR_1 = self.res.BLUE_LIGHT
            COLOR_2 = self.res.WHITE
            COLOR_3 = self.res.GREY_LIGHT    
            
        self.mini_map_surface.fill(COLOR_1)
        
        for y,line in enumerate(self.map):
            for x,key in enumerate(line):

                if key == '1': pygame.draw.rect(self.mini_map_surface, COLOR_2, [15*x, 15*y, 15, 15])
                if key == '#': pygame.draw.rect(self.mini_map_surface, COLOR_3, [15*x, 15*y, 15, 15])
                
        return self.mini_map_surface


    def createRandomMap(self):
        correct = True

        while correct:

            self.tmp_check_list = []
            random_map          = []
            line                = ''
            floors              = 12
            
            for y in range(0,22):
                for x in range(0,27):
                    
                    if   y == 0:    line+='1'
                    elif y == 21:   line+='1'
                    elif x == 0:    line+='1'
                    elif x == 26:   line+='1'
                    elif y == 1  and  x in (1,2,24,25): line+='0'
                    elif y == 20 and  x in (1,2,24,25): line+='0'
                    elif y == 2  and  x in (1,25):      line+='0'
                    elif y == 19 and  x in (1,25):      line+='0'
                    else:
                        choice=random.randint(1,10)

                        if 1 <= choice <= 3:
                            line   +='0'
                            floors +=1
                            
                        elif 4 <= choice <=6:
                            line   +='1'
                            
                        else:
                            line   +='#'
                            floors +=1
                            
                random_map.append(line)
                line = ''
            
            self.checkRandomMap(random_map,1,1)
            
            if floors == len(self.tmp_check_list): correct=False
     
        self.mini_map_surface.fill(self.res.BLACK)
        
        for y,line in enumerate(random_map):
            for x,key in enumerate(line):

                if key == '1': pygame.draw.rect(self.mini_map_surface, self.res.WHITE, [15*x, 15*y, 15, 15])
                if key == '#': pygame.draw.rect(self.mini_map_surface, self.res.BLUE,  [15*x, 15*y, 15, 15])
                
        self.map = random_map
        
        return self.mini_map_surface


    def checkRandomMap(self, tmp_map, x, y):
        if x!=0 and y!=0 and x!= 26 and y!=21:

            if tmp_map[y][x] == '0' or tmp_map[y][x] == '#':
                self.tmp_check_list.append((x, y))

            if (tmp_map[y-1][x] == '0' or tmp_map[y-1][x] == '#' ) and (x, y-1) not in self.tmp_check_list: 
                self.checkRandomMap(tmp_map, x,y -1)
               
            if (tmp_map[y][x-1] == '0' or tmp_map[y][x-1] == '#' ) and (x-1, y) not in self.tmp_check_list:
                self.checkRandomMap(tmp_map, x-1, y)

            if (tmp_map[y][x+1] == '0' or tmp_map[y][x+1] == '#' ) and (x+1, y) not in self.tmp_check_list:
                self.checkRandomMap(tmp_map, x+1, y)

            if (tmp_map[y+1][x] == '0' or tmp_map[y+1][x] == '#' ) and (x, y+1) not in self.tmp_check_list:
                self.checkRandomMap(tmp_map, x, y+1)


    def saveMap(self, mapa):
        
        index_file  = (str)(self.mm_index_max+2)
        string      = ''
        Parser      = configparser.ConfigParser()
        newfile     = open('levels/lvl_'+index_file+'.txt', 'w+')

        Parser.add_section('level')
        
        for y, line in enumerate(mapa):
            for x, key in enumerate(line):
                string += key
            string += '\n'
            
        Parser.set('level','map',''+string+'')
        Parser.write(newfile)
        
        newfile.close()
        
