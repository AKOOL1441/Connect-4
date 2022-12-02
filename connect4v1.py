import pygame
pygame.init()

WIN_WIDTH, WIN_HEIGHT = 700, 750
HEAD_WIDTH, HEAD_HEIGHT = 700, 150
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Connect 4 v1")

BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
WHITE = (255,255,255)
YELLOW = (255,0,0)

WINNER_FONT = pygame.font.SysFont("comicsans",100)
SCORE_FONT = pygame.font.SysFont("comicsans",40)

FPS = 60

TILE_WIDTH, TILE_HEIGHT = 100, 100
PIECE_VEL = 2.5

BACKGROUND = pygame.image.load("background.png")
BACKGROUND.set_colorkey(WHITE)
RED_PIECE_IMG = pygame.image.load("red_piece.png")
RED_PIECE = pygame.transform.scale(RED_PIECE_IMG,(TILE_WIDTH,TILE_HEIGHT))
RED_PIECE.set_colorkey(BLACK)
YELLOW_PIECE_IMG = pygame.image.load("yellow_piece.png")
YELLOW_PIECE = pygame.transform.scale(YELLOW_PIECE_IMG,(TILE_WIDTH,TILE_HEIGHT))
YELLOW_PIECE.set_colorkey(BLACK)


def draw_winner(winner_text):
    rendered_text = WINNER_FONT.render(winner_text,1,BLACK)
    WIN.blit(rendered_text,(WIN_WIDTH/2 - rendered_text.get_width()/2,
                                WIN_HEIGHT/2 - rendered_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def check_winner(pieces):
    #columns
    for column in pieces:
        if len(column) > 3:
            for i in range(len(column) - 3):
                if sum(column[i:i+4]) == 0:
                    return "Red wins!"
                elif sum(column[i:i+4]) == 4:
                    return "Yellow wins!"
    #rows
    for i in range(6):
        for j in range(4):
            try:
                four_row_sum = pieces[j][i] + pieces[j+1][i] + pieces[j+2][i] + pieces[j+3][i]
                if four_row_sum == 0:
                    return "Red wins!"
                elif four_row_sum == 4:
                    return "Yellow wins!"
            except IndexError:
                pass
    #diagonal +ve grad
    for i in range(2):
        for j in range(4):
            try:
                four_row_sum = pieces[j][i] + pieces[j+1][i+1] + pieces[j+2][i+2] + pieces[j+3][i+3]
                if four_row_sum == 0:
                    return "Red wins!"
                elif four_row_sum == 4:
                    return "Yellow wins!"
            except IndexError:
                pass
    #diagonal -ve grad
    for i in range(2):
        for j in range(4):
            try:
                four_row_sum = pieces[j][i+3] + pieces[j+1][i+2] + pieces[j+2][i+1] + pieces[j+3][i]
                if four_row_sum == 0:
                    return "Red wins!"
                elif four_row_sum == 4:
                    return "Yellow wins!"
            except IndexError:
                pass
    return False


def free_column(full_columns):
    column = pygame.mouse.get_pos()[0]//100
    if pygame.mouse.get_pos()[0] - (TILE_WIDTH/2)*(2*column + 1) < 0:
        side = -1
    else:
        side = 1
    while column in full_columns or column < 0 or column > 6:  
        column += side
        side *= -1
        if side < 0:
            side -= 1
        else:
            side += 1
    return column


def draw_window(red_turn,column,pieces,dropping,dropping_piece_pos,red_score,yellow_score):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN,BLACK,(0,0,HEAD_WIDTH,HEAD_HEIGHT))
    for i, elem in enumerate(pieces):
        for j, piece in enumerate(elem):
            tile_pos = (i*TILE_WIDTH,WIN_HEIGHT - (j+1)*TILE_HEIGHT)
            if piece == 0:
                WIN.blit(RED_PIECE,tile_pos)
            else:
                WIN.blit(YELLOW_PIECE,tile_pos)
    if red_turn:
        WIN.blit(RED_PIECE,(column*TILE_WIDTH,WIN_HEIGHT - 700))
        if dropping:
            dropping_piece_pos[1] += PIECE_VEL
            WIN.blit(RED_PIECE,tuple(dropping_piece_pos))
    else:
        WIN.blit(YELLOW_PIECE,(column*TILE_WIDTH, WIN_HEIGHT - 700))
        if dropping:
            dropping_piece_pos[1] += PIECE_VEL
            WIN.blit(YELLOW_PIECE,tuple(dropping_piece_pos))
    WIN.blit(BACKGROUND,(0,WIN_HEIGHT - 600))
    red_score_text = SCORE_FONT.render("Red: " + str(red_score),1,WHITE)
    WIN.blit(red_score_text,(10,0))
    yellow_score_text = SCORE_FONT.render("Yellow: " + str(yellow_score),1,WHITE)
    WIN.blit(yellow_score_text,(WIN_WIDTH - yellow_score_text.get_width() - 10,0))
    pygame.display.update()


def main(red_score=0,yellow_score=0,red_turn=True):
    pieces = [[],[],[],[],[],[],[]]
    piece_count = 0
    full_columns = []

    first_turn = red_turn
    dropping = False
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        draw_window(red_turn,free_column(full_columns),pieces,False,None,red_score,yellow_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    dropping = True
                    column = free_column(full_columns)
                    next_free_tile = [column*TILE_WIDTH,WIN_HEIGHT - (len(pieces[column]) + 1)*TILE_HEIGHT]
                    dropping_piece_pos = [column*TILE_WIDTH,WIN_HEIGHT - 700]
                    while dropping:
                        draw_window(red_turn,column,pieces,dropping,dropping_piece_pos,red_score,yellow_score)
                        if dropping_piece_pos == next_free_tile:
                            if red_turn:
                                pieces[column].append(0)
                            else:
                                pieces[column].append(1)
                            piece_count += 1
                            if len(pieces[column]) == 6:
                                full_columns.append(column)
                            red_turn = not red_turn
                            dropping = False

        winner_text = check_winner(pieces)
        if piece_count == 42:
            winner_text = "Draw, no winner"
        if winner_text:
            draw_winner(winner_text)
            run = False
            if "Red" in winner_text:
                main(red_score + 1,yellow_score,not first_turn)
            elif "Yellow" in winner_text:
                main(red_score,yellow_score + 1,not first_turn)
            else:
                main(red_score,yellow_score,not first_turn)
        
    pygame.quit()

if __name__ == "__main__":
    main()