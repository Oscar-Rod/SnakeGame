import random


class Snake:
    def __init__(self, map_size, position=None, square_size=15, length=5, speed=1, direction=None):
        self.square_size = square_size
        self.length = length
        self.speed = speed
        self.direction = {"x": 0, "y": 0}
        self.map_size = map_size
        if position is None:
            self.position = [random.randrange((length - 1) * square_size, map_size - length * square_size, square_size),
                             random.randrange((length - 1) * square_size, map_size - length * square_size, square_size)]
        else:
            self.position = [position[0], position[1]]
        self.delay_counter = 0
        self.set_direction(direction)
        self.body = Body(length, self.direction, self.position[0], self.position[1], square_size)
        self.alive = True

    def set_direction(self, direction):

        if direction is None:
            direction = random.choice(["left", "right", "up", "down"])

        if direction == "left":
            if self.direction["x"] == 1:
                return
            self.direction["x"] = -1
            self.direction["y"] = 0
        elif direction == "right":
            if self.direction["x"] == -1:
                return
            self.direction["x"] = 1
            self.direction["y"] = 0
        elif direction == "up":
            if self.direction["y"] == 1:
                return
            self.direction["x"] = 0
            self.direction["y"] = -1
        elif direction == "down":
            if self.direction["y"] == -1:
                return
            self.direction["x"] = 0
            self.direction["y"] = 1

    def update_position(self):
        if self.delay_counter == 10 - self.speed:
            segments = self.body.get_segments()
            last_segment = segments.pop(-1)
            last_segment.position_x = segments[0].position_x + self.direction["x"] * self.square_size
            last_segment.position_y = segments[0].position_y + self.direction["y"] * self.square_size
            if last_segment.position_x < 0 or last_segment.position_x > (self.map_size - self.square_size):
                self.alive = False
            if last_segment.position_y < 0 or last_segment.position_y > (self.map_size - self.square_size):
                self.alive = False
            segments.insert(0, last_segment)
        else:
            self.delay_counter += 1

    def get_segments(self):
        return self.body.get_segments()


class Segment:
    def __init__(self, position_x, position_y, size):
        self.position_x = position_x
        self.position_y = position_y
        self.size = size


class Body:
    def __init__(self, length, direction, head_x, head_y, square_size):
        self.length = length
        self.direction = direction
        self.head_x = head_x
        self.head_y = head_y
        self.size = square_size
        self.list_of_segments = self.generate_segments()

    def generate_segments(self):
        list_of_segments = []
        for i in range(self.length):
            pos_x = self.head_x - i * self.direction["x"] * self.size
            pos_y = self.head_y - i * self.direction["y"] * self.size
            list_of_segments.append(Segment(pos_x, pos_y, self.size))
        return list_of_segments

    def get_segments(self):
        return self.list_of_segments
