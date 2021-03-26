#!/usr/bin/env python3

from repetitions import Repetition
from Queue import Queue
from repetitions import Repetition
from consts import data
import sys


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Requires a content argument")
        sys.exit(1)
    queue = Queue(data)
    rep = Repetition(args[1])
    queue.add_to_queue(rep)
    queue.write()
