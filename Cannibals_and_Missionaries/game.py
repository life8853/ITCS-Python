import pygame
import random
import sys

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 140, 0)
GRAY_TRANSPARENT = (53, 53, 53, 180)
WHITE = (255, 255, 255)

BOAT_TRAVEL_DISTANCE = 360
MAX_PEOPLE_IN_THE_BOAT = 2

INTERLINE = 30

MOVES_MARGIN = 10
TOP_MARGIN = 50

MENU_BIG_FONT_SIZE = 64
FONT_SIZE_SCORE = 32
MENU_HEADING_SIZE = 32
MENU_TEXT_SIZE = 20


CHARACTER_SIZE_WITH_BOTTOM_MARGIN = 120

STEP = 5

SELECT_STEP = 100

GAMEGRAPH = {
            "cccmmmb-": {"cb": "ccmmm-cb", "ccb": "cmmm-ccb",
                         "mb": "cccmm-mb", "mmb": "cccm-mmb",
                         "cmb": "ccmm-cmb"},
            "ccmmm-cb": {"cb": "cccmmmb-"},
            "cmmm-ccb": {"cb": "ccmmmb-c", "ccb": "cccmmmb-"},
            "ccmmmb-c": {"cb": "cmmm-ccb", "ccb": "mmm-cccb",
                         "mb": "ccmm-cmb", "mmb": "ccm-cmmb",
                         "cmb": "cmm-ccmb"},
            "ccmm-cmb": {"cb": "cccmmb-m",
                         "mb": "ccmmmb-c",
                         "cmb": "cccmmmb-"},
            "mmm-cccb": {"cb": "cmmmb-cc", "ccb": "ccmmmb-c"},
            "cmmmb-cc": {"cb": "mmm-cccb",
                         "mb": "cmm-ccmb", "mmb": "cm-ccmmb",
                         "cmb": "mm-cccmb"},
            "cm-ccmmb": {"cb": "ccmb-cmm", "ccb": "cccmb-mm",
                         "mb": "cmmb-ccm", "mmb": "cmmmb-cc",
                         "cmb": "ccmmb-cm"},
            "ccmmb-cm": {"cb": "cmm-ccmb", "ccb": "mm-cccmb",
                         "mb": "ccm-cmmb", "mmb": "cc-cmmmb",
                         "cmb": "cm-ccmmb"},
            "cc-cmmmb": {"cb": "cccb-mmm",
                         "mb": "ccmb-cmm", "mmb": "ccmmb-cm",
                         "cmb": "cccmb-mm"},
            "cccb-mmm": {"cb": "cc-cmmmb", "ccb": "c-ccmmmb"},
            "c-ccmmmb": {"cb": "ccb-cmmm", "ccb": "cccb-mmm",
                         "mb": "cmb-ccmm", "mmb": "cmmb-ccm",
                         "cmb": "ccmb-cmm"},
            "ccb-cmmm": {"cb": "c-ccmmmb", "ccb": "-cccmmmb"},
            "cmb-ccmm": {"cb": "m-cccmmb",
                         "mb": "c-ccmmmb",
                         "cmb": "-cccmmmb"},

            "cccmm-mb": "failure",
            "cccm-mmb": "failure",
            "cccmmb-m": "failure",
            "ccm-cmmb": "failure",
            "cmm-ccmb": "failure",
            "mm-cccmb": "failure",
            "cmmb-ccm": "failure",
            "cccmb-mm": "failure",
            "ccmb-cmm": "failure",
            "m-cccmmb": "failure",

            "-cccmmmb": "success"}


def undo_selection():
    '''
    Undos the selection of all characters, aka moves
    them back to their positions

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    if boat_side == 2:
        selected_step = SELECT_STEP
    else:
        selected_step = -SELECT_STEP

    if len(cannibals_position[1]) != 0:
        for cannibal in cannibals_position[1]:
            cannibals_position[boat_side].append(cannibal)
            cannibal["rect"] = cannibal["rect"].move(selected_step, 0)
        cannibals_position[1].clear()

    if len(missionary_position[1]) != 0:
        for missionary in missionary_position[1]:
            missionary_position[boat_side].append(missionary)
            missionary["rect"] = missionary["rect"].move(selected_step, 0)
        missionary_position[1].clear()


def failure():
    '''
    Displays the gameover message and takes away the
    control over the characters

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    text_rect = pygame.Rect(0, 0, 380, 200)
    text_rect.center = display.center
    pygame.draw.rect(window, BLACK, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sys.exit()

        myfont = pygame.font.Font('freesansbold.ttf', 48)

        msg1 = myfont.render("GAME OVER", True, RED)
        msg1_box = msg1.get_rect()
        msg1_box.center = display.center
        msg1_box.centery -= INTERLINE
        window.blit(msg1, msg1_box)

        msg2 = myfont.render("(space to exit)", True, RED)
        msg2_box = msg2.get_rect()
        msg2_box.center = display.center
        msg2_box.centery += INTERLINE
        window.blit(msg2, msg2_box)
        pygame.display.flip()


def success():
    '''
    Displays the congratulations message and takes away the
    control over the characters

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    text_rect = pygame.Rect(0, 0, 380, 200)
    text_rect.center = display.center
    pygame.draw.rect(window, BLACK, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sys.exit()

        myfont = pygame.font.Font('freesansbold.ttf', 48)

        msg1 = myfont.render("You won!", True, GREEN)
        msg1_box = msg1.get_rect()
        msg1_box.center = display.center
        msg1_box.centery -= INTERLINE
        window.blit(msg1, msg1_box)

        msg2 = myfont.render("(space to exit)", True, GREEN)
        msg2_box = msg2.get_rect()
        msg2_box.center = display.center
        msg2_box.centery += INTERLINE
        window.blit(msg2, msg2_box)
        pygame.display.flip()


def move_boat(boat):
    '''
    Moves the boast and all the characters
    onto the opposite bank of the river

    Parameters
    ----------
    boat : (str, Surface, Rect)

    Returns
    -------
    None
    '''

    global graph_action
    graph_action = ""

    global boat_moved

    done = False
    number_of_cannibals_transported = len(cannibals_position[1])
    number_of_missionaries_transported = len(missionary_position[1])
    i = 0
    j = 0

    if boat_side == 2:
        destination_side = 0
        selected_step = -STEP
    else:
        destination_side = 2
        selected_step = STEP

    if boat_moved == 0:
        boat["rect"] = boat["rect"].move(selected_step, 0)
        if (boat["rect"].centerx > display.centerx + BOAT_TRAVEL_DISTANCE/2
           or boat["rect"].centerx < display.centerx - BOAT_TRAVEL_DISTANCE/2):
            boat["surf"] = pygame.transform.flip(boat["surf"],
                                                 True, False)
            boat_moved = 1

    for cannibal in cannibals_position[1]:
        cannibal["rect"] = cannibal["rect"].move(selected_step, 0)
        i += 1
        if not display.contains(cannibal["rect"]):
            cannibal["rect"] = cannibal["rect"].move((-selected_step, 0))
            cannibal["surf"] = pygame.transform.flip(cannibal["surf"],
                                                     True, False)
            cannibals_position[destination_side].append(cannibal)
            graph_action += "c"
            if (number_of_cannibals_transported == i):
                cannibals_position[1].clear()

    for missionary in missionary_position[1]:
        missionary["rect"] = missionary["rect"].move(selected_step, 0)
        j += 1
        if not display.contains(missionary["rect"]):
            missionary["rect"] = missionary["rect"].move((-selected_step, 0))
            missionary["surf"] = pygame.transform.flip(missionary["surf"],
                                                       True, False)
            missionary_position[destination_side].append(missionary)
            graph_action += "m"
            if (number_of_missionaries_transported == j):
                missionary_position[1].clear()

    if (len(cannibals_position[1]) == 0 and len(missionary_position[1]) == 0):
        graph_action += "b"
        done = True

    return done


def move_cannibal():
    '''
    Selects a random cannibal to be moved by boat.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    if (len(cannibals_position[1]) + len(missionary_position[1])
            < MAX_PEOPLE_IN_THE_BOAT):
        random_cannibal = \
            random.randint(0, len(cannibals_position[boat_side]) - 1)

        cannibals_position[1].append(cannibals_position
                                     [boat_side][random_cannibal])
        cannibals_position[boat_side].pop(random_cannibal)

        moved_cannibal = len(cannibals_position[1]) - 1

        if boat_side == 2:
            selected_step = -SELECT_STEP
        else:
            selected_step = SELECT_STEP

        cannibals_position[1][moved_cannibal]["rect"] = \
            cannibals_position[1][moved_cannibal]["rect"] \
            .move(selected_step, 0)


def move_missionary():
    '''
    Selects a random missionary to be moved by boat.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    if (len(cannibals_position[1]) + len(missionary_position[1])
            < MAX_PEOPLE_IN_THE_BOAT):
        random_missionary = \
            random.randint(0, len(missionary_position[boat_side]) - 1)

        missionary_position[1].append(missionary_position
                                      [boat_side][random_missionary])
        missionary_position[boat_side].pop(random_missionary)

        moved_missionary = len(missionary_position[1]) - 1

        if boat_side == 2:
            selected_step = -SELECT_STEP
        else:
            selected_step = SELECT_STEP

        missionary_position[1][moved_missionary]["rect"] = \
            missionary_position[1][moved_missionary]["rect"] \
            .move(selected_step, 0)


def getkey():
    '''
    Handles all inputs for the main section of the game.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    global action
    global boat_moved
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                sys.exit()

            if (event.key == pygame.K_c and
               len(cannibals_position[boat_side])) != 0:
                move_cannibal()

            if (event.key == pygame.K_m and
               len(missionary_position[boat_side])) != 0:
                move_missionary()

            if (event.key == pygame.K_SPACE and
               (len(cannibals_position[1]) +
                    len(missionary_position[1])) != 0):
                boat_moved = 0
                action = "boat"

            if (event.key == pygame.K_BACKSPACE and
               (len(cannibals_position[1]) +
                    len(missionary_position[1])) != 0):
                undo_selection()


def menu():
    '''
    Displays the pre-game information on how to play the game.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    background = pygame.image.load("menu_background.png")
    background_rect = background.get_rect()

    margin_top = 10
    margin_heading = 50
    margin_text = 30

    heading_font = pygame.font.Font('freesansbold.ttf', MENU_HEADING_SIZE)
    text_font = pygame.font.Font('freesansbold.ttf', MENU_TEXT_SIZE)
    big_font = pygame.font.Font('freesansbold.ttf', MENU_BIG_FONT_SIZE)

    caption1 = {"text": "Cannibals and Missionaries",
                "font": heading_font,
                "under": display.top,
                "margin": margin_top, }

    caption2 = {"text": ("Your goal is to help 3 cannibals and 3"
                         " missionaries cross the river."),
                "font": text_font,
                "margin": margin_heading, }

    caption3 = {"text": "This task won't be easy.",
                "font": text_font,
                "margin": margin_text, }

    caption4 = {"text": ("Maximum of 2 people (at least 1)"
                         " can travel in the boat at"
                         " the same time."),
                "font": text_font,
                "margin": margin_heading, }

    caption5 = {"text": ("If you leave missionaries outnumbered by"
                         " cannibals on the same bank"),
                "font": text_font,
                "margin": margin_text, }

    caption6 = {"text": "they will be eaten alive.",
                "font": text_font,
                "margin": margin_text, }

    caption7 = {"text": "Controls",
                "font": heading_font,
                "margin": margin_heading, }

    caption8 = {"text": "c - select a cannibal",
                "font": text_font,
                "margin": margin_heading, }

    caption9 = {"text": "m - select a missionary",
                "font": text_font,
                "margin": margin_text, }

    caption10 = {"text": "backspace - undo the selection",
                 "font": text_font,
                 "margin": margin_text, }

    caption11 = {"text": "space - send boat to the other side",
                 "font": text_font,
                 "margin": margin_text, }

    caption11 = {"text": "escape - leave the game",
                 "font": text_font,
                 "margin": margin_text, }

    caption12 = {"text": "PRESS SPACE TO START",
                 "font": big_font,
                 "under": display.bottom / 3 * 2,
                 "margin": 0, }

    captions = [caption1, caption2, caption3, caption4,
                caption5, caption6, caption7, caption8,
                caption9, caption10, caption11, caption12]

    window.blit(background, background_rect)

    for i, caption in enumerate(captions):
        caption["surf"] = caption["font"].render(caption["text"], True, BLACK)
        caption["rect"] = caption["surf"].get_rect()
        caption["rect"].center = display.center
        if (caption.get("under", None) is not None):
            caption["rect"].top = caption["under"] + caption["margin"]
        else:
            caption["rect"].top = captions[i-1]["rect"].top + caption["margin"]
        window.blit(caption["surf"], caption["rect"])

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    main()


def main():
    '''
    Main function of the game.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    global boat_side
    boat_side = 0

    global action
    action = "listen"

    global graph_action
    graph_action = ""

    gamestate = "cccmmmb-"

    # Moves counter
    moves_number = 0

    moves_font = pygame.font.Font('freesansbold.ttf', FONT_SIZE_SCORE)
    moves_message = moves_font.render("Moves: " +
                                      str(moves_number),
                                      True, ORANGE)
    moves_box = moves_message.get_rect()
    moves_box.center = display.center
    moves_box.top = display.top + MOVES_MARGIN

    size_background_moves = (moves_box.width +
                             MOVES_MARGIN * 2,
                             moves_box.height +
                             MOVES_MARGIN * 2)
    moves_background = pygame.Surface(size_background_moves, pygame.SRCALPHA)
    moves_background.fill(GRAY_TRANSPARENT)
    moves_background_box = moves_background.get_rect()
    moves_background_box.left = moves_box.left - MOVES_MARGIN
    moves_background_box.centery = moves_box.centery

    # background
    background = pygame.image.load("background.jpeg")
    background_rect = background.get_rect()

    # Characters
    cannibal1 = {"file": "cannibal.png"}
    cannibal2 = {"file": "cannibal.png"}
    cannibal3 = {"file": "cannibal.png"}

    missionary1 = {"file": "missionary.png"}
    missionary2 = {"file": "missionary.png"}
    missionary3 = {"file": "missionary.png"}

    boat = {"file": "canoe.png"}

    global boat_moved
    boat_moved = 0

    characters = [cannibal1, cannibal2, cannibal3,
                  missionary1, missionary2, missionary3,
                  boat]

    global cannibals_position
    cannibals_position = [[cannibal1, cannibal2, cannibal3], [], []]

    global missionary_position
    missionary_position = [[missionary1, missionary2, missionary3], [], []]

    for i, character in enumerate(characters):
        character["surf"] = pygame.image.load(character["file"])
        character["surf"] = pygame.transform.flip(character["surf"], 1, 0)
        character["rect"] = character["surf"].get_rect()
        character["rect"].topleft = (0, i * CHARACTER_SIZE_WITH_BOTTOM_MARGIN
                                     + TOP_MARGIN)

    boat["rect"].center = display.center
    boat["rect"].left -= BOAT_TRAVEL_DISTANCE/2

    # Main processing loop
    while True:

        if action == "listen":
            getkey()

        if action == "boat":
            done = move_boat(boat)
            if done:
                if boat_side == 0:
                    boat_side = 2
                else:
                    boat_side = 0

                gamestate = GAMEGRAPH[gamestate][graph_action]

                moves_number += 1

                moves_message = moves_font.render("Moves: " +
                                                  str(moves_number),
                                                  True, ORANGE)

                if (moves_number) == 10:
                    moves_box = moves_message.get_rect()
                    moves_box.center = display.center
                    moves_box.top = display.top + MOVES_MARGIN

                    size_background_moves = (180, 50)
                    size_background_moves = (moves_box.width +
                                             MOVES_MARGIN * 2,
                                             moves_box.height +
                                             MOVES_MARGIN * 2)
                    moves_background = pygame.Surface(size_background_moves,
                                                      pygame.SRCALPHA)
                    moves_background.fill(GRAY_TRANSPARENT)
                    moves_background_box = moves_background.get_rect()
                    moves_background_box.left = moves_box.left - MOVES_MARGIN
                    moves_background_box.centery = moves_box.centery

                if GAMEGRAPH[gamestate] == "success":
                    action = "success"
                elif GAMEGRAPH[gamestate] == "failure":
                    action = "failure"
                else:
                    action = "listen"

        window.blit(background, background_rect)
        window.blit(moves_background, moves_background_box)
        window.blit(moves_message, moves_box)
        for character in characters:
            window.blit(character["surf"], character["rect"])

        pygame.display.flip()

        if action == "failure":
            failure()
        if action == "success":
            success()

        fps.tick(60)


if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption("Cannibals and Missionaries")
    window = pygame.display.set_mode((1000, 800))
    display = window.get_rect()
    fps = pygame.time.Clock()

    menu()
    main()
