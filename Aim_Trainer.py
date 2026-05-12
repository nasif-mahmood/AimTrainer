import math
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer") #name of window

TARGET_INCREMENT = 400 # the time in milliseconds between each target spawn, the lower the number, the faster the targets will spawn
TARGET_EVENT = pygame.USEREVENT + 1 # creating a custom event for spawning targets

TARGET_PADDING = 30 # the minimum distance between targets, the lower the number, the closer the targets will be to each other

BG_COLOR = (0, 25, 40)
LIVES = 3
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("comicsans", 24) # the font and size of the text that will be displayed on the top bar

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
        
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE: # if the size of the target is greater than or equal to the max size, stop growing
            self.grow = False
        
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE
     
    # draw the target, the target is made up of 4 circles, the first circle is the outer circle, the second circle is the inner circle, the third circle is the middle circle, and the fourth circle is the center circle        
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)
        
    # checking if the mouse click is within the center circle of the target, if it is, return true, otherwise return false
    def collide(self, x, y): 
        distance = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2) # calculating the distance between the target and the mouse click using the distance formula
        return distance <= self.size * 0.4 # if the distance is less than or equal to the size of the center circle, return true, otherwise return false
    
def draw(win, targets):
    win.fill(BG_COLOR) # fill the window with the background color before drawing the targets
    for target in targets:
        target.draw(win)
    
def format_time(seconds):
    milli = math.floor(int(seconds * 1000 % 1000) / 100)
    seconds = int(round(seconds % 60, 1))
    minutes = int(seconds // 60)
    
    return f"{minutes:02d}:{seconds:02d}.{milli}" # formatting the time to display minutes, seconds, and milliseconds in the format of 0:00.0

# drawing the top bar, which will display the elapsed time, the number of targets pressed, the number of clicks, and the number of misses
def draw_top_bar(win, elapsed_time, targets_pressed, clicks, misses):
    pygame.draw.rect(win, "grey", (0,0, WIDTH, TOP_BAR_HEIGHT)) # drawing a rectangle at the top of the window to serve as the background for the top bar
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black") # rendering the text for the elapsed time
    
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black") # rendering the text for the speed, which is calculated by dividing the number of targets pressed by the elapsed time
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black") # rendering the text for the number of targets pressed
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black") # rendering the text for the number of misses and the number of lives remaining
    win.blit(time_label, (5,5)) # drawing the elapsed time text on the top bar
    win.blit(speed_label, (200,5)) # drawing the speed text on the top bar
    win.blit(hits_label, (450,5)) # drawing the number of targets pressed text on the top bar
    win.blit(lives_label, (650,5)) # drawing the number of lives remaining text on the top bar

def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white") # rendering the text for the elapsed time
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} targets/second", 1, "white") # rendering the text for the speed, which is calculated by dividing the number of
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white") # rendering the text for the number of targets pressed
    accuracy = round(targets_pressed / clicks * 100, 1) if clicks > 0 else 0
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white") # rendering the text for the accuracy, which is calculated by dividing the number of targets pressed
    
    win.blit(time_label, (get_middle(time_label), 100)) # drawing the elapsed time text on the end screen
    win.blit(speed_label, (get_middle(speed_label), 200)) # drawing the speed text on the end screen
    win.blit(hits_label, (get_middle(hits_label), 300)) # drawing the number of targets pressed text on the end screen
    win.blit(accuracy_label, (get_middle(accuracy_label), 400)) # drawing the accuracy text on the end screen
    
    pygame.display.update() # updating the display to show the changes made to the window
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

    
# this function is used to get the x coordinate for the text to be centered on the screen, it takes in a surface as an argument and returns the x coordinate for the text to be centered on the screen by subtracting half of the width of the surface from half of the width of the window
def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()
    
    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time() # getting the current time in seconds, this will be used to calculate the time it takes for the player to hit a target
    
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT) # setting the timer for the target spawn event
    
    while run:
        clock.tick(60) # setting the frame rate to 60 frames per second
        click = False
        mouse_pos = pygame.mouse.get_pos() # getting the current position of the mouse as a tuple of (x, y) coordinates
        elapsed_time = time.time() - start_time # calculating the elapsed time by subtracting the start time from the current time
        
        # Quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING) # generating a random x and y coordinate for the target, the target will not spawn within the padding distance from the edges of the window
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING) 
                target = Target(x,y)
                targets.append(target)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
        
        for target in targets:
            target.update()
            if target.size <= 0: # if the size of the target is less than or equal to 0, remove the target from the list
                targets.remove(target)
                misses += 1
            # if the mouse is clicked and the click collides with the target, remove the target from the list and increment the targets_pressed variable
            if click and target.collide(*mouse_pos): # the splat operator is used to unpack the mouse_pos tuple into x and y coordinates
                targets.remove(target)
                targets_pressed += 1
        if misses >= LIVES: # if the number of misses is greater than or equal to the number of lives, end the game
            end_screen(WIN, elapsed_time, targets_pressed, clicks)
        
        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, clicks, misses)
        pygame.display.update() # updating the display to show the changes made to the window
        
    pygame.quit()

if __name__ == "__main__":
    main()