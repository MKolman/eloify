import argparse
import typing
from collections import defaultdict as dd


parser = argparse.ArgumentParser(description='Load a csv of all mathches and return resulting ELO ratings.')
parser.add_argument('--input_csv', type=str, default='', help='Input csv with the list of all games played.')
parser.add_argument('--k', type=float, default=20, help='K-value determines maximum rating change after 1 game.')
parser.add_argument('--elo', type=float, default=1000, help='ELO rating of players who played 0 games.')
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
  return args.k * (result - expected)

def parse_csv(file) -> typing.Generator[typing.Tuple[str, str, float], None, None]:
  """ Parse matches one by one and yield player names and result converted
  to 0-1 range. """
  for line in file:
    _, p1, p2, result = line.split(',')
    a, b = map(int, result.split('-'))
    yield p1.strip(), p2.strip(), 1 if a > b else 0 if a < b else 0.5

def main():
  ratings = dd(lambda: args.elo)
  with open(args.input_csv) as f:
    for player1, player2, result in parse_csv(f):
      diff = get_rating_update(ratings[player2] - ratings[player1], result)
      ratings[player1] += diff
      ratings[player2] -= diff
  return ratings

if __name__ == '__main__':
  for team, rating in sorted(main().items(), key=lambda x: -x[1]):
    print('{}: {:.0f}'.format(team, rating))