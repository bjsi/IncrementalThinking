#!/usr/bin/env python3

from Queue import Queue
from consts import data


if __name__ == "__main__":
    queue = Queue(data)
    queue.loop();
