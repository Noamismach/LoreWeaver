
# LoreWeaver CLI

<p align="center">
  <img src="img/logo.png" alt="LoreWeaver Logo" width="180">
</p>

A simple CLI tool to track characters, aliases, and events for fictional worlds.

<p align="center">
  <img src="img/hero.webp" alt="BEEST by Hack Club" width="520">
</p>

I built this for Hack Club's BEEST program. Reading epic fantasy with massive worlds (like Sanderson or Riordan) makes you realize how hard it is to track overlapping timelines and hidden identities. I prefer the terminal over bulky GUIs, so I wrote this to handle worldbuilding straight from the command line.

## Quick Start
```bash
git clone [https://github.com/Noamismach/LoreWeaver.git](https://github.com/Noamismach/LoreWeaver.git)
cd LoreWeaver
python3 lore_manager.py
```

## Features

- Track characters, their origins, and current locations.
- Resolve aliases to see who is hiding behind a name.
- Log chronological events to a timeline.
- Zero dependencies (uses standard Python libs).

## Usage

<p align="center">
  <img src="img/cmd.png" alt="LoreWeaver CMD Demo" width="535">
</p>

Run the script and use the numbered menu to navigate:
```bash
python3 lore_manager.py
# Example: Press 1 to add a character, or 5 to view the timeline.
```

## Notes

There is no "edit" or "delete" function in the CLI menu yet. If you make a typo or want to drop a character from the lore, you'll just have to open `lore_data.json` and modify the JSON directly.
