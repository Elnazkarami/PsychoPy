"""PsychoPy slider-rating demonstration.

Shows three neutral prompts, one per trial, each with a continuous 0-1 slider.
The participant clicks or drags on the slider, presses Enter to confirm, or
presses Escape to abort. One CSV row is written per trial, as soon as the trial
ends, so aborting keeps every trial completed before it.
"""
import csv
import uuid
from datetime import datetime
from pathlib import Path

from psychopy import core, event, visual

PROMPTS = [
    ("p1", "How easy is this sentence to read?"),
    ("p2", "How warm does the room feel right now?"),
    ("p3", "How much do you like the colour blue?"),
]

CONFIRM_KEYS = ["return", "num_enter"]
ABORT_KEY = "escape"
FIELDS = [
    "session_id",
    "trial_id",
    "prompt_id",
    "prompt_text",
    "rating",
    "confirmation_rt_s",
    "last_rating_rt_s",
    "status",
]

INSTRUCTIONS = (
    "Click or drag on the line to choose a rating.\n"
    "Press Enter to confirm your rating.\n"
    "Press Escape to quit the task."
)


def new_session_id():
    """Timestamp plus a random suffix, so two runs never share an ID or a file."""
    return f"{datetime.now():%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:6]}"


def run_trial(win, slider, prompt_stim, instructions, prompt_text):
    """Run one trial and return (status, rating, confirmation_rt_s, last_rating_rt_s).

    confirmation_rt_s: seconds from the first frame showing the prompt to the
        Enter press that confirmed the rating.
    last_rating_rt_s: slider.getRT(), seconds from the first frame the slider
        was drawn after slider.reset() to the mouse release that set the most
        recent rating. It is not the confirmation time.
    """
    slider.reset()
    prompt_stim.text = prompt_text
    event.clearEvents()

    clock = core.Clock()
    win.callOnFlip(clock.reset)
    while True:
        prompt_stim.draw()
        slider.draw()
        instructions.draw()
        win.flip()

        keys = event.getKeys(keyList=CONFIRM_KEYS + [ABORT_KEY])
        if ABORT_KEY in keys:
            return "aborted", None, None, None
        # A rating of 0 is valid, so only None counts as "no selection yet".
        rating = slider.getRating()
        if rating is not None and any(k in CONFIRM_KEYS for k in keys):
            return "completed", rating, clock.getTime(), slider.getRT()


def main():
    session_id = new_session_id()
    out_dir = Path(__file__).resolve().parent / "data"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"slider_ratings_{session_id}.csv"

    win = visual.Window([800, 600], color="white", units="pix")
    slider = visual.Slider(
        win,
        ticks=(0, 1),
        labels=["0", "1"],
        granularity=0,
        size=(400, 20),
        pos=(0, 0),
        style="rating",
        color="black",        # labels and ticks
        borderColor="black",  # the scale line
        fillColor="red",      # the marker
        labelHeight=20,
    )
    prompt_stim = visual.TextStim(win, text="", pos=(0, 150), color="black", height=24, wrapWidth=700)
    instructions = visual.TextStim(win, text=INSTRUCTIONS, pos=(0, -180), color="black", height=18, wrapWidth=700)

    # Mode "x" refuses to overwrite an existing file.
    with open(out_path, "x", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for trial_id, (prompt_id, prompt_text) in enumerate(PROMPTS, start=1):
            status, rating, confirmation_rt, last_rating_rt = run_trial(
                win, slider, prompt_stim, instructions, prompt_text
            )
            writer.writerow({
                "session_id": session_id,
                "trial_id": trial_id,
                "prompt_id": prompt_id,
                "prompt_text": prompt_text,
                "rating": "" if rating is None else f"{rating:.4f}",
                "confirmation_rt_s": "" if confirmation_rt is None else f"{confirmation_rt:.4f}",
                "last_rating_rt_s": "" if last_rating_rt is None else f"{last_rating_rt:.4f}",
                "status": status,
            })
            f.flush()
            if status == "aborted":
                break

    print(f"Saved {out_path}")
    win.close()
    core.quit()


if __name__ == "__main__":
    main()
