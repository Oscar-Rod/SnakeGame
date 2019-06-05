import copy


class Snake:
    def __init__(self, position, direction, cell_size=15, length=5, speed=1):
        self.cell_size = cell_size
        self.length = length
        self.speed = speed
        self.direction = direction
        self.speed_x = 0
        self.speed_y = 0
        self.set_speeds(direction)
        self.position = position
        self.delay_counter = 0
        self.body = Body(length, self.position[0], self.position[1], self.speed_x, self.speed_y, cell_size)
        self.alive = True

    def set_direction(self, direction):

        is_valid = self.check_is_a_valid_direction(direction)
        if is_valid:
            self.direction = direction
            self.set_speeds(direction)

    def check_is_a_valid_direction(self, direction):
        segments = self.body.get_segments()
        first = segments[0]
        second = segments[1]
        if first.position_x == second.position_x and first.position_y > second.position_y:
            if direction is "up":
                return False
        if first.position_x == second.position_x and first.position_y < second.position_y:
            if direction is "down":
                return False
        if first.position_y == second.position_y and first.position_x > second.position_x:
            if direction is "left":
                return False
        if first.position_y == second.position_y and first.position_x < second.position_x:
            if direction is "right":
                return False
        return True

    def set_speeds(self, direction):

        if direction == "left":
            self.speed_x = -1
            self.speed_y = 0
        elif direction == "right":
            self.speed_x = 1
            self.speed_y = 0
        elif direction == "up":
            self.speed_x = 0
            self.speed_y = -1
        elif direction == "down":
            self.speed_x = 0
            self.speed_y = 1

    def update_position(self):
        if self.delay_counter == 101 - self.speed:
            segments = self.body.get_segments()
            last_segment = segments.pop(-1)
            last_segment.position_x = segments[0].position_x + self.speed_x * self.cell_size
            last_segment.position_y = segments[0].position_y + self.speed_y * self.cell_size
            segments.insert(0, last_segment)
            self.delay_counter = 0
        else:
            self.delay_counter += 1

    def get_segments(self):
        return self.body.get_segments()

    def add_a_segment(self):
        self.body.add_a_segment()


class Segment:
    def __init__(self, position_x, position_y, size):
        self.position_x = position_x
        self.position_y = position_y
        self.size = size


class Body:
    def __init__(self, length, head_x, head_y, speed_x, speed_y, square_size):
        self.length = length
        self.speed_y = speed_y
        self.speed_x = speed_x
        self.head_x = head_x
        self.head_y = head_y
        self.size = square_size
        self.list_of_segments = self.generate_segments()

    def generate_segments(self):
        list_of_segments = []
        for i in range(self.length):
            pos_x = self.head_x - i * self.speed_x * self.size
            pos_y = self.head_y - i * self.speed_y * self.size
            list_of_segments.append(Segment(pos_x, pos_y, self.size))
        return list_of_segments

    def get_segments(self):
        return self.list_of_segments

    def add_a_segment(self):
        last_segment = self.list_of_segments[-1]
        copied_segment = copy.deepcopy(last_segment)
        self.list_of_segments.append(copied_segment)
