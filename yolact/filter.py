
import numpy as np

class Filter:

    def __init__(self, w, h):
        self.prev = np.zeros((h, w))
        self.w = w
        self.h = h
    
    def init(self, depth):
        self.prev = depth

    def filter(self, depth, alpha):
        self.prev = alpha * depth + (1.0 - alpha) * self.prev

        return self.prev
