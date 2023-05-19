import pygame
import math
import colorsys

pygame.init()

# pygame uses rgb color in the range of 0~255 for red, green, blue respectively

# initialize of our hsv color
hue = 0

WIDTH = 1920
HEIGHT = 1080

x_start, y_start = 0, 0

x_separator = 10
y_separator = 20

rows = HEIGHT // y_separator
columns = WIDTH // x_separator
screen_size = rows * columns

# we cannot change the offset to current point coordinate since this is a 'cross section'
# that every point will use during rotation inside the double for loop
x_offset = columns / 2
y_offset = rows / 2

z_angle, x_angle = 0, 0  # rotating animation

theta_spacing = 10
phi_spacing = 1  # for faster rotation change to 2, 3 or more, but first change 86, 87 lines as commented

chars = ".,-~:;=!*#$@"  # luminance index

screen = pygame.display.set_mode((WIDTH, HEIGHT))

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Donut')
font = pygame.font.SysFont('Arial', 18, bold=True)


def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def text_display(letter, x, y):
    text = font.render(str(letter), True, hsv_to_rgb(hue, 1, 1))
    display_surface.blit(text, (x, y))


run = True

while run:

    screen.fill((0, 0, 0))  # fill the screen with black color

    # reset during the game loop
    if y_start == rows * y_separator - y_separator:  # if we get to the very last point in a column
        y_start = 0

    if x_start == columns * x_separator - x_separator:  # if we get to the very last point in a row
        x_start = 0

    z_buffer = [0] * screen_size  # the depth of each point on the screen, used when determining luminance
    display = [' '] * screen_size  # the list of every point on the screen

    # This for loop compute the rotation, projection and luminance of all the points on the donut
    for j in range(0, 628, theta_spacing):  # from 0 to 2pi, collect all circles to form a donut
        for i in range(0, 628, phi_spacing):  # from 0 to 2pi, draw a circle on an x-y plane
            cross_section_sin = math.sin(i)
            cross_section_cos = math.cos(i)
            phi_sin = math.sin(j)
            phi_cos = math.cos(j)
            real_phi_cos = phi_cos + 2
            #  this is to make a hole in the center of the 'ball' to make it look like a donut
            z_angle_sin = math.sin(z_angle)
            z_angle_cos = math.cos(z_angle)
            D = 1 / (8 + cross_section_sin * real_phi_cos * z_angle_sin + phi_sin * z_angle_cos)
            # D stands for 1/real_depth, 8 stands for the distance from screen to the object
            # to make it closer or 'bigger', make the value smaller but not 0
            x_angle_sin = math.sin(x_angle)
            x_angle_cos = math.cos(x_angle)
            abb = cross_section_sin * real_phi_cos * z_angle_cos - phi_sin * z_angle_sin
            # abbreviation to make the formula shorter

            # Rotation
            x = int(x_offset + 40 * D * (cross_section_cos * real_phi_cos * x_angle_cos - abb * x_angle_sin))
            y = int(y_offset + 20 * D * (cross_section_cos * real_phi_cos * x_angle_sin + abb * x_angle_cos))
            o = int(x + columns * y)  # cast the coordinate of a 2d point into a 1d array index
            N = int(8 * ((phi_sin * z_angle_sin - cross_section_sin * phi_cos * z_angle_cos) * x_angle_cos -
                         cross_section_sin * phi_cos * z_angle_sin - phi_sin * z_angle_cos -
                         cross_section_cos * phi_cos * x_angle_sin))
            # luminance index

            # projection
            if rows > y > 0 and 0 < x < columns and D > z_buffer[o]:
                # check if the point is in the range of valid display and is closest to the screen
                z_buffer[o] = D  # update the point depth which is the closest to the screen so far
                display[o] = chars[N if N > 0 else 0]  # update display, negative number stands for no light

    # print('This is x', x_start)
    # print('This is y', y_start)

    # x_start = 0
    # y_start = 0

    # Display, that is, display all the point in the display list
    for i in range(len(display)):
        z_angle += 0.00002  # the speed of rotation around z-axis
        x_angle += 0.00002  # the speed of rotation around x-axis
        # we can do rotation around y-axis too but the effect does not change a lot
        # while giving much more burden to compiler
        if i == 0 or i % columns:
            text_display(display[i], x_start, y_start)
            x_start += x_separator
        else:
            y_start += y_separator
            x_start = 0
            text_display(display[i], x_start, y_start)
            x_start += x_separator

    pygame.display.update()

    hue += 0.005
    # to change the color of the donut every round, which is the reason why we use hsv color scale, we can only change
    # one parameter rather than three in RGB color system

    # to quit, please use esc button
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
