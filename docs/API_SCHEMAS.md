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
| element | The manager id | integer |
| position | The position of the player in the team. GK = 1, 12, Outfield depends on the formation being played.  | integer |
| is_captain | Has the player been captained this week (NA in Draft) | integer |
| is_vice_captain | Has the player been vice-captained this week (NA in Draft) | integer  |
| multiplier | multiplier based on captain, vice-captain etc. (NA in Draft) | integer  |

# League Details - api/league/{league_id}/details
Example: https://draft.premierleague.com/api/league/41747/details

## League

## League Entries
List of dictionaries containing the details of a Draft team

Example:
```
league_entries: [
    {
        entry_id: 164273,
        entry_name: "Boom Xhaka Laka",
        id: 164651,
        joined_time: "2020-09-01T18:27:43.454935Z",
        player_first_name: "Jack",
        player_last_name: "Chandler",
        short_name: "JC",
        waiver_pick: null
    },
    {
        entry_id: 166238,
        entry_name: "Bilbao Baggins",
        id: 166625,
        joined_time: "2020-09-01T21:09:27.382849Z",
        player_first_name: "Oliver",
        player_last_name: "Bignall",
        short_name: "OB",
        waiver_pick: null
    },
]

```

| column_name  | description  | data_type  |
|---|---|---|
| entry_id | the Draft team ID | integer |
| entry_name | The Draft team name  | string |
| id | The ID | integer |
| joined_time | When the manager joined the league | datetime  |
| player_first_name | First name of the Draft manager | string  |
| player_last_name | Surname name of the Draft manager | string  |
| short_name | Draft manager initials | integer  |
| waiver_pick | What number is the manager in the current draft pick | integer  |


## Standings

Example:
```
standings: [
    {
        event_total: 49,
        last_rank: 1,
        league_entry: 166704,
        rank: 1,
        rank_sort: 1,
        total: 1790
    },
    {
        event_total: 58,
        last_rank: 4,
        league_entry: 166625,
        rank: 2,
        rank_sort: 2,
        total: 1684
    }
]
```

# Game Week Manager Details - api/event/{game_week}/live
Example: https://draft.premierleague.com/api/event/34/live

# Fixtures Details - api/fixtures/?event={game_week}
Example: https://fantasy.premierleague.com/api/fixtures/?event=34

# Player Details - api/bootstrap-static
A full list of all available players in FPL

Example: https://draft.premierleague.com/api/bootstrap-static