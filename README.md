# PsychoPy Codes for Human Psychophysics Test Design

This repository contains a collection of useful PsychoPy scripts for designing and implementing psychophysical tests in human research. These scripts cover various aspects of test design, including interactive elements, response collection, and data handling.

##  Project Overview

PsychoPy is a powerful tool for creating experiments in Python, and this repository provides example codes to assist in the development of psychophysical tests. The provided scripts can be used to create interactive stimuli, collect participant responses, and analyze psychophysical data.

##  Repository Contents

- **`slider_bar_psychopy.py`**: Example script for creating an interactive slider bar where users can adjust a value by dragging the slider handle.
- **`example_2.py`**: (Add other example scripts here with brief descriptions)
- **`example_3.py`**: (Add other example scripts here with brief descriptions)

##  Requirements

- **Python**: Ensure you have Python installed.
- **PsychoPy**: Download and install PsychoPy. For installation instructions, visit [PsychoPy Installation](https://www.psychopy.org/download.html).

##  How to Use

1. **Install PsychoPy**: Install PsychoPy via pip if you haven’t already:

   pip install psychopy
  
2. **Run the Script**:
   - Save the script you want to use (e.g., `slider_bar_psychopy.py`) to your local machine.
   - Navigate to the directory containing the script.
   - Run the script using Python:
 
     python slider_bar_psychopy.py


3. **Interact with the Test Elements**:
   - Follow the instructions provided in the script to interact with the test elements.
   - For the slider bar example, click and drag the slider handle to adjust the value.
   - Press 'q' to quit the experiment.

##  Example Script: Slider Bar

### Description

The `slider_bar_psychopy.py` script demonstrates how to create an interactive slider bar using PsychoPy. The slider responds to mouse input, allowing users to adjust a value by dragging the handle.

### Script Overview

1. **Initialize PsychoPy**: Opens a PsychoPy window.
2. **Create the Slider**: Uses `visual.Slider` to create an interactive slider.
3. **Instructions**: Displays instructions using `visual.TextStim`.
4. **Main Loop**:
   - Draws the slider and updates its value based on mouse position.
   - Checks for the 'q' key to exit the loop.
5. **Get the Slider Value**: Prints the current slider value.
6. **Cleanup**: Closes the window and exits.

### Example Code

Here’s the full code for the slider bar example:


from psychopy import visual, core, event, gui

# Create a PsychoPy window
win = visual.Window([800, 600], color=[1, 1, 1], units='pix')

# Create a slider
slider = visual.Slider(win, ticks=(0, 1), labels=['0', '1'], size=(400, 20),
                       pos=(0, 0), style='rating', color='black', fillColor='red')

# Instructions
instructions = visual.TextStim(win, text='Drag the slider to adjust the value.\nPress "q" to quit.',
                               pos=(0, 250), color='black')

# Main loop
running = True
while running:
    instructions.draw()
    slider.draw()
    win.flip()

    # Check for mouse clicks
    mouse = event.Mouse()
    if mouse.isPressedIn(slider):
        slider.setRating(mouse.getPos()[0] / slider.size[0])
        
    # Check for exit condition
    keys = event.getKeys()
    if 'q' in keys:
        running = False

# Get the slider value
slider_value = slider.getRating()
print(f'Slider Value: {slider_value}')

# Cleanup
win.close()
core.quit()


##  Contributing

Contributions are welcome! If you have additional PsychoPy scripts or improvements, please fork the repository, make changes, and submit a pull request. For significant changes, open an issue to discuss your proposed modifications.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

