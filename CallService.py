import numpy as np
import random
import math
from numpy.core.fromnumeric import shape
from scipy.stats import poisson
import pygame


class Cars:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # 0 for up, 1 for down, 2 for left, 3 for right

        self.base = chooseMax_map[int(x/20), int(y/20)]
        self.original_base = chooseMax_map[int(x/20), int(y/20)]
        self.power = np.max(power_map[:, int(x/20), int(y/20)], axis=0)
        self.oncall = 'No'
        self.remain_time = 0

    def move_forward(self):
        # move forward on normal road
        if self.direction == 0:
            self.y = self.y - 20
        elif self.direction == 1:
            self.y = self.y + 20
        elif self.direction == 2:
            self.x = self.x - 20
        elif self.direction == 3:
            self.x = self.x + 20

    def move_cross(self):
        # move the place on crossroad
        move_direction_count = RandomNum(31)
        # original up direction
        if (self.direction == 0):
            # keep up
            if move_direction_count <= 15:
                self.y = self.y - 20
            # turn down
            elif 15 < move_direction_count <= 17:
                self.y = self.y + 20
                self.direction = 1
            # turn left
            elif 17 < move_direction_count <= 24:
                self.x = self.x - 20
                self.direction = 2
            # turn right
            elif 24 < move_direction_count <= 31:
                self.x = self.x + 20
                self.direction = 3
        # original down direction
        elif (self.direction == 1):
            # keep down
            if move_direction_count <= 15:
                self.y = self.y + 20
            # turn up
            elif 15 < move_direction_count <= 17:
                self.y = self.y - 20
                self.direction = 0
            # turn left
            elif 17 < move_direction_count <= 24:
                self.x = self.x - 20
                self.direction = 2
            # turn right
            elif 24 < move_direction_count <= 31:
                self.x = self.x + 20
                self.direction = 3
        # original left direction
        elif (self.direction == 2):
            # keep left
            if move_direction_count <= 15:
                self.x = self.x - 20
            # turn right
            elif 15 < move_direction_count <= 17:
                self.x = self.x + 20
                self.direction = 3
            # turn up
            elif 17 < move_direction_count <= 24:
                self.y = self.y - 20
                self.direction = 0
            # turn down
            elif 24 < move_direction_count <= 31:
                self.y = self.y + 20
                self.direction = 1
        # original right direction
        elif (self.direction == 3):
            # keep right
            if move_direction_count <= 15:
                self.x = self.x + 20
            # turn right
            elif 15 < move_direction_count <= 17:
                self.x = self.x - 20
                self.direction = 2
            # turn up
            elif 17 < move_direction_count <= 24:
                self.y = self.y - 20
                self.direction = 0
            # turn down
            elif 24 < move_direction_count <= 31:
                self.y = self.y + 20
                self.direction = 1


def RandomNum(upper_num):
    n = random.randint(0, upper_num)
    return n


def CreateBaseMap(appended_list):
    # set the base place
    base_id = 0
    for i in range(10):
        for j in range(10):
            base_flag = RandomNum(9)
            # this block create base or not
            if base_flag == 1:
                adjust_base_position = RandomNum(3)
                base_frequency = RandomNum(9)
                if adjust_base_position == 0:
                    base_unit = (base_id, 1250+i*2500-100, 1250 +
                                 j*2500, (base_frequency+1)*10)
                elif adjust_base_position == 1:
                    base_unit = (base_id, 1250+i*2500+100, 1250 +
                                 j*2500, (base_frequency+1)*10)
                elif adjust_base_position == 2:
                    base_unit = (base_id, 1250+i*2500, 1250+j *
                                 2500-100, (base_frequency+1)*10)
                elif adjust_base_position == 3:
                    base_unit = (base_id, 1250+i*2500, 1250+j *
                                 2500+100, (base_frequency+1)*10)
                appended_list.append(base_unit)
                base_id = base_id + 1
            else:
                pass
    return


def CountPower(mobile_x, mobile_y, base_x, base_y, frequency, pt):
    # calculate power
    distance = math.sqrt((base_x - mobile_x)**2 + (base_y - mobile_y)**2)
    pathloss = 32.45 + 20*math.log10(frequency) + 20*math.log10(distance/1000)
    power_value = pt - pathloss
    return power_value


def CreatePowerMap(p_array, b_list):
    # setting the map countain every place power
    for i in range(0, int(25000/20)+1):
        for j in range(0, int(25000/20)+1):
            for p in range(len(b_list)):
                p_array[p, i, j] = CountPower(
                    i*20, j*20, b_list[p][1], b_list[p][2], b_list[p][3], 120)


def CreateCar(c_list):
    # possion distri to set car enter
    possiblity = poisson.pmf(1, 1/12)
    for i in range(4):
        for j in range(1, 10):
            car_flag = RandomNum(int(1/possiblity))
            if car_flag == 0:
                if i == 0:  # up side
                    c_list.append(Cars(2500*j, 0, 1))
                elif i == 1:  # down side
                    c_list.append(Cars(2500*j, 25000, 0))
                elif i == 2:  # left side
                    c_list.append(Cars(0, 2500*j, 3))
                elif i == 3:  # right side
                    c_list.append(Cars(25000, 2500*j, 2))
            else:
                pass
    return


def MoveCar(c_list):
    for i in range(len(c_list)):
        # move place
        if ((c_list[i].x % 2500 == 0) and (c_list[i].y % 2500 == 0) and (c_list[i].x not in [0, 25000]) and (c_list[i].y not in [0, 25000])):
            c_list[i].move_cross()
        else:
            c_list[i].move_forward()
    return


def OnCall(c_list):
    for i in range(len(c_list)):
        # if not on call
        if c_list[i].oncall == 'No':
            # prob to call
            r = RandomNum(1800)
            if r == 1:
                # normal distribution set connect time
                mu = 180
                sigma = 1
                sample_times = np.random.normal(mu, sigma, 1)
                c_list[i].remain_times = sample_times
                c_list[i].oncall = 'Yes'
            else:
                pass
        # now on call
        else:
            # reduce remain times
            c_list[i].remain_times = c_list[i].remain_times - 1
            if c_list[i].remain_times < 0:
                c_list[i].oncall = 'No'
                c_list[i].remain_times = 0


def ChangeBase(c_list):
    for i in range(len(c_list)):
        # maintain power in original base
        c_list[i].power = power_map[c_list[i].base,
                                    int(c_list[i].x/20), int(c_list[i].y/20)]
        # choose used algorithm
        if case == 1:
            if(c_list[i].power < 35):
                max_value = np.max(
                    power_map[:, int(c_list[i].x/20), int(c_list[i].y/20)], axis=0)
                c_list[i].power = max_value
                c_list[i].base = chooseMax_map[int(
                    c_list[i].x/20), int(c_list[i].y/20)]
        elif case == 2:
            max_value = np.max(
                power_map[:, int(c_list[i].x/20), int(c_list[i].y/20)], axis=0)
            c_list[i].power = max_value
            c_list[i].base = chooseMax_map[int(
                c_list[i].x/20), int(c_list[i].y/20)]
        elif case == 3:
            max_value = np.max(
                power_map[:, int(c_list[i].x/20), int(c_list[i].y/20)], axis=0)
            if((max_value - c_list[i].power) > 25):
                c_list[i].power = max_value
                c_list[i].base = chooseMax_map[int(
                    c_list[i].x/20), int(c_list[i].y/20)]
        elif case == 4:
            max_value = np.max(
                power_map[:, int(c_list[i].x/20), int(c_list[i].y/20)], axis=0)
            if (max_value > 60):
                c_list[i].power = max_value
                c_list[i].base = chooseMax_map[int(
                    c_list[i].x/20), int(c_list[i].y/20)]
        # check it is on call and change original_base
        if c_list[i].oncall == 'Yes':
            if c_list[i].base != c_list[i].original_base:
                global exchange_count
                exchange_count = exchange_count + 1
                c_list[i].original_base = c_list[i].base
    return


def RemoveCar(c_list):
    # delete the car out boundary
    c_list[:] = [car_object for car_object in c_list if not (
        car_object.x > 25000 or car_object.x < 0 or car_object.y > 25000 or car_object.y < 0)]
    return


def DrawMap():
    # run through all base, and print it on screen
    for p in range(len(base_list)):
        x = base_list[p][1]/50
        y = base_list[p][2]/50
        if p == 0:
            color = (255, 255, 255)
        elif p == 1:
            color = (255, 0, 255)
        elif p == 2:
            color = (255, 255, 0)
        elif p == 3:
            color = (0, 255, 255)
        elif p == 4:
            color = (255, 0, 0)
        elif p == 5:
            color = (0, 255, 0)
        elif p == 6:
            color = (0, 0, 255)
        elif p == 7:
            color = (120, 120, 0)
        elif p == 8:
            color = (120, 30, 120)
        elif p == 9:
            color = (0, 120, 120)
        elif p == 10:
            color = (220, 120, 60)
        elif p == 11:
            color = (50, 50, 20)
        elif p == 12:
            color = (0, 150, 50)
        elif p == 13:
            color = (250, 10, 150)
        elif p == 14:
            color = (150, 250, 10)
        elif p == 15:
            color = (10, 150, 250)
        else:
            color = (0, 2, 5)
        pygame.draw.circle(screen, color, (x, y), 7)

    # run through all car and print it on screen
    for car in car_list:
        if car.oncall == 'Yes':
            if(car.base == 0):
                color = (255, 255, 255)
            elif(car.base == 1):
                color = (255, 0, 255)
            elif(car.base == 2):
                color = (255, 255, 0)
            elif(car.base == 3):
                color = (0, 255, 255)
            elif(car.base == 4):
                color = (255, 0, 0)
            elif(car.base == 5):
                color = (0, 255, 0)
            elif(car.base == 6):
                color = (0, 0, 255)
            elif(car.base == 7):
                color = (120, 120, 0)
            elif(car.base == 8):
                color = (120, 30, 120)
            elif(car.base == 9):
                color = (0, 120, 120)
            elif(car.base == 10):
                color = (220, 120, 60)
            elif(car.base == 11):
                color = (50, 50, 20)
            elif(car.base == 12):
                color = (0, 150, 50)
            elif(car.base == 13):
                color = (250, 10, 150)
            elif(car.base == 14):
                color = (150, 250, 10)
            elif(car.base == 15):
                color = (10, 150, 250)
            else:
                color = (0, 2, 5)
        else:
            color = (25, 25, 25)
        pygame.draw.rect(screen, color, pygame.Rect(car.x/50-1.5, car.y/50-1.5, 3, 3))


if __name__ == "__main__":
    # initialize basic info
    exchange_count = 0
    car_list = []

    # create base
    base_list = []
    CreateBaseMap(base_list)

    # choose algorithm
    case = int(input('Which algorithm you want (1, 2, 3, 4)?'))
    if case == 1:
        print('You choose Minimum Threshold algorithm')
    elif case == 2:
        print('You choose Best effort algorithm')
    elif case == 3:
        print('You choose Entropy algorithm')
    elif case == 4:
        print('You choose Maximum Threshold algorithm')

    # create power map
    power_map = np.empty([len(base_list), int(25000/20)+1, int(25000/20)+1])
    CreatePowerMap(power_map, base_list)

    # create map to find out max power base according to its place
    chooseMax_map = np.zeros([int(25000/20)+1, int(25000/20)+1])
    chooseMax_map = np.argmax(power_map, axis=0)

    # print out info
    print(power_map)
    print(shape(chooseMax_map))
    print(chooseMax_map)
    print(base_list)

    # create and init pygame
    pygame.init()
    screen = pygame.display.set_mode((int(25000/50), int(25000/50)), 0, 32)
    pygame.display.set_caption('Howard City - Call Service model')
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))

    # while loop to maintain simulation
    running = True
    while(running):
        # one time one second
        clock.tick(10)

        # fill screen with black
        screen.fill((0, 0, 0))

        # print car info
        # for i in range(len(car_list)):
        # print('x = ' + str(car_list[i].x) + ' y = ' + str(car_list[i].y)+' direction = ' + str(car_list[i].direction) +
        # ' base = ' + str(car_list[i].base) + ' oncall = ' + str(car_list[i].oncall) + ' power = ' + str(car_list[i].power))
        print('current total car number = ' + str(len(car_list)))
        oncall_car_list = []
        for car in car_list:
            if car.oncall == 'Yes':
                oncall_car_list.append(car)
        print('current on call number = ' + str(len(oncall_car_list)))
        print('total exchange count = ' + str(exchange_count))
        print()

        # create Car
        CreateCar(car_list)

        # move Car
        MoveCar(car_list)

        # delete Car
        RemoveCar(car_list)

        # change base
        ChangeBase(car_list)

        # check on call
        OnCall(car_list)

        # draw the map
        DrawMap()
        pygame.display.update()

        # check stop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
