"""Run slider_bar_psychopy.main() in a real PsychoPy window with scripted input.

The slider's mouse and PsychoPy's key reader are replaced by a frame-by-frame
script, so this checks the trial logic and CSV output. It does not replace
testing with a real mouse and keyboard (see README, "Verification").

Usage: python tests/simulated_session.py [screenshot.png]
"""
import csv
import sys
from pathlib import Path

repo = Path(__file__).resolve().parent.parent
shot = Path(sys.argv[1]) if len(sys.argv) > 1 else repo / "data" / "screenshot.png"
sys.path.insert(0, str(repo))

from psychopy import event, visual  # noqa: E402

# frame index -> (mouse_down, mouse_x, keys)
SCRIPT = {
    # trial 1: Enter before any selection must be ignored; then click the left end (0)
    1: (False, 0, ["return"]),
    2: (True, -200, []), 3: (True, -200, []), 4: (False, -200, []),
    6: (False, 0, ["return"]),
    # trial 2: Enter right away must be ignored (slider reset); then click the right end (1)
    7: (False, 0, ["return"]),
    8: (True, 200, []), 9: (False, 200, []),
    10: (False, 0, ["return"]),
    # trial 3: select 0.65, take a screenshot, then Escape
    11: (True, 60, []), 12: (False, 60, []),
    14: (False, 0, ["escape"]),
}
state = {"frame": 0, "down": False, "x": 0, "win": None}


class FakeMouse:
    units = "pix"
    def __init__(self, *a, **k):
        pass

    def getPressed(self, *a, **k):
        return [state["down"], False, False]

    def getPos(self):
        return (state["x"], 0)


def fake_get_keys(keyList=None, **k):
    n = state["frame"]
    if n == 13:  # trial 3, marker at 0.65 is drawn on the front buffer
        state["win"].getMovieFrame(buffer="front")
        state["win"].saveMovieFrames(str(shot))
    state["frame"] += 1
    down, x, keys = SCRIPT.get(state["frame"], (False, state["x"], []))
    state["down"], state["x"] = down, x
    return [key for key in keys if keyList is None or key in keyList]


RealWindow = visual.Window


def capturing_window(*a, **k):
    state["win"] = RealWindow(*a, **k)
    return state["win"]


RealSlider = visual.Slider


def fake_mouse_slider(*a, **k):
    slider = RealSlider(*a, **k)
    slider.mouse = FakeMouse()
    return slider


event.getKeys = fake_get_keys
visual.Window = capturing_window
visual.Slider = fake_mouse_slider

import slider_bar_psychopy as demo  # noqa: E402

try:
    demo.main()
except SystemExit:
    pass

latest = max((repo / "data").glob("slider_ratings_*.csv"), key=lambda p: p.stat().st_mtime)
rows = list(csv.DictReader(open(latest)))
print(latest)
for r in rows:
    print(r)
assert [r["status"] for r in rows] == ["completed", "completed", "aborted"], rows
assert float(rows[0]["rating"]) == 0.0, "left endpoint / zero not saved"
assert float(rows[1]["rating"]) == 1.0, "right endpoint not saved"
assert rows[2]["rating"] == "" and rows[2]["confirmation_rt_s"] == "", "aborted trial has a rating"
assert len({r["session_id"] for r in rows}) == 1
assert [r["trial_id"] for r in rows] == ["1", "2", "3"]
print("ALL CHECKS PASSED")
