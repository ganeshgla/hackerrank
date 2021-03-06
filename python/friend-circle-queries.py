#!/bin/python3

import math
import os
import random
import re
import sys


class FriendCircle:
    """
    Roughly a disjoint set.
    """

    def __init__(self):
        self.circles = {}  # person => parent
        self.circle_sizes = {}  # person => size of the circle they belong to
        self.largest_circle_size = 1

    def befriend(self, friend_a, friend_b):
        self.maybe_init_circle(friend_a)
        self.maybe_init_circle(friend_b)

        circle_a = self.find_circle(friend_a)
        circle_b = self.find_circle(friend_b)

        if circle_a != circle_b:
            self.combine_circles(circle_a, circle_b)

    def combine_circles(self, circle_a, circle_b):
        self.circles[circle_b] = circle_a
        new_circle_size = self.circle_sizes[circle_a] + \
            self.circle_sizes[circle_b]
        self.circle_sizes[circle_a] = new_circle_size
        self.circle_sizes[circle_b] = new_circle_size
        self.maybe_update_largest_circle_size(new_circle_size)

    def find_circle(self, person):
        if self.circles[person] == person:
            # person is their own parent so they are the head of the circle.
            return person
        else:
            # path compression.
            self.circles[person] = self.find_circle(self.circles[person])
            return self.circles[person]

    def maybe_init_circle(self, person):
        if person not in self.circles:
            self.circles[person] = person
            self.circle_sizes[person] = 1

    def maybe_update_largest_circle_size(self, circle_size):
        if circle_size > self.largest_circle_size:
            self.largest_circle_size = circle_size


if __name__ == '__main__':
    friend_circle = FriendCircle()
    num_queries = int(input())
    for _ in range(num_queries):
        friend_a, friend_b = tuple(map(int, input().rstrip().split()))
        friend_circle.befriend(friend_a, friend_b)
        print(friend_circle.largest_circle_size)
