from random import random,randint,choice
import pygame,sys

class cell:
    """
    A class used to represent a terrain cell of a 2D terrain grid

    Attributes
    ----------
    x : int
        the row position of the cell in the grid
    y : int
        the column position of the cell in the grid
    state : str
        the terrain of the cell (default water)
    neighbours: list
        list of neighbouring cells of the grid
    is_delta : bool
        if the cell is the delta of a river
    is_begin : bool
        if the cell is the beggining of a river
    
    Methods
    -------
    state_neighbours(_state) : int
        Returns the number of neighbouring cells that have `_state`
    non_diagonal() : list
        Returns the non-diagonal neighbours of the cell
    get_path(_size):
        Returns a path from rhe cell of _size `_size`
    """
    def __init__(self,i=-1,j=-1):
        """
        Parameters
        ----------
        i : int, optional
            the row of the cell in the grid (default -1)
        j : int, optional
            the column of the cell in the grid (default -1)
        """
        self.x = i
        self.y = j
        self.state = "^"
        self.neighbours = []
        self.parent = [-2,-2]
        self.is_delta = False
        self.is_begin = False
  
    def state_neighbours(self,_state):
        """ Returns the number of neighbouring cells that have `_state`
        Parameters
        ----------
        _state : str
            the cell state
        """
        num = 0
        for a in self.neighbours:
            if a.state==_state:
                num += 1
        return num
    
    def non_diagonal(self):
        """Returns the non-diagonal neighbours of the cell
        """
        non_diag = self.neighbours.copy()

        for i in range(len(self.neighbours)):
            if self.neighbours[i].x!=self.x and self.neighbours[i].y!=self.y:
                non_diag.remove(self.neighbours[i])

        return non_diag
    
    def get_path(self,_size):
        """Returns a path from rhe cell of _size `_size`
        Parameters
        ----------
        _size : int
            Size of the path
        """
        path = [self]
        end = False

        while len(path)<_size and not end:
            candidates = path[-1].non_diagonal()
            elim = []
            for i in range(len(candidates)):
                for c in path:
                    if c.x==candidates[i].x and c.y==candidates[i].y:
                        elim.append(i)
                if candidates[i].state=="~" or candidates[i].state=="-":
                    elim.append(i)
            path_choices = [candidates[i] for i in range(len(candidates)) if
                            i not in elim]
            if not path_choices:
                end = True
            else:
                c = choice(path_choices)
                path.append(c)

        return path

class map2D:
    """
    A class used to represent a 2D map


    Attributes
    ----------
    water : str
        the symbol to represent water
    land : str
        the symbol to represent land
    river : str
        the symbol to represent a river
    mountain : str
        the symbol to represent a mountain
    map : list
        the grid of the map
    height : int
        the height of the map
    width : int
        the width of the map
    rivers : list
        the list of river paths
    
    Methods
    -------
    set_terrain_view(iter,prob_l,tol,prob_r,r_len,prob_m,m_len) : void
        Creates the map
    print_map() : str
        Returns a graphical representation for the map
    def river_corner(path) : list
        Returns a list of river corners and their appropiate angle
    """

    water = "~"
    land = "⯀"
    river = "-"
    mountain = "^"

    def __init__(self,h,w):
        self.map = []
        self.height = h
        self.width = w
        self.rivers = []

        for i in range(h):
            row = []
            for j in range(w):
                c = cell(i,j)
                c.state = map2D.water
                row.append(c)
            self.map.append(row)
        
        for row in self.map:
            for c in row:
                for i in range(c.x-1,c.x+2):
                    for j in range(c.y-1,c.y+2):
                        if i>=0 and i<h:
                            if j>=0 and j<w:
                                    c.neighbours.append(self.map[i][j])
                c.neighbours.remove(c)

    def set_terrain(self,iter=3,prob_l=0.5,tol=4,prob_r=0.1,r_len=6,prob_m=0.05,m_len=4):
        """Creates the map
        Parameters
        ----------
        iter : int, optional
            the number of smoothing iterations to the map (default 3)
        prob_l : float, optional
            the probability to spawn land (default 0.5)
        tol : int, optional
            the number of adjacent cells minimum for a cell to have the same state (default 4)
        prob_r : float, optional
            the probability to spawn rivers (default 0.1)
        r_len : int, optional
            the maximum lenght of rivers (default 6)
        prob_m : float, optional
            the probability to spawn mountains (default 0.05)
        m_len : int, optional
            the maximum lenght of mountain ranges (default 4)
        """
        # Land generation
        for row in self.map:
            for c in row:
                if random()<prob_l:
                    c.state = map2D.land
        
        # Smoothing
        n_iter = iter
        while n_iter>=0:
            for row in self.map:
                for c in row:
                    corner = ((c.x==0 or c.x==self.height-1) and
                              (c.y==0 or c.y==self.width-1))
                    if c.state==map2D.water and c.state_neighbours(map2D.water)<tol:
                        if corner and c.state_neighbours(map2D.water)<2:
                            c.state = map2D.land
                        elif not corner:
                            c.state = map2D.land
                    elif c.state==map2D.land and c.state_neighbours(map2D.land)<tol:
                        if corner and c.state_neighbours(map2D.land)<2:
                            c.state = map2D.water
                        elif not corner:
                            c.state = map2D.water
            n_iter -= 1
        
        # Mountain and river generation
        for row in self.map:
            seas = [row[i] for i in range(len(row)) if row[i].state==map2D.water]
            for c in seas: # River generation
                shores_aux = c.non_diagonal()
                shores = [shores_aux[i] for i in range(len(shores_aux)) if 
                          shores_aux[i].state==map2D.land and 
                          shores_aux[i].state_neighbours(map2D.river)==0]
                if shores and random()<prob_r:
                    new_river = choice(shores)
                    new_river.state = map2D.river
                    c.is_delta = True
                    river_lenght = randint(0,r_len-1)
                    river_path = [c]
                    path = new_river.get_path(river_lenght)
                    for p in path:
                        p.state = map2D.river
                    river_path += path
                    river_path[-1].is_begin = True
                    if len(river_path)>1:
                        self.rivers.append(river_path)
            lands = [row[i] for i in range(len(row)) if row[i].state==map2D.land and 
                     row[i].state_neighbours(map2D.mountain)==0]
            for c in lands: # Mountain generator
                if random()<prob_m:
                    c.state = map2D.mountain
                    mountain_lenght = randint(0,m_len-1)
                    last_cell = c
                    end = False
                    while mountain_lenght>0 and not end:
                        candidates = [last_cell.neighbours[i] for i in
                                      range(len(last_cell.neighbours)) if
                                      last_cell.neighbours[i].state==map2D.land]
                        if not candidates:
                            end = True
                        else:
                            last_cell = choice(candidates)
                            last_cell.state = map2D.mountain
                            mountain_lenght -= 1

    def print_map(self):
        """Returns a graphical representation for the map
        """
        map_image = "   "
        for i in range(len(self.map[0])):
            map_image += str(i+1) + " "
            if i<9:
                map_image += " "
        map_image += "\n"
        for i in range(len(self.map)):
            map_image += str(i+1) + " "
            if i<9:
                map_image += " "
            for j in range(len(self.map[i])):
                map_image += str(self.map[i][j].state) + "  "
            map_image += "\n"
        return map_image

    def river_corner(self,path):
        """Returns a list of river corners and their appropiate angle
        Parameters
        ----------
        path : list
            list of cells conforming the river
        """
        r_corners = []
        for i in range(1,len(path)-1):
            father = path[i-1]
            son = path[i+1]

            if father.x!=son.x and father.y!=son.y:
                r_corners.append([i,angle_3(father,son,path[i])])
        return r_corners

def angle_3(a,b,c):
    """Determines the angle of a corner `c` to match its neighbours

    Parameters
    ----------
    a : cell
        parent cell
    b : cell
        child cell
    c : cell
        corner cell
    """
    angle = 0
    if (a.x==b.x+1 and b.y==a.y+1 and c.y==a.y+1) or (b.x==a.x+1 and
        a.y==b.y+1 and c.y==b.y+1):
        angle = 90
    elif (b.x==a.x+1 and b.y==a.y+1 and c.x==a.x+1) or (a.x==b.x+1 and
          a.y==b.y+1 and c.x==b.x+1):
        angle = 180
    elif (b.x==a.x+1 and a.y==b.y+1 and b.x==c.x+1) or(a.x==b.x+1 and 
          b.y==a.y+1 and a.x==c.x+1):
        angle = 270
    return angle

def angle_2(a,rel):
    """Determines the turn angle of `a` relative to `rel` to match it

    Parameters
    ----------
    a : cell
        cell we want to know the angle
    rel: cell
        relative cell to the one we want
    """
    angle = 0
    if a.y==rel.y+1:
        angle = 90
    elif rel.y==a.y+1:
        angle = 270
    elif a.x==rel.x+1:
        angle = 180
    return angle