import argparse
import typing
import sys
from collections import defaultdict as dd
from itertools import chain


parser = argparse.ArgumentParser(description='Load a csv of all mathches and return resulting ELO ratings.')
parser.add_argument('input_csv', metavar='input_file', type=argparse.FileType('r'), default=[sys.stdin], nargs='*', help='Input list of csv files with records of all games played. Defaults to stdin if none are given.')
parser.add_argument('-o', '--output_file', metavar='OUT', type=argparse.FileType('w'), default=sys.stdout, help='Output file. Defaults to stdout.')
parser.add_argument('-k', '--k_value', metavar='K', type=float, default=20, help='K-value determines maximum rating change after 1 game.')
parser.add_argument('-e', '--start_elo', metavar='E', type=float, default=1000, help='ELO rating of players who played 0 games.')
args = parser.parse_args()

def get_expected_score(elo_diff: float) -> float:
  """ Given the difference between elo ratings of two players return
  expected score for the first player if the two would play a game.
  The expected score for the second player is 1 - this."""
  return 1 / (1 + 10**((elo_diff) / 400))

def get_rating_update(elo_diff: float, result: float) -> float:
  """ Given the difference between elo ratings of two players return the
  change in ratings if their game ended in `result`."""
  expected = get_expected_score(elo_diff)
  return args.k_value * (result - expected)

def parse_csv(file) -> typing.Generator[typing.Tuple[str, str, float], None, None]:
  """ Parse matches one by one and yield player names and result converted
  to 0-1 range. """
  prev_id = None
  for line in file:
    try:
      match_id, p1, p2, result = line.split(',')
    except ValueError:
      sys.stderr.write('Problem parsing line: "{}"'.format(line.strip()))
      raise
    assert prev_id == None or prev_id <= match_id, 'First column should have lexicographically increasing strings. I found "{}" followed by "{}".'.format(prev_id, match_id)
    prev_id = match_id
    a, b = map(int, result.split('-'))
    yield p1.strip(), p2.strip(), 1 if a > b else 0 if a < b else 0.5

def main():
  ratings = dd(lambda: args.start_elo)
  for player1, player2, result in parse_csv(chain(*args.input_csv)):
    diff = get_rating_update(ratings[player2] - ratings[player1], result)
    ratings[player1] += diff
    ratings[player2] -= diff
  return ratings

if __name__ == '__main__':
  for team, rating in sorted(main().items(), key=lambda x: -x[1]):
    args.output_file.write('{}: {:.0f}\n'.format(team, rating))
