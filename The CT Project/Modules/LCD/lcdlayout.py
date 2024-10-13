#84 x 48
import pygame as p

PIXEL_SIZE = 10 #8
BORDER_X = PIXEL_SIZE*5
BORDER_Y = PIXEL_SIZE*4
running = True
cursor_x = BORDER_X
cursor_y = BORDER_Y
pixels = {}
default_drawn = False
MOUSE_DOWN = False
Z_DOWN = False

p.init()
width, height = 84*PIXEL_SIZE + 2*BORDER_X, 48*PIXEL_SIZE + 2*BORDER_Y
font = p.font.SysFont(None, PIXEL_SIZE)
screen = p.display.set_mode((width,height))

p.display.set_caption("Nokia 5110 Simulator")
screen.fill((192,192,192))

while running:
    toPrint = ""
    cursor_x = BORDER_X
    cursor_y = BORDER_Y
    
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
            break
    
    while default_drawn == False:
        for i in range(0,48):
            text_surface = font.render(f"Y {i}", True, (0,0,0))
            screen.blit(text_surface, (cursor_x-(PIXEL_SIZE*2), cursor_y))
            
            for x in range(0,84):   
                if i == 0:
                    text_surface = font.render(f" {x}", True, (0,0,0))
                    screen.blit(text_surface, (cursor_x, cursor_y-(PIXEL_SIZE*2)))
                
                pixels[f"pixel {int((cursor_x-BORDER_X)/PIXEL_SIZE)},{int((cursor_y-BORDER_Y)/PIXEL_SIZE)}"] = p.Rect(cursor_x, cursor_y, PIXEL_SIZE, PIXEL_SIZE)
                p.draw.rect(screen, (172, 172, 172), (cursor_x, cursor_y, PIXEL_SIZE, PIXEL_SIZE), width=1)
                cursor_x += PIXEL_SIZE
            
            cursor_y += PIXEL_SIZE
            cursor_x = BORDER_X
            default_drawn = True
            
        #print(pixels)
            
    if event.type == p.MOUSEBUTTONDOWN:
        MOUSE_DOWN = True
        toPrint = f"| X{int((event.pos[0]-BORDER_X)/PIXEL_SIZE)} Y{int((event.pos[1]-BORDER_Y)/PIXEL_SIZE)} |"
        mouse_x, mouse_y = event.pos
        
    elif event.type == p.MOUSEBUTTONUP:
        toPrint = f"| X{int((event.pos[0]-BORDER_X)/PIXEL_SIZE)} Y{int((event.pos[1]-BORDER_Y)/PIXEL_SIZE)} |"
        MOUSE_DOWN = False
    
    elif event.type == p.MOUSEMOTION:
        toPrint = f"| X{int((event.pos[0]-BORDER_X)/PIXEL_SIZE)} Y{int((event.pos[1]-BORDER_Y)/PIXEL_SIZE)} |"
        if MOUSE_DOWN == True:
            mouse_x, mouse_y = event.pos #only write if holding down 
            
    if event.type == p.KEYDOWN:
        if event.key == p.K_ESCAPE:
            Z_DOWN = True
    
    if event.type == p.KEYUP:
        if event.key == p.K_ESCAPE:
            Z_DOWN = False
    
    if MOUSE_DOWN == True:
        for pixel in pixels:
            if (pixels.get(pixel)).collidepoint(mouse_x, mouse_y):
                if Z_DOWN == True:
                    p.draw.rect(screen, (192, 192, 192), (pixels.get(pixel).left, pixels.get(pixel).top, pixels.get(pixel).width, pixels.get(pixel).height))
                    p.draw.rect(screen, (172, 172, 172), (pixels.get(pixel).left, pixels.get(pixel).top, pixels.get(pixel).width, pixels.get(pixel).height), width=1)
                    toPrint += f" Z"
                    
                else: 
                    p.draw.rect(screen, (000, 000, 000), (pixels.get(pixel).left, pixels.get(pixel).top, pixels.get(pixel).width, pixels.get(pixel).height))
                    toPrint += f" D"
    
    if toPrint != "":
        print(toPrint + "                     ", end='\r')
    
    toPrint = ""
    
    # Update the display
    p.display.flip()