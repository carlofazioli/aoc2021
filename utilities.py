from datetime import datetime
from pathlib import Path
import requests

YEAR = datetime.today().year
DAY = datetime.today().day


def load_data(year=YEAR, day=DAY):
    input_file = Path(f'./input_data/day_{day}.txt')
    if not input_file.exists():
        with open('./.aoc_cookie', 'r') as f:
            aoc_cookie = f.read().strip()
        url = f'https://adventofcode.com/{year}/day/{day}/input'
        response = requests.get(url, cookies={'session': aoc_cookie})
        with open(input_file, 'w') as f:
            f.write(response.text)

    with open(input_file, 'r') as f:
        input_data = f.read().strip()
    return input_data


def submit(answer, part, year=YEAR, day=DAY):
    url = f'https://adventofcode.com/{year}/day/{day}/answer'
    payload = {'level': part, 'answer': answer}
    with open('./.aoc_cookie', 'r') as f:
        aoc_cookie = f.read().strip()
    response = requests.post(url, payload, cookies={'session': aoc_cookie})
    if 'That\'s the right answer!' in response.text:
        print(f'Fucken sick bro you got part {part}!')
    elif 'You don\'t seem to be solving the right level.' in response.text:
        print(f'Ya already solved part {part} knucklehead.')
    else:
        print('Incorrect!  Keep trying!')
    return response
