# OrbitalWitness Interview Task

This repository is a response to the OrbitalWitness interview task.

I Have chosen to approach the sample JSON file included.

## Plan of works

Before undertaking a task I like to plan it out a little.

I Also am fairly against code comments as they tend to not be that well maintained over time, unless there are processes and integrations I would not have time to set up.

### Running

This project assumes you have a recent Python on your machine and will not guide the install of. It uses virtualenv to isolate dependencies `pip install virtualenv`.

You can create a new virtualenv by running `virtualenv .venv` or `python -m virtualenv .`.

If you run a system with multiple python runtimes, please ensure you use python 3.6 with pip 20.1 or greater.

You can run `. .venv/bin/activate` on recent Linux & OSx shells, or `. .venv/Scripts/activate` if you use Windows.

The project also documents requirements `pip install requirements.txt` and development-requirements `pip install requirements-dev.txt`. Dev requirements automatically install runtime requirements, although there would be no problem running both.

The entrypoint is main.py, which can be run using `python main.py`.

### Testing

I've chosen to use Pytest testing framework. from within the activated virtual environment, you should be able to use `pytest .` or `python -m py.test .`.

### High level bullet point

1. receive json
2. parse to json structure
3. remove noisy outer layers and repetition
4. enumerate to keep position (preserve other context)
    a. scheduleType is always the same
5. iterate over entries
6. enumerate to keep position (preserve other context)
    a. it's a list no context aside from position
7. check for context
    a. there is an index, which seems to be local (can use enumerate)
    b. there is an entryDate which is always blank
    c. there is an entryType which can be one of two unique values
    d. entryText seems to be a list of strings
8. join all entryText lines with newline
9. chop, explode, split (separate) on 'NOTE' string literal
    a. after Notes begin, content seems to have ended, suggesting envelope header format
    b. some preliminary investigation suggests this is stable
10. take first item away (this is text content)
11. join notes back with 'NOTE' while keeping separate.
    a. keeps all of the line for a note with that note.
12. send first item for text processing
    a. The above separates notes, and also allows the least possible decision making
13. for every non-note (1 per entry), use regex to split apart lines
    a. this is known not to be good enough but gives some benefits
    b. if we can keep each line and column separate we can support re-ordering
14. create a list of 4 lists (one per column)
15. merge each item into the correct list placement
16. adjust for two error cases where 5 columns are made.
17. investigate alternatives
    a. regex for title number
    b. Look at fixed width columns
        i. problem with # of columns
    c. parenthesis / continuation word balancing...
