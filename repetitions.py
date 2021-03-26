from consts import DEFAULT_A_FACTOR, DEFAULT_INTERVAL, DEFAULT_PRIORITY, media_dir
import os
import time
import subprocess
from gtts import gTTS
from datetime import datetime as dt
from datetime import timedelta


class Repetition:

    path: str
    priority: int
    content: str
    afactor: int
    interval: int
    last_rep: str

    def __init__(self,
                 content: str,
                 path: str = None,
                 afactor: int = DEFAULT_A_FACTOR,
                 interval: int = DEFAULT_INTERVAL,
                 last_rep: str = "1970-01-01",
                 priority: int = DEFAULT_PRIORITY):

        self.content = content
        self.afactor = afactor
        self.interval = interval
        self.last_rep = last_rep
        self.priority = priority
        if path is None:
            path = self.generate()
        self.path = path

    def __repr__(self):
        return f"<Rep: content: {self.content}>"

    def generate(self):
        print("Generating tts")
        try:
            tts = gTTS(self.content)
            fp = self.generate_fp()
            tts.save(os.path.join(media_dir, fp))
            print("Successfully generated tts")
            return fp
        except Exception:
            print("Failed to generate tts")
            return ""

    def generate_fp(self) -> str:
        fp = str(int(time.time()))
        return fp + ".mp3"

    def play(self):
        fp = os.path.join(media_dir, self.path)
        subprocess.Popen(["mpv", fp])

    def is_due(self):
        last_date = dt.strptime(self.last_rep, "%Y-%m-%d")
        due_Date = timedelta(days=self.interval) + last_date
        if dt.today() >= due_Date:
            return True
        return False

    def to_list(self):
        return [
                self.path,
                str(self.priority),
                self.content,
                str(self.afactor),
                str(self.interval),
                self.last_rep,
            ]
