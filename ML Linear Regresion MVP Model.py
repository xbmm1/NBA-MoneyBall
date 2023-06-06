# Player data
player_data = [
    {
        'name': 'Player A',
        'versatility_index': 10.2,
        'per': 28.6,
        'ts_percentage': 0.650,
        'bpm': 6.5,
        'ws': 4.2
    },
    {
        'name': 'Player B',
        'versatility_index': 8.7,
        'per': 26.3,
        'ts_percentage': 0.620,
        'bpm': 5.9,
        'ws': 3.9
    },
    # Add more players' data here
]

# Weightings for each metric
weight_versatility_index = 0.2
weight_per = 0.2
weight_ts_percentage = 0.2
weight_bpm = 0.2
weight_ws = 0.2

# Calculate MVP score for each player
for player in player_data:
    mvp_score = (
        weight_versatility_index * player['versatility_index'] +
        weight_per * player['per'] +
        weight_ts_percentage * player['ts_percentage'] +
        weight_bpm * player['bpm'] +
        weight_ws * player['ws']
    )
    player['mvp_score'] = mvp_score

# Sort players by MVP score in descending order
player_data.sort(key=lambda x: x['mvp_score'], reverse=True)

# Print the predicted MVP
print("Predicted MVP of the 2023 NBA Finals:")
print(player_data[0]['name'])
