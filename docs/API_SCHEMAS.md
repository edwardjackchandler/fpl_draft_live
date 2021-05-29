# Game Week League Details - api/entry/{team_id}/event{game_week}
Example: https://draft.premierleague.com/api/entry/169801/event/34

## Picks
List of picks for an individual Game Week.
15 positions.

Example:
```
picks: [
    {
        element: 383,
        position: 1,
        is_captain: false,
        is_vice_captain: false,
        multiplier: 1
    },
...
    {
        element: 495,
        position: 15,
        is_captain: false,
        is_vice_captain: false,
        multiplier: 1
    }
]
```

| column_name  | description  | data_type  |
|---|---|---|
| element | The player id | integer |
| position | The position of the player in the team. GK = 1, 12, Outfield depends on the formation being played.  | integer |
| is_captain | Has the player been captained this week (NA in Draft) | integer |
| is_vice_captain | Has the player been vice-captained this week (NA in Draft) | integer  |
| multiplier | multiplier based on captain, vice-captain etc. (NA in Draft) | integer  |

# League Details - api/league/{league_id}/details
Example: https://draft.premierleague.com/api/league/41747/details

# Game Week Player Details - api/event/{game_week}/live
Example: https://draft.premierleague.com/api/event/34/live

# Fixtures Details - api/fixtures/?event={game_week}
Example: https://fantasy.premierleague.com/api/fixtures/?event=34