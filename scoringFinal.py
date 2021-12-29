import numpy as np
import pandas as pd

from numpy import absolute as abs

def LoadTransform():
    picks = pd.read_csv('picks.csv')
    scores = pd.read_csv('scores.csv')

    finalScores = scores[scores['Pick'] != "none"]
    finalPicks = picks[picks['Bowl'].isin(list(finalScores['Bowl']))]
    unscoredPicks = finalPicks.merge(finalScores, on='Bowl', suffixes=('_user','_actual'))
    return unscoredPicks

def Scoring(actual, pick):
    spreadDifference = abs(pick - actual)
    if spreadDifference == 0:
        return 10
    if spreadDifference <= 3 and spreadDifference != 0:
        return 8
    if spreadDifference <= 7 and spreadDifference > 3:
        return 6
    if spreadDifference > 7:
        return 5

def Update(picks):
    newScores = []
    for index, row in picks.iterrows():
        if row['Pick_user'] == row['Pick_actual']:
            newScores.append(Scoring(row['Spread_actual'], row['Spread_user']))
        else:
            newScores.append(0)
    
    picks['Score'] = newScores
    picks.to_csv('detail.csv')

    results = picks[['Name','Score']]
    results = results.groupby(['Name'], sort=False)['Score'].sum().reset_index()
    results = results.sort_values('Score', ascending=False)
    results['Rank'] = results['Score'].rank(method='min', ascending=False)

    stringList = []
    for index, row in results.iterrows():
        stringList.append(f"{int(row['Rank'])}. {row['Name']} - {row['Score']}")
    results['String'] = stringList
    
    results.to_csv('results.csv', index=False)



def main():
    print('Loading Picks and Scores...')
    picks = LoadTransform()
    print('Updating Scoring...')
    Update(picks)
    print('Finishing Up...')

if __name__ == "__main__":
    main()