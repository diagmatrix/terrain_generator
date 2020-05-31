from terrain_generator import *

def main():
    #  Create map and screen
    h = 30
    w = 25
    mapa = map2D(h,w)
    mapa.set_terrain()
    pygame.init()
    screen = pygame.display.set_mode([32*h,32*w])

    # Import images
    water_img = pygame.image.load("water.png").convert()
    land_img = pygame.image.load("land.png").convert()
    land_2 = pygame.image.load("land_1.png").convert()
    mountain_img = pygame.image.load("mountain.png").convert()
    river_img = pygame.image.load("river.png").convert()
    river_begin = pygame.image.load("river_begin.png").convert()
    river_corner = pygame.image.load("river_corner.png").convert()
    delta = pygame.image.load("delta.png").convert()

    # Paint the map
    last_cell = cell(-2,-2)
    for row in mapa.map:
            for c in row:
                if c.state==map2D.water and not c.is_delta:
                    screen.blit(water_img,(32*c.x,32*c.y))
                elif c.state==map2D.land:
                    if random()<0.8:
                        screen.blit(land_img,(32*c.x,32*c.y))
                    else:
                        screen.blit(land_2,(32*c.x,32*c.y))
                elif c.state==map2D.mountain:
                    screen.blit(mountain_img,(32*c.x,32*c.y))

    # Paint the rivers
    for river_paths in mapa.rivers:
        r_corners = mapa.river_corner(river_paths)
        for i in range(len(river_paths)):
            if river_paths[i].is_delta:
                screen.blit(pygame.transform.rotate(delta,angle_2(river_paths[i+1],river_paths[i])),(32*river_paths[i].x,32*river_paths[i].y))
            elif river_paths[i].is_begin or river_paths[-1]==c:
                screen.blit(pygame.transform.rotate(river_begin,angle_2(river_paths[i],river_paths[i-1])),(32*river_paths[i].x,32*river_paths[i].y))
            else:
                screen.blit(pygame.transform.rotate(river_img,angle_2(river_paths[i],river_paths[i-1])),(32*river_paths[i].x,32*river_paths[i].y))
        for c in r_corners:
            screen.blit(pygame.transform.rotate(river_corner,c[1]),(32*river_paths[c[0]].x,32*river_paths[c[0]].y))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

main()