from typing import List
from Getch import getch
import sys
from repetitions import Repetition
import os
import csv
from datetime import datetime as dt


class Queue:

    fp: str
    reps: List["Repetition"] = []
    header = ["Path", "Priority", "Content", "A-Factor", "Interval", "Last Rep"]

    def __init__(self, fp: str):
        self.fp = fp
        if os.path.exists(fp):
            self.load()
        else:
            self.write()

    def loop(self):
        while True:
            key = getch()
            if key == "q":
                self.exit()
            elif key == " ":
                self.current_rep()
            elif key == "l":
                self.next_rep()

    def exit(self):
        self.write()
        sys.exit(0)

    def dismiss_current(self):
        self.sort_reps()
        if (not self.reps):
            print("No repetition to dismiss")
            return

        cur = self.reps[0]
        if not cur.is_due():
            print("No due repetition to dismiss.")
            return

        if len(self.reps) > 1:
            self.reps = self.reps[1:]
        else:
            self.reps.pop()

        print("Dismissed repetition")
        self.write()

    def next_rep(self):
        self.sort_reps()

        cur = None
        next_rep = None
        to_load = None

        if self.reps:
            cur = self.reps[0]
        if len(self.reps) > 1:
            next_rep = self.reps[1]

        if (cur and next_rep):
            self.reps = self.reps[1:]
            to_load = next_rep
        else:
            self.reps.pop()
            to_load = cur

        self.schedule(cur)
        if to_load.is_due():
            print("Loading repetition...")
            to_load.play()
        else:
            print("No more repetitions")

        self.write()

    def current_rep(self):
        if not self.reps or not self.reps[0].is_due():
            print("No outstanding reps.")
            return
        self.reps[0].play()

    def load(self):
        with open(self.fp) as fobj:
            reader = csv.reader(fobj)
            next(reader, None) # Skip header
            self.reps = [
                    Repetition(path=row[0], priority=int(row[1]), content=row[2], afactor=int(row[3]), interval=int(row[4]), last_rep=row[5])
                    for row in reader
                    ]

    def schedule(self, rep: "Repetition"):
        rep.last_rep = dt.strftime(dt.today(), "%Y-%m-%d")
        rep.interval = rep.afactor * rep.interval
        self.reps.append(rep)

    def is_duplicate(self, rep: "Repetition"):
        if any((row.content == rep.content for row in self.reps)):
            return True
        return False

    def sort_reps(self):
        self.reps.sort(key=lambda x: x.priority)
        self.reps.sort(key=lambda x: x.is_due())

    def add_to_queue(self, rep: "Repetition"):
        if self.is_duplicate(rep):
            print("Failed to add because it is a duplicate.")
            return False
        self.reps.append(rep)
        self.sort_reps()
        self.write()
        print("Added new rep: " + rep.content)
        return True

    def write(self) -> bool:
        try:
            with open(self.fp, 'w') as fobj:
                writer = csv.writer(fobj)
                rows = [self.header]
                rows.extend([rep.to_list() for rep in self.reps])
                writer.writerows(rows)
                print("Successfully wrote")
                return True
        except Exception as e:
            print(f"Failed to write with exception {e}")
            return False


