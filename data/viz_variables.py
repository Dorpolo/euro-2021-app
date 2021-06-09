import pandas as pd

FAMILY_FONT = 'sans-serif'
FONT_COL = 'black'
t = [[f"{h}-{h-j_start}" for h in range(j_start, (j_start+6))] for j_start in range(0, 10)]
SCORE_LIST = [item for sublist in t for item in sublist]
SCORE_MAP_DF = pd.DataFrame([[j, i] for i, j in enumerate(SCORE_LIST)]).rename(columns={0: 'score', 1: 'score_rank'})
SCORE_WINNER_DF = pd.DataFrame({'winner': ['home', 'draw', 'away'], 'winner_rank': [0, 1, 2]})