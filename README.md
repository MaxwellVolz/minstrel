# minstrel
python bot with opencv for playing music in dnd


## Setup

```sh
python3 -m venv venv

.\venv\Scripts\activate.bat

python -m pip install

deactivate
```

## Running Tests

This project uses `pytest` for automated tests, including GUI interactions with `pyautogui`. 

Navigate to the project root and execute:

```sh
pytest tests/
```


## First Goal

1. Detect Song Selection Key Press (E)
2. Attempt to determine song on release

## Spell Orders

### General

1. Allegro
2. Rousing Rhythms
3. Shriek of Weakness
4. Din of Darkness

### Chasing

1. Allegro
2. Beats of Alacrity
3. Din of Darkness

## Songs and Note Skipping

| Instrument | Song               | Total Notes | To Skip |
| ---------- | ------------------ | ----------- | ------- |
| Drum       | Rousing Rhythm     | 4           | any     |
| Drum       | Din of Darkness    | 7           | 2       |
| Drum       | Beats of Alacrity  | 4           | 1       |
| Drum       | Allegro            |             | any     |
| Drum       | Accel              |             | any     |
| Flute      | Shriek of Weakness | 3           | 1       |

### Allegro

- 4 notes, skip 2

### Din of Darkness

- 7 notes, skip 2 and 4

### Shriek of Weakness

- 3 notes
- skip 1

### Beats of Al

- 4 notes
- skip 1