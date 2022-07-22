import turtle
import time
from math import sqrt
import random
import os


def midpoint_calculator(point_one, point_two):
    midpoint_one = ((point_one[0] + point_two[0]) / 2)
    midpoint_two = ((point_one[1] + point_two[1]) / 2)
    midpoints = (midpoint_one, midpoint_two)
    return midpoints


def draw_point(dot):
    t.penup()
    t.setposition(dot)
    t.pendown()
    t.dot(2)


if __name__ == '__main__':
    side_length = int(input("Enter side length of your triangle: "))
    number_of_dots = int(input("How many points would you like: "))
    refresh_rate = int(input("Please enter a number greater than 1 for your screen refresh rate. The higher the "
                             "number, the quicker the triangle will generate: "))
    beginning = time.time()
    screen = turtle.Screen()
    screen.setup(width=1024, height=768)
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    turtle.delay(0)
    screen.tracer(0)
    half_height = ((sqrt((side_length ** 2) - (side_length / 2) ** 2)) / 2)
    top_point = (0, half_height)
    left_point = (-side_length/2, -half_height)
    right_point = (side_length/2, -half_height)
    main_points = [top_point, left_point, right_point]
    for point in main_points:
        draw_point(point)
    first_choice = random.randint(0, len(main_points) - 1)
    second_choice = first_choice
    while first_choice == second_choice:
        second_choice = random.randint(0, len(main_points) - 1)
    if first_choice == 0:
        first_point = top_point
    elif first_choice == 1:
        first_point = left_point
    elif first_choice == 2:
        first_point = right_point
    if second_choice == 0:
        second_point = top_point
    elif second_choice == 1:
        second_point = left_point
    elif second_choice == 2:
        second_point = right_point
    midpoint = midpoint_calculator(first_point, second_point)
    draw_point(midpoint)
    previous_point = midpoint
    i = 1
    start = time.time()
    while i <= number_of_dots:
        # os.system('clear')
        new_choice = random.randint(0, len(main_points) - 1)
        if new_choice == 0:
            new_point = top_point
        elif new_choice == 1:
            new_point = left_point
        elif new_choice == 2:
            new_point = right_point
        midpoint = midpoint_calculator(new_point, previous_point)
        draw_point(midpoint)
        previous_point = midpoint
#         print(i)
        if i % refresh_rate == 0:
            screen.update()
        i += 1
    
#     os.system('clear')
    print("Triangle Complete!")
    print(f"Total time elapsed {(time.time() - beginning):.6f}")
    print(f"Time per point {((time.time() - beginning)/number_of_dots):.6f}")
    screen.exitonclick()
