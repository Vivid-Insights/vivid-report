# Judging task

You are judging answers written for a scout at a football club, who asked questions
about one player. Below are the information about the player, the explanations and
rule-based descriptions for each question, and then 30 answers, each with an id.

Rate each answer on its own, against the information for its question. Do not compare
answers with each other, and do not try to work out who wrote them.

Rate three criteria, each from 1 (very poor) to 5 (very good):
- faithfulness: how faithfully the answer represents the information given;
- engagement: an engaging answer tells the scout about the player in footballing terms,
  without overwhelming them with numbers and statistics. If it gives a number, it does so
  in the context of comparing the player with other players;
- usefulness: an answer is only useful if it compares the player with other, similar
  players. If it gives numbers, it explains what they mean.
Also list every hallucination in the answer, that is every unsupported or fabricated claim:
a statement the information does not support or that contradicts it. Quote each briefly.

Write your ratings to the results file named at the end, one JSON object per line, one
line per answer, in this form:
{"id": "...", "faithfulness": 1-5, "engagement": 1-5, "usefulness": 1-5, "hallucinations": ["..."], "reason": "one or two sentences"}


## Data about the player
Player: Dani Ortolan (full name Daniela Maria Lopes Ortolan), striker, Brazilian Brasileiro Women 2026, 1253 minutes.
z-scores compare the player with players in the same position in Brazilian Brasileiro Women 2026 (0 = average, positive = above average).

Qualities (z-score):
- Active Defence: -1.646
- Aerial Threat: -0.356
- Box Threat: -0.615
- Chance Prevention: 0.407
- Composure: -0.79
- Defensive Heading: 0.547
- Dribbling: -1.067
- Effectiveness: -2.081
- Finishing: 0.691
- Hold Up Play: -1.148
- Intelligent Defence: -1.121
- Involvement: -2.144
- Passing Quality: -1.705
- Poaching: 0.421
- Pressing: -1.331
- Progression: -1.77
- Providing Teammates: -1.368
- Run Quality: -0.674
- Territorial Dominance: 0.244
- Winning Duels: -1.712

Metrics (value per 90 minutes or share, and z-score):
- Aerials: 4.886 (z = 1.104)
- Aerials won: 1.581 (z = 0.51)
- Aerials won %: 0.324 (z = -0.422)
- Assists: 0.0 (z = -0.879)
- Attacking aerials: 4.344 (z = 0.962)
- Attacking aerials won: 1.193 (z = 0.278)
- Attacking aerials won %: 0.275 (z = -0.635)
- Ball progression (xT): 0.019 (z = -1.668)
- Loose ball recoveries: 0.373 (z = -1.652)
- Ball runs (xT): 0.008 (z = -0.891)
- Box entries from carries: 0.17 (z = -0.751)
- Carries: 19.0 (z = -1.085)
- Carries (xT): 0.029 (z = -1.148)
- Carries (xT) per 100 receptions: 0.143 (z = -1.028)
- Counterpressing actions: 0.994 (z = 0.064)
- Chance creating passes: 0.341 (z = -1.282)
- Crosses (xT): 0.005 (z = -0.755)
- Deep completions: 0.0 (z = -0.951)
- Through ball receptions (xT): 0.024 (z = 0.128)
- Defending 1v1: 0.248 (z = -0.743)
- Defending 1v1s won %: 0.5 (z = 0.262)
- Defensive actions won: 1.739 (z = -1.537)
- Defensive aerials: 2.174 (z = 0.999)
- Defensive aerials won: 0.932 (z = 1.006)
- Defensive aerials won %: 0.429 (z = 0.246)
- Defensive area adj (m^2): 0.0 (z = -0.406)
- Defensive area (m^2): 0.0 (z = -0.406)
- Defensive duels: 4.597 (z = -0.832)
- Defensive ground duels won: 1.118 (z = -1.493)
- Defensive ground duels won %: 0.243 (z = -1.777)
- Defensive intensity: 2.982 (z = -1.016)
- Defensive action height (m): 53.595 (z = -0.137)
- Dribbles: 0.426 (z = -1.268)
- Dribble success %: 0.8 (z = 0.271)
- Successful dribbles: 0.341 (z = -1.226)
- Dribbles (xT): 0.012 (z = -1.094)
- np Goals - np xG: 1.011 (z = 0.747)
- np Goals per box touch: 0.2 (z = 1.213)
- Headed plays: 0.511 (z = -0.448)
- High recoveries: 0.124 (z = -1.693)
- Low turnovers: 0.596 (z = -0.671)
- Low turnovers per low reception: 0.2 (z = -0.991)
- Interceptions: 1.802 (z = -0.501)
- Key passes: 0.17 (z = -0.948)
- Linkups: 0.256 (z = -0.749)
- Long ball receptions: 1.437 (z = -0.631)
- Long ball receptions (xT): 0.027 (z = -0.742)
- Ball losses: 5.111 (z = 1.309)
- Low receptions: 2.515 (z = -0.523)
- np Goals: 0.256 (z = 0.236)
- Shots: 1.278 (z = -1.026)
- Opp. possessions: 1351.0 (z = 0.289)
- Possessions: 310.0 (z = -0.174)
- Opp. Pass success % into defensive area: 0.0 (z = 0.468)
- Opp. Possession %: 0.578 (z = 1.279)
- Opposition possessions in defensive area: 0.0 (z = -0.324)
- Opp. Progressive passes from defensive area %: 0.0 (z = 0.433)
- Opp. touches: 10224.0 (z = 0.657)
- Opp. xG after defensive action raw: 0.0 (z = 0.178)
- Opp. xG after defensive action: 0.0 (z = 0.203)
- Opp. xG from defensive area raw: 0.0 (z = 0.286)
- Opp. xG from defensive area: 0.0 (z = 0.336)
- Allowed xT from defensive area: 0.0 (z = 0.307)
- Opp. xT from defensive area: 0.0 (z = 0.455)
- Opp. xT into defensive area: 0.0 (z = 0.441)
- Passes: 163.0 (z = -0.689)
- Passes into defensive area: 0.0 (z = -0.32)
- Passes into final third (xT): 0.004 (z = -1.095)
- Passes in final third (xT): 0.047 (z = -1.606)
- Passes (xT): 0.082 (z = -1.779)
- Passes (xT) per 100 receptions: 0.411 (z = -1.973)
- Box receptions: 2.215 (z = -0.313)
- Minutes: 1252.67 (z = 0.428)
- Playmaking passes: 0.681 (z = -1.73)
- Possession %: 0.422 (z = -1.279)
- Recoveries: 0.808 (z = -1.426)
- Recoveries per opponent possession: 0.01 (z = -1.211)
- Pressure resistance %: 0.618 (z = -1.293)
- Progressive passes inside: 0.0 (z = -0.301)
- Receptions: 20.018 (z = -1.147)
- Second assists: 0.0 (z = -0.709)
- np Shot conversion %: 0.2 (z = 1.074)
- Start inside: 0.0 (z = -0.304)
- Defending 1v1s won: 0.124 (z = -0.451)
- Successful passes into defensive area: 0.0 (z = -0.317)
- Tackles won %: 0.439 (z = -1.233)
- Team touches: 7456.0 (z = -0.04)
- Touches: 15.674 (z = -1.97)
- Touches in box: 1.278 (z = -1.126)
- True tackles: 2.547 (z = -1.209)
- Tackles won: 1.118 (z = -1.493)
- Under pressure: 5.792 (z = 0.922)
- Under pressure retention: 3.578 (z = 0.36)
- xA: 0.011 (z = -1.209)
- np xG: 0.169 (z = -0.667)
- xGBuildup: 0.042 (z = -1.598)
- xG Chain: 0.187 (z = -1.54)
- xGChain per possession: 0.008 (z = -1.511)
- xGCreated: 0.011 (z = -1.405)
- xGDribble: 0.004 (z = -0.861)
- xGOT: 0.148 (z = -0.551)
- np xG per box touch: 0.133 (z = 0.688)
- np xG per shot: 0.133 (z = 0.151)
- np xG + xA per 100 touches: 1.148 (z = -0.429)
- xT Into Area: 0.0 (z = 0.293)

Zones of the pitch: for each quality, the z-score of its pitch metric in each zone, against players in the same position:
- Providing Teammates (xGCreated): own penalty area -0.164, attacking central midfield -0.874, defensive right wing -0.12, defensive right half-space -0.129, defensive left half-space -0.121, defensive central midfield -0.163, attacking left half-space -0.636, attacking left wing -0.503, attacking right wing -0.568, attacking right half-space -0.635, defensive left wing -0.14, opposition penalty area -0.944
- Aerial Threat (Attacking aerials won): opposition penalty area -0.164, defensive right wing 2.143, defensive right half-space 0.883, defensive left wing -0.456, defensive left half-space -0.537, defensive central midfield -0.581, attacking right wing 0.071, attacking right half-space -0.106, attacking left wing 1.291, attacking left half-space 1.367, attacking central midfield -0.309
- Involvement (xGBuildup): own penalty area -0.207, opposition penalty area -0.461, defensive right wing -0.417, defensive right half-space -0.539, defensive left half-space -0.675, defensive left wing -0.516, attacking central midfield -0.403, attacking left wing -0.692, attacking right half-space -0.802, attacking right wing -0.756, defensive central midfield -0.475, attacking left half-space -0.888
- Composure (Pressure resistance %): defensive right wing -1.223, defensive right half-space 0.181, defensive left wing -0.962, defensive left half-space 1.164, defensive central midfield -0.359, attacking right wing -2.041, attacking right half-space -0.889, attacking left wing -1.48, attacking left half-space 1.009, attacking central midfield 0.662
- Run Quality (Carries (xT)): attacking central midfield 0.314, attacking left half-space -1.047, attacking left wing -0.948, attacking right half-space -1.076, attacking right wing -0.723, defensive central midfield -0.589, defensive left half-space -0.546, defensive left wing -0.733, defensive right half-space -0.832, defensive right wing -0.576, opposition penalty area -0.111, own penalty area -0.331
- Hold Up Play (Under pressure retention): attacking central midfield -0.371, attacking left half-space 0.233, attacking left wing -0.493, attacking right half-space 0.15, attacking right wing -0.812, defensive central midfield 1.684, defensive left half-space 1.766, defensive left wing -0.067, defensive right half-space 0.075, defensive right wing -0.791, own penalty area -0.603
- Active Defence (Defensive actions won): opposition penalty area -1.055, own penalty area 0.679, attacking central midfield -0.516, attacking left half-space -0.959, defensive right wing -0.968, attacking left wing 0.171, attacking right wing -1.201, defensive central midfield -0.709, attacking right half-space -1.472, defensive right half-space -0.23, defensive left wing -0.453, defensive left half-space -0.74
- Effectiveness (np xG per shot): opposition penalty area 0.808, attacking central midfield -0.941, attacking right half-space 0.972, attacking left half-space 0.213, golden zone -0.669, outside of the box -0.35, six yard box 0.078
- Dribbling (Dribbles (xT)): own penalty area -0.198, opposition penalty area -1.126, defensive right wing -0.447, defensive right half-space -0.518, defensive left wing -0.651, defensive left half-space -0.483, defensive central midfield -0.646, attacking right wing -0.771, attacking right half-space -0.517, attacking left wing -0.739, attacking left half-space -1.313, attacking central midfield 0.697
- Intelligent Defence (Loose ball recoveries): own penalty area -0.752, opposition penalty area -0.601, defensive right wing -0.859, defensive right half-space 0.175, defensive left wing -0.676, defensive left half-space 0.613, defensive central midfield -0.32, attacking right wing -0.097, attacking right half-space -0.905, attacking left wing -0.171, attacking left half-space -0.929, attacking central midfield -1.103
- Defensive Heading (Defensive aerials won): attacking central midfield -0.525, attacking left half-space 2.025, attacking left wing 1.51, attacking right half-space -0.436, attacking right wing 1.608, defensive central midfield 1.857, defensive left half-space -0.665, defensive left wing 1.104, defensive right half-space 0.145, defensive right wing 0.963, own penalty area 0.729
- Winning Duels (Defensive ground duels won): defensive left half-space -0.968, defensive left wing -0.739, defensive right half-space -0.13, defensive right wing 0.011, opposition penalty area 0.402, own penalty area -0.611, attacking central midfield -0.934, attacking left half-space -0.631, attacking left wing -0.053, attacking right half-space -1.304, attacking right wing -1.004, defensive central midfield -0.136
- Passing Quality (Passes (xT)): defensive left wing -1.087, defensive left half-space -0.211, defensive central midfield -0.005, attacking right wing -0.952, attacking right half-space -1.497, attacking left wing -1.029, attacking left half-space -1.094, attacking central midfield -0.597, own penalty area -0.79, opposition penalty area -1.113, defensive right half-space -0.508, defensive right wing -0.965
- Progression (Playmaking passes): attacking central midfield -0.97, attacking left half-space -0.82, attacking left wing -1.051, attacking right half-space -1.132, attacking right wing -0.826, defensive central midfield -0.775, defensive left half-space -0.12, defensive left wing -0.664, defensive right wing -0.876, opposition penalty area -0.916, own penalty area -0.278, defensive right half-space -0.656
- Pressing (Defensive intensity): own penalty area 1.091, attacking central midfield 0.34, attacking left half-space -0.003, attacking left wing -0.234, attacking right half-space -1.248, attacking right wing -0.995, defensive central midfield 0.027, defensive left half-space -0.841, defensive left wing -0.392, defensive right half-space -0.175, defensive right wing -0.812, opposition penalty area -0.016
- Poaching (np xG): attacking central midfield -0.812, attacking left wing -0.251, attacking right half-space 0.867, attacking right wing -0.201, defensive central midfield -0.165, defensive left half-space -0.12, defensive right wing -0.12, opposition penalty area -0.585, attacking left half-space 0.202, outside of the box -0.549, golden zone -0.85, six yard box -0.308
- Finishing (np Shot conversion %): outside of the box 1.476, golden zone 0.148, six yard box -0.014

From Twelve's data (get_players_by_id):
player_id: 688425; short_name: Dani Ortolan; full_name: Daniela Maria Lopes Ortolan; last_name: Lopes Ortolan; birth_date: 1998-07-26; age: 28.229979466119097; foot: unknown; image_url: https://cdn5.wyscout.com/photos/players/public/g-201192_100x130.png; nationality: Brazil; birth_country: Brazil

From Twelve's data (get_player_career):
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 35074; season: 2026; season_minutes: 1252.67; is_domestic_league_competition: True; is_competition_season_completed: True; position: CF; position_minutes: 823.01; minutes_pct: 65.7; current: True; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 35074; season: 2026; season_minutes: 1252.67; is_domestic_league_competition: True; is_competition_season_completed: True; position: SS; position_minutes: 407.19; minutes_pct: 32.51; current: True; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 35074; season: 2026; season_minutes: 1252.67; is_domestic_league_competition: True; is_competition_season_completed: True; position: LW; position_minutes: 12.17; minutes_pct: 0.97; current: True; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 35074; season: 2026; season_minutes: 1252.67; is_domestic_league_competition: True; is_competition_season_completed: True; position: RW; position_minutes: 10.3; minutes_pct: 0.82; current: True; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 58488; season: 2024; season_minutes: 15.63; is_domestic_league_competition: True; is_competition_season_completed: True; position: LW; position_minutes: 15.63; minutes_pct: 100.0; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 58488; season: 2023; season_minutes: 412.96; is_domestic_league_competition: True; is_competition_season_completed: True; position: CF; position_minutes: 376.18; minutes_pct: 91.09; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 58488; season: 2023; season_minutes: 412.96; is_domestic_league_competition: True; is_competition_season_completed: True; position: SS; position_minutes: 33.3; minutes_pct: 8.06; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 58488; season: 2023; season_minutes: 412.96; is_domestic_league_competition: True; is_competition_season_completed: True; position: LCMF; position_minutes: 3.48; minutes_pct: 0.84; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 58488; season: 2022; season_minutes: 537.49; is_domestic_league_competition: True; is_competition_season_completed: True; position: CF; position_minutes: 434.61; minutes_pct: 80.86; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 58488; season: 2022; season_minutes: 537.49; is_domestic_league_competition: True; is_competition_season_completed: True; position: SS; position_minutes: 90.96; minutes_pct: 16.92; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 58488; season: 2022; season_minutes: 537.49; is_domestic_league_competition: True; is_competition_season_completed: True; position: RW; position_minutes: 9.22; minutes_pct: 1.72; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 58488; season: 2022; season_minutes: 537.49; is_domestic_league_competition: True; is_competition_season_completed: True; position: LCMF; position_minutes: 2.7; minutes_pct: 0.5; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 43370; competition: 43370; team_id: 58488; season: 2022; season_minutes: 55.33; is_domestic_league_competition: False; is_competition_season_completed: True; position: CF; position_minutes: 55.33; minutes_pct: 100.0; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 30655; season: 2021; season_minutes: 598.51; is_domestic_league_competition: True; is_competition_season_completed: True; position: CF; position_minutes: 321.97; minutes_pct: 53.8; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 30655; season: 2021; season_minutes: 598.51; is_domestic_league_competition: True; is_competition_season_completed: True; position: LW; position_minutes: 96.17; minutes_pct: 16.07; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 30655; season: 2021; season_minutes: 598.51; is_domestic_league_competition: True; is_competition_season_completed: True; position: RW; position_minutes: 68.77; minutes_pct: 11.49; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 30655; season: 2021; season_minutes: 598.51; is_domestic_league_competition: True; is_competition_season_completed: True; position: LAMF; position_minutes: 65.7; minutes_pct: 10.98; current: False; is_national_team_competition: False; is_youth_team_competition: False
player_id: 688425; competition_id: 1468; competition: 1468; team_id: 30655; season: 2021; season_minutes: 598.51; is_domestic_league_competition: True; is_competition_season_completed: True; position: RWF; position_minutes: 45.9; minutes_pct: 7.67; current: False; is_national_team_competitio
(cut)

From Twelve's data (get_player_match_metrics):
competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: CF; player_position_match_minutes_p90: 823.01; possession_pct: 0.3940692307692308; team_events: 4841; opp_team_events: 6853; passes: 115; passes_accurate: 83; pass_accuracy_pct: 0.7217; passes_open_play: 115; passes_accurate_open_play: 83; progressive_passes: 3; passes_into_final_third: 1; through_passes: 1; through_passes_accurate: 0; smart_passes: 0; smart_passes_accurate: 0; crosses: 4; crosses_accurate: 1; key_passes: 2; assists: 0; shot_assists: 4; second_assists: 0; creative_passes: 4; linkups: 3; playmaking_passes: 4; deep_completions: 0; passes_xt: 0.6524; passes_into_third_xt: 0.0142; passes_third_xt: 0.3889; crosses_xt: 0.0088; xa: 0.1234; receptions: 153; low_receptions: 23; penalty_area_receptions: 19; long_ball_receptions: 14; long_ball_receptions_xt: 0.3014; deep_runs_xt: 0.2785; shots: 12; np_shots: 10; shots_on_target: 4; shot_on_target_pct: 0.4; goals: 3; np_goals: 2; own_goals: 0; shot_conversion_pct: 0.2; xg: 1.6028; xg_on_target: 1.4122; goals_minus_xg: 0.3972; xg_per_shot: 0.1603; carries: 12; carries_successful: 12; accelerations: 0; carries_xt: 0.2324; ball_runs_xt: 0.0272; dribbles_xt: 0.1226; ball_progression_xt: 0.0859; box_entries: 1; touches: 128; touches_in_box: 12; goals_per_box_touch: 0.1667; xg_per_box_touch: 0.1336; xg_plus_xa_per_100_touches: 1.3486; dribbles: 3; dribbles_successful: 3; dribbles_success_pct: 1.0; interceptions: 15; ball_recoveries: 5; high_recoveries: 1; possessions_won: 11; possessions_won_per_opponent_possession: 0.0127; num_opponent_possessions: 865; num_team_possessions: 843; possession_count: 1708; clearances: 4; defensive_duels: 45; defensive_duels_won: 12; defensive_duels_won_pct: 0.2667; true_tackles: 21; true_tackles_won: 12; tackle_success_pct: 0.5714; defensive_intensity: 28; defensive_actions: 19; defensive_line_height_m: 51.05; aerials: 45; aerials_won: 15; aerials_won_pct: 0.3333; attacking_aerials: 36; attacking_aerials_won: 11; attacking_aerials_won_pct: 0.3056; defensive_aerials: 23; defensive_aerials_won: 10; defensive_aerials_won_pct: 0.4348; headed_plays: 5; losses: 44; high_turnovers: 4; num_low_turnovers: 4; high_turnovers_per_low_reception: 0.1739; num_low_turnovers_per_low_reception: 0.1739; carries_xt_per_100_receptions: 0.1519; passes_xt_per_100_receptions: 0.4264; corners: 0; free_kicks: 1; goal_kicks: 0; penalties_taken: 2; penalties_scored: 1; fouls_committed: 10; fouls_suffered: 20; yellow_cards: 2; red_cards: 0; defending_1v1: 2; successful_1v1: 2; defending_1v1_pct: 1.0; under_pressure_actions: 44; under_pressure_retention: 26; pressure_resistance_pct: 0.5909; counterpressing: 7; num_counterpresses: 7; num_counterpresses_leading_to_recovery: 1; xg_created: 0.1286; xg_dribble: 0.0474; xg_buildup: 0.3948; xg_chain: 2.1207; xg_chain_per_possession: 0.0102; num_possessions_involved: 207
competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: LW; player_position_match_minutes_p90: 12.17; possession_pct: 0.3641; team_events: 67; opp_team_events: 117; passes: 2; passes_accurate: 0; pass_accuracy_pct: 0.0; passes_open_play: 2; passes_accurate_open_play: 0; progressive_passes: 0; passes_into_final_third: 0; through_passes: 0; through_passes_accurate: 0; smart_passes: 0; smart_passes_accurate: 0; crosses: 0; crosses_accurate: 0; key_passes: 0; assists: 0; shot_assists: 0; second_assists: 0; creative_passes: 0; linkups: 0; playmaking_passes: 0; deep_completions: 0; passes_xt: 0.0; passes_into_third_xt: 0.0; passes_third_xt: 0.0; crosses_xt: 0.0; xa: 0.0; receptions: 2; low_receptions: 0; penalty_area_receptions: 0; long_ball_receptions: 0; long_ball_receptions_xt: 0.0; deep_runs_xt: 0.0; shots: 1; np_shots: 1; shots_on_target: 0; shot_on_target_pct: 0.0; goals: 0; np_goals: 0; own_goals: 0; shot_conversion_pct: 0.0; xg: 0.0684; xg_on_target: 0.0; goals_minus_xg: -0.0684; xg_per_shot: 0.0684; carries: 0; carries_successful: 0; accelerations: 0; carries_xt: 0.0; ball_runs_xt: 0.0; dribbles_xt: 0.0; ball_progression_xt: 0.0; box_entries: 0; touches: 2; touches_in_box: 0; xg_plus_xa_per_100_touches: 3.42; dribbles: 0; dribbles_successful: 0; interceptions: 1; ball_recoveries: 0; high_recoveries: 0; possessions_won: 0; possessions_won_per_opponent_possession: 0.0; num_opponent_possessions: 17; num_team_possessions: 15; possession_count: 32; clearances: 0; defensive_duels: 2; defensive_duels_won: 1; defensive_duels_won_pct: 0.5; true_tackles: 2; true_tackles_won: 1; tackle_success_pct: 0.5; defensive_intensity: 2; defensive_actions: 1; defensive_line_height_m: 39.2; aerials: 1; aerials_won: 1; aerials_won_pct: 1.0; attacking_aerials: 0; attacking_aerials_won: 0; defensive_aerials: 1; defensive_aerials_won: 1; defensive_aerials_won_pct: 1.0; headed_plays: 0; losses: 1; high_turnovers: 0; num_low_turnovers: 0; carries_xt_per_100_receptions: 0.0; passes_xt_per_100_receptions: 0.0; corners: 0; free_kicks: 0; goal_kicks: 0; penalties_taken: 0; penalties_scored: 0; fouls_committed: 0; fouls_suffered: 0; yellow_cards: 0; red_cards: 0; defending_1v1: 0; successful_1v1: 0; under_pressure_actions: 0; under_pressure_retention: 0; counterpressing: 1; num_counterpresses: 1; num_counterpresses_leading_to_recovery: 0; xg_created: 0.0; xg_dribble: 0.0; xg_buildup: 0.0; xg_chain: 0.0684; xg_chain_per_possession: 0.0228; num_possessions_involved: 3
competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: RW; player_position_match_minutes_p90: 10.3; possession_pct: 0.2342; team_events: 37; opp_team_events: 121; passes: 1; passes_accurate: 1; pass_accuracy_pct: 1.0; passes_open_play: 1; passes_accurate_open_play: 1; progressive_passes: 0; passes_into_final_third: 0; through_passes: 0; through_passes_accurate: 0; smart_passes: 0; smart_passes_accurate: 0; crosses: 0; crosses_accurate: 0; key_passes: 0; assists: 0; shot_assists: 0; second_assists: 0; creative_passes: 0; linkups: 0; playmaking_passes: 0; deep_completions: 0; passes_xt: 0.0072; passes_into_third_xt: 0.0; passes_third_xt: 0.0; crosses_xt: 0.0; xa: 0.0; receptions: 1; low_receptions: 0; penalty_area_receptions: 0; long_ball_receptions: 0; long_ball_receptions_xt: 0.0; deep_runs_xt: 0.0; shots: 0; np_shots: 0; shots_on_target: 0; goals: 0; np_goals: 0; own_goals: 0; xg: 0.0; xg_on_target: 0.0; goals_minus_xg: 0.0; carries: 0; carries_successful: 0; accelerations: 0; carries_xt: 0.0; ball_runs_xt: 0.0; dribbles_xt: 0.0; ball_progression_xt: 0.0; box_entries: 0; touches: 1; touches_in_box: 0; xg_plus_xa_per_100_touches: 0.0; dribbles: 0; dribbles_successful: 0; interceptions: 0; ball_recoveries: 0; high_recoveries: 0; possessions_won: 0; possessions_won_per_opponent_possession: 0.0; num_opponent_possessions: 15; num_team_possessions: 10; possession_count: 25; clearances: 0; defensive_duels: 0; defensive_duels_won: 0; true_tackles: 0; true_tackles_won: 0; defensive_intensity: 0; defensive_actions: 0; defensive_line_height_m: 67.2; aerials: 0; aerials_won: 0; attacking_aerials: 0; attacking_aerials_won: 0; defensive_aerials: 0; defensive_aerials_won: 0; headed_plays: 0; losses: 0; high_turnovers: 0; num_low_turnovers: 0; carries_xt_per_100_receptions: 0.0; passes_xt_per_100_receptions: 0.72; corners: 0; free_kicks: 0; goal_kicks: 0; penalties_taken: 0; penalties_scored: 0; fouls_committed: 1; fouls_suffered: 0; yellow_cards: 0; red_cards: 0; defending_1v1: 0; successful_1v1: 0; under_pressure_actions: 1; under_pressure_retention: 0; pressure_resistance_pct: 0.0; counterpressing: 0; num_counterpresses: 0; num_counterpresses_leading_to_recovery: 0; xg_created: 0.0; xg_dribble: 0.0; xg_buildup: 0.0; xg_chain: 0.0; xg_chain_per_possession: 0.0; num_possessions_involved: 1
competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: SS; player_position_match_minutes_p90: 407.19; possession_pct: 0.4511833333333333; team_events: 2511; opp_team_events: 3133; passes: 45; passes_accurate: 35; pass_accuracy_pct: 0.7778; passes_open_play: 45; passes_accurate_open_play: 35; progressive_passes: 2; passes_into_final_third: 2; through_passes: 0; through_passes_accurate: 0; smart_passes: 0; smart_passes_accurate: 0; crosses: 2; crosses_accurate: 1; key_passes: 0; assists: 0; shot_assists: 0; second_assists: 0; creative_passes: 0; linkups: 0; playmaking_passes: 4; deep_completions: 0; passes_xt: 0.306; passes_into_third_xt: 0.0278; passes_third_xt: 0.1679; crosses_xt: 0.0466; xa: 0.0; receptions: 79; low_receptions: 12; penalty_area_receptions: 7; long_ball_receptions: 6; long_ball_receptions_xt: 0.0784; deep_runs_xt: 0.0; shots: 4; np_shots: 4; shots_on_target: 2; shot_on_target_pct: 0.5; goals: 1; np_goals: 1; own_goals: 0; shot_conversion_pct: 0.25; xg: 0.3177; xg_on_target: 0.3245; goals_minus_xg: 0.6823; xg_per_shot: 0.0794; carries: 7; carries_successful: 7; accelerations: 0; carries_xt: 0.1035; ball_runs_xt: 0.0694; dribbles_xt: 0.0219; ball_progression_xt: 0.1352; box_entries: 1; touches: 53; touches_in_box: 3; goals_per_box_touch: 0.3333; xg_per_box_touch: 0.1059; xg_plus_xa_per_100_touches: 0.5994; dribbles: 2; dribbles_successful: 1; dribbles_success_pct: 0.5; interceptions: 13; ball_recoveries: 1; high_recoveries: 1; possessions_won: 2; possessions_won_per_opponent_possession: 0.0044; num_opponent_possessions: 454; num_team_possessions: 445; possession_count: 899; clearances: 0; defensive_duels: 27; defensive_duels_won: 5; defensive_duels_won_pct: 0.1852; true_tackles: 18; true_tackles_won: 5; tackle_success_pct: 0.2778; defensive_intensity: 18; defensive_actions: 8; defensive_line_height_m: 59.85; aerials: 22; aerials_won: 6; aerials_won_pct: 0.2727; attacking_aerials: 15; attacking_aerials_won: 3; attacking_aerials_won_pct: 0.2; defensive_aerials: 11; defensive_aerials_won: 4; defensive_aerials_won_pct: 0.3636; headed_plays: 1; losses: 15; high_turnovers: 3; num_low_turnovers: 3; high_turnovers_per_low_reception: 0.25; num_low_turnovers_per_low_reception: 0.25; carries_xt_per_100_receptions: 0.131; passes_xt_per_100_receptions: 0.3873; corners: 0; free_kicks: 0; goal_kicks: 0; penalties_taken: 0; penalties_scored: 0; fouls_committed: 8; fouls_suffered: 9; yellow_cards: 0; red_cards: 0; defending_1v1: 2; successful_1v1: 0; defending_1v1_pct: 0.0; under_pressure_actions: 23; under_pressure_retention: 16; pressure_resistance_pct: 0.6957; counterpressing: 8; num_counterpresses: 8; num_counterpresses_leading_to_recovery: 2; xg_created: 0.0013; xg_dribble: 0.0; xg_buildup: 0.0957; xg_chain: 0.4134; xg_chain_per_possession: 0.0042; num_possessions_involved: 99

From Twelve's data (get_player_match_metrics_defence):
(no rows)

From Twelve's data (get_player_match_metrics_by_zone):
zone: ATT_HALF_LEFT_HALF_SPACE; competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: CF; team_events: 6; receptions: 20; losses: 3; passes_xt: 0.0482; passes: 7; playmaking_passes: 1; carries_xt: 0.0; carries: 0; dribbles_xt: 0.0; dribbles: 0; xg: 0.0; xg_on_target: 0.0; np_shots: 0; shots_np: 0; goals_np: 0; defensive_actions: 0; defensive_duels: 3; defensive_duels_won: 1; defensive_duels_won_pct: 0.3333; defensive_intensity: 2; defensive_aerials: 5; defensive_aerials_won: 2; defensive_aerials_won_pct: 0.4; attacking_aerials: 12; attacking_aerials_won: 3; attacking_aerials_won_pct: 0.25; aerials: 12; ball_recoveries: 0; under_pressure_retention: 0; under_pressure_actions: 0; xg_buildup: 0.0; xg_chain: 0.0; xg_chain_per_possession: 0.0; xg_created: 0.0; xg_dribble: 0.0
zone: ATT_HALF_LEFT_HALF_SPACE; competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: LW; team_events: 1; receptions: 2; losses: 0; passes_xt: 0.0; passes: 0; playmaking_passes: 0; carries_xt: 0.0; carries: 0; dribbles_xt: 0.0; dribbles: 0; xg: 0.0684; xg_on_target: 0.0; np_shots: 1; shots_np: 1; goals_np: 0; shot_conversion_pct: 0.0; xg_per_shot: 0.0684; defensive_actions: 0; defensive_duels: 1; defensive_duels_won: 0; defensive_duels_won_pct: 0.0; defensive_intensity: 1; defensive_aerials: 0; defensive_aerials_won: 0; attacking_aerials: 0; attacking_aerials_won: 0; aerials: 0; ball_recoveries: 0; under_pressure_retention: 0; under_pressure_actions: 0; xg_buildup: 0.0; xg_chain: 0.0684; xg_chain_per_possession: 0.0684; xg_created: 0.0; xg_dribble: 0.0
zone: ATT_HALF_LEFT_HALF_SPACE; competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: RW; team_events: 0; receptions: 1; losses: 0; passes_xt: 0.0; passes: 0; playmaking_passes: 0; carries_xt: 0.0; carries: 0; dribbles_xt: 0.0; dribbles: 0; xg: 0.0; xg_on_target: 0.0; np_shots: 0; shots_np: 0; goals_np: 0; defensive_actions: 0; defensive_duels: 0; defensive_duels_won: 0; defensive_intensity: 0; defensive_aerials: 0; defensive_aerials_won: 0; attacking_aerials: 0; attacking_aerials_won: 0; aerials: 0; ball_recoveries: 0; under_pressure_retention: 0; under_pressure_actions: 0; xg_buildup: 0.0; xg_chain: 0.0; xg_created: 0.0; xg_dribble: 0.0
zone: ATT_HALF_LEFT_HALF_SPACE; competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: SS; team_events: 10; receptions: 5; losses: 1; passes_xt: 0.0543; passes: 6; playmaking_passes: 1; carries_xt: 0.0145; carries: 3; dribbles_xt: 0.0; dribbles: 0; xg: 0.0095; xg_on_target: 0.0; np_shots: 1; shots_np: 1; goals_np: 0; shot_conversion_pct: 0.0; xg_per_shot: 0.0095; defensive_actions: 1; defensive_duels: 2; defensive_duels_won: 0; defensive_duels_won_pct: 0.0; defensive_intensity: 2; defensive_aerials: 1; defensive_aerials_won: 0; defensive_aerials_won_pct: 0.0; attacking_aerials: 3; attacking_aerials_won: 0; attacking_aerials_won_pct: 0.0; aerials: 3; ball_recoveries: 0; under_pressure_retention: 3; under_pressure_actions: 3; pressure_resistance_pct: 1.0; xg_buildup: 0.0019; xg_chain: 0.0114; xg_chain_per_possession: 0.0008; xg_created: 0.0013; xg_dribble: 0.0
zone: ATT_HALF_LEFT_WING; competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: CF; team_events: 3; receptions: 5; losses: 3; passes_xt: 0.0144; passes: 4; playmaking_passes: 0; carries_xt: 0.0033; carries: 1; dribbles_xt: 0.0; dribbles: 0; xg: 0.0; xg_on_target: 0.0; np_shots: 0; shots_np: 0; goals_np: 0; defensive_actions: 2; defensive_duels: 3; defensive_duels_won: 2; defensive_duels_won_pct: 0.6667; defensive_intensity: 2; defensive_aerials: 0; defensive_aerials_won: 0; attacking_aerials: 1; attacking_aerials_won: 1; attacking_aerials_won_pct: 1.0; aerials: 1; ball_recoveries: 0; under_pressure_retention: 1; under_pressure_actions: 5; pressure_resistance_pct: 0.2; xg_buildup: 0.0; xg_chain: 0.0; xg_chain_per_possession: 0.0; xg_created: 0.0; xg_dribble: 0.0
zone: ATT_HALF_LEFT_WING; competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: LW; team_events: 0; receptions: 1; losses: 0; passes_xt: 0.0; passes: 0; playmaking_passes: 0; carries_xt: 0.0; carries: 0; dribbles_xt: 0.0; dribbles: 0; xg: 0.0; xg_on_target: 0.0; np_shots: 0; shots_np: 0; goals_np: 0; defensive_actions: 1; defensive_duels: 1; defensive_duels_won: 1; defensive_duels_won_pct: 1.0; defensive_intensity: 1; defensive_aerials: 0; defensive_aerials_won: 0; attacking_aerials: 0; attacking_aerials_won: 0; aerials: 0; ball_recoveries: 0; under_pressure_retention: 0; under_pressure_actions: 0; xg_buildup: 0.0; xg_chain: 0.0; xg_chain_per_possession: 0.0; xg_created: 0.0; xg_dribble: 0.0
zone: ATT_HALF_LEFT_WING; competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: SS; team_events: 7; receptions: 7; losses: 1; passes_xt: 0.0359; passes: 6; playmaking_passes: 0; carries_xt: 0.0043; carries: 1; dribbles_xt: 0.0219; dribbles: 1; xg: 0.0; xg_on_target: 0.0; np_shots: 0; shots_np: 0; goals_np: 0; defensive_actions: 3; defensive_duels: 3; defensive_duels_won: 1; defensive_duels_won_pct: 0.3333; defensive_intensity: 3; defensive_aerials: 1; defensive_aerials_won: 1; defensive_aerials_won_pct: 1.0; attacking_aerials: 1; attacking_aerials_won: 1; attacking_aerials_won_pct: 1.0; aerials: 1; ball_recoveries: 1; under_pressure_retention: 1; under_pressure_actions: 2; pressure_resistance_pct: 0.5; xg_buildup: 0.0178; xg_chain: 0.0178; xg_chain_per_possession: 0.0022; xg_created: 0.0; xg_dribble: 0.0
zone: ATT_HALF_RIGHT_HALF_SPACE; competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: CF; team_events: 17; receptions: 14; losses: 10; passes_xt: 0.0633; passes: 14; playmaking_passes: 1; carries_xt: 0.0063; carries: 1; dribbles_xt: 0.0157; dribbles: 1; xg: 0.0925; xg_on_target: 0.4744; np_shots: 2; shots_np: 2; goals_np: 1; shot_conversion_pct: 0.5; xg_per_shot: 0.0463; defensive_actions: 0; defensive_duels: 4; defensive_duels_won: 0; defensive_duels_won_pct: 0.0; defensive_intensity: 1; defensive_aerials: 0; defensive_aerials_won: 0; attacking_aerials: 2; attacking_aerials_won: 1; attacking_aerials_won_pct: 0.5; aerials: 2; ball_recoveries: 0; under_pressure_retention: 3; under_pressure_actions: 6; pressure_resistance_pct: 0.5; xg_buildup: 0.0257; xg_chain: 0.1183; xg_chain_per_possession: 0.0045; xg_created: 0.0039; xg_dribble: 0.0
zone: ATT_HALF_RIGHT_HALF_SPACE; competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: RW; team_events: 0; receptions: 1; losses: 0; passes_xt: 0.0; passes: 0; playmaking_passes: 0; carries_xt: 0.0; carries: 0; dribbles_xt: 0.0; dribbles: 0; xg: 0.0; xg_on_target: 0.0; np_shots: 0; shots_np: 0; goals_np: 0; defensive_actions: 0; defensive_duels: 0; defensive_duels_won: 0; defensive_intensity: 0; defensive_aerials: 0; defensive_aerials_won: 0; attacking_aerials: 0; attacking_aerials_won: 0; aerials: 0; ball_recoveries: 0; under_pressure_retention: 0; under_pressure_actions: 0; xg_buildup: 0.0; xg_chain: 0.0; xg_created: 0.0; xg_dribble: 0.0
zone: ATT_HALF_RIGHT_HALF_SPACE; competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player_position: SS; team_events: 0; receptions: 3; losses: 2; passes_xt: 0.0; passes: 0; playmaking_passes: 0; carries_xt: 0.0; carries: 0; dribbles_xt: 0.0; dribbles: 0; xg: 0.0; xg_on_target: 0.0; np_shots: 0; shots_np: 0; goals_np: 0; defensive_actions: 0; defensive_duels: 0; defensive_duels_won: 0; defensive_intensity: 0; defensive_aerials: 0; defensive_aerials_won: 0; attacking_aerials: 1; attacking_aerials_won: 0; attacking_aerials_won_pct: 0.0; aerials: 1; ball_recoveries: 0; under_pressure_retention: 0; under_pressure_actions: 0; xg_buildup: 0.0; xg_chain: 0.0; xg_chain_per_possession: 0.0; xg_created: 0.0; xg_dribble: 0.0
zone: ATT_HALF_RIGHT_WING; competition_id: 1468; season: 2026; team_id: 35074; player_id: 688425; player
(cut)

## Question 1: Give me a summary of Dani Ortolan's season.

### What the data means
Q: What can we infer from a striker that is good in both making runs and dribbling?
A: Players who are strong in both making runs and dribbling are likely to be more faster and agile, along with having the technical ability to carry the ball long distances and retain it.

Q: What qualities do we use to evaluate a striker?
A: We evaluate strikers by their involvement, their hold-up play, their ability to provide for teammates, their aerial threat, their poaching, their finishing, their run quality and their pressing.

Q: How would we define a modern striker?
A: A modern striker is someone who excels in traditional areas that we look for in strikers such as goalscoring, but is also at least average in pressing, making runs and creating for others.

Q: What are the important metrics for a striker who is good at finishing?
A: The primary quality of a good finisher is that they score goals at high rate per ninety. But it is also important to look at how often they convert the chances they get and if they have high quality chances on target.

Q: What are the most important metrics/data-points for a striker?
A: How often they score (non-penalty goals per ninety) and how accurate their shooting is (non-penlashot conversion %) are two of the most important metrics for evaluating strikers.

Q: What are some attributes of a striker with a good run quality?
A: The key to a striker's run quality is making threatening runs with and without the ball and carrying the ball forward. Strikers who are good at runs take the ball into the box themselves and have a high number of penalty area receptions.

Q: What does it mean for a striker to be an aerial threat?
A: A striker who isan aerial threat is getting into a lot of aerial duels and winning a lot of them in the final third. They are important to attacks as they are able to compete with centre backs for balls in the air on set pieces and also help retain the ball after a clearances or goal kicks. Typically, these players are taller than average, although there are many examples of shorter strikers who are strong in heading.

Q: What makes a striker a strong finisher?
A: Strikers with excellent finishing skills tend to exhibit a notably high shot conversion percentage. Furthermore, another sign of their prowess in finishing is when they surpass their expected goals by scoring more frequently or consistently placing their shots in optimal positions, indicating a superior ability to convert opportunities compared to their expected goal values.

Q: How do we measure if a striker is an aerial threat?
A: A striker who has a good success rate in aerials, wins many aerial dules and frequently makes headed plays, especially in the attacking half, is considered to be an aerial threat.

Q: Explain why involvement can be important for a striker?
A: We often want strikers who help the team build up attacks. Involvement is high when a player drops in to midfield and passes to winger or attacking midfielders by laying the ball off to them. Once they have started the attack, a good striker will run towards the goal, in order to recieve a pass.

Q: What does it mean for a striker to be good in pressing?
A: Strikers who rank highly in defensive intensity are good in pressing. This means they are attempting a lot of defensive actions and winning the ball back.

Q: What are the important attributes of a striker who has good involvement?
A: A striker is considered to have good involvement if they are active defensively, have lots of touches on the ball and are involved in play leading up to a shot.

Q: What does it mean for a striker to be clinical?
A: When describing a striker, clinical means they are very good finishers. This means they have a high np shot conversion % and generally also score more than expected given their chances, that is, they outperform their expected goals.

Q: Why is it important to have a striker who is good technically?
A: A striker who is good technically as can contribute to attacks with more than just their goalscoring. For modern strikers, it is expected that they can both contribute to the buildup and create threat themselves. Having a striker who is good in goalscoring, creating and running makes them a triple-threat who are hard to defend against.

Q: What makes a striker a good dribbler of the ball?
A: A good dribbler makes a high number of progressive runs and carries the ball into dangerous areas (high expected threat). They take the ball in to the box, have dribbles which lead to chances and can retain the ball under pressure. Dribbling is not always a quality we look for in a striker, but run quality includes some of these aspects.

Q: How do we measure if a striker is good at holding up the ball?
A: Players who are good at holding up the ball can receive long balls played up to them and retain the ball under pressure. They win ariels with a high percent and don't lose the ball.

Q: Why is it important to have a striker with high pressing?
A: Strikers with high pressing are typically harder-working and are able to help the team's defence by spearheading their pressing attempts. They are very important to modern attacks which rely on pressing and counterpressing to win the ball back.

Q: How do we measure if a striker provides for their teammates?
A: A striker who provides for their teammates ﻿makes a lot of key passes, assists and second assists. They will rank highly in expected goals created and expected assists. Deep completions are also important.

Q: What makes a striker strong technically?
A: A striker who is good in creating for others can be defined as strong technically. A player who is bad in creating and dribbling would be defined as poor technically.

Q: How would you describe a striker who is not above average in any metrics?
A: A striker who is not above average in any metrics could be described as not being a standout in any area.

Q: What metrics tell us that a striker is good at pressing?
A: A striker who presses well has lots high recoveries and makes interceptions. They have a high defence intensity and engage in counterpressing.

Q: What metrics does a striker rank well in if they are good at poaching?
A: A good poaching striker has a high number expected goals per shot (which means they come in to good shooting positions), as well as a high expected goals per touch.

Q: What is a striker?
A: A striker is the football player whose primary role is to score goals or to assist other players in scoring goals. They often find themselves receiving the ball in the box or making runs to receive the ball high up the pitch.

Q: What are the most important attributes for a striker?
A: The most important attribute for a striker is undeniably goalscoring, as their main job is to put the ball in the back of the net. Some good strikers are good at only goalscoring, but in the modern game, it is almost necessary for a striker to be good in other aspects in order to succeed. Some teams rely on strikers to contribute to the build-up with passing and dribbling ability, while others desire someone who makes a lot of runs in behind. It is largely dependent on what the team and coaches want from their striker.

Q: What makes a striker a good targetman?
A: A striker who is strong in primarily heading, but also a player who scores lots of goals and receives the ball in the box could be called a targetman.

Q: What does it mean for a striker to be good in poaching?
A: A striker who is good in poaching is making the most of their touches in the box. They shoot from very high-probability locations. Typically, these are players who are getting on the end of crosses and shooting mainly from first-time shots close to goal, rather than someone trying to create chances for themselves.

Q: If a striker is strong in attack, but has low pressing, how do we characterise them?
A: A striker who is strong in attack but not in pressing can be described as very attacking, but not defensively minded.

Q: What can we infer from a striker that is good in terms of run quality?
A: Players who rank highly in making runs tend to be faster, as they use their pace to make threatening runs and receive the ball behind the defensive line.

Q: What measurements would convince us that a striker has a high aeriel threat?
A: A striker who wins aeriel duels, who ranks highly in attacking aeriels in particular is considered to have ariel threat.

Q: What do we mean by holding up the ball?
A: A striker who can hold up the ball is able to receive the ball when a team is counterattcking, often via a long ball from deep in the team's own half. They can then keep control of the ball and find another player to lay it off to. This can be essential in the build up to attacks.

### Rule-based description of this player's data for this question
Dani Ortolan is a unknown footed 28-year-old striker playing for América Mineiro in the Brasileiro Women. She is average at poaching compared to other strikers. She performs well in np goals per box touch. She is good at finishing compared to other strikers. She performs well in np shot conversion %. She is poor at providing teammates compared to other strikers. In providing teammates, she is weakest in xgcreated. She is below average at run quality compared to other strikers. She performs poorly in carries (xt). She is poor at hold up play compared to other strikers. In hold up play, she is weakest in pressure resistance %. She is average at aerial threat compared to other strikers. She is average in every metric in aerial threat. She is poor at pressing compared to other strikers. In pressing, she is weakest in high recoveries. She is poor at involvement compared to other strikers. In involvement, she is weakest in touches.

## Question 2: What are Dani Ortolan's strengths and weaknesses?

### What the data means
(none)

### Rule-based description of this player's data for this question
Dani Ortolan is a unknown footed 28-year-old striker playing for América Mineiro in the Brasileiro Women. Let's take a look at the strengths of Daniela Maria Lopes Ortolan. 

The best skill of Daniela Maria Lopes Ortolan  is finishing. She is good at finishing compared to other strikers. She performs well in np Shot conversion %. Here is some useful information about what it means for a player to be strong in finishing:What does it mean for a player to be good in finishing?
Players who are good in finishing make the most out of their goal-scoring opportunities. This means that they have a high shot conversion % and generally also score more than expected given their chances, that is, they outperform their expected goals.

What makes a striker a strong finisher?
Strikers with excellent finishing skills tend to exhibit a notably high shot conversion percentage. Furthermore, another sign of their prowess in finishing is when they surpass their expected goals by scoring more frequently or consistently placing their shots in optimal positions, indicating a superior ability to convert opportunities compared to their expected goal values.

What does it mean for a player to be bad in finishing?
Players who are bad in finishing struggle to score goals from their chances. This means that they have a low shot conversion % and generally also score less than expected given their chances, that is, they underperform their expected goals.

What are the important metrics for a striker who is good at finishing?
The primary quality of a good finisher is that they score goals at high rate per ninety. But it is also important to look at how often they convert the chances they get and if they have high quality chances on target.

The second best skill of Daniela Maria Lopes Ortolan  is defensive heading. She is good at defensive heading compared to other strikers. She performs well in Defensive aerials won. Here is some useful information about what it means for a player to be strong in defensive heading:How would we describe a player with strong defensive heading ability?
A player excels in defensive heading by consistently winning aerial challenges, particularly in key defensive areas, and effectively using their aerial ability to clear threats, maintain defensive structure, and provide security in the air.

How would we describe a player with strong defensive heading ability?
A player excels in defensive heading by consistently winning aerial challenges, particularly in key defensive areas, and effectively using their aerial ability to clear threats, maintain defensive structure, and provide security in the air.

What does it mean for a player to be good in defensive heading? 
Players with high defensive heading rankings win a substantial number of aerial duels and maintain a high success rate, particularly in the defensive 60% of the field.

What does it mean for a player to be bad in defensive heading?
Players with low defensive heading rankings win few aerial duels and have a low success rate, particularly in the defensive 60% of the field.

The third best skill of Daniela Maria Lopes Ortolan  is poaching. She is average at poaching compared to other strikers. She performs well in np Goals per box touch. Here is some useful information about what it means for a player to be strong in poaching:What does it mean for a player to be good in poaching?
Players who are good in poaching make the most of their touches in the box and mainly shoot from very dangerous chances. Typically, these are players who get on the end of crosses and shoot mainly from first-time shots close to goal, rather than creating chances for themselves.

What does it mean for a player to be bad in poaching?
Players who are bad in poaching typically take shots from more difficult chances and are more involved in the build-up to shots.

What does it mean for a striker to be good in poaching?
A striker who is good in poaching is making the most of their touches in the box. They shoot from very high-probability locations. Typically, these are players who are getting on the end of crosses and shooting mainly from first-time shots close to goal, rather than someone trying to create chances for themselves.

How does a player's poaching ability contribute to their box threat?
Players who are good at poaching enhance their box threat by being in the right place at the right time to score goals. Their instinct for finding scoring opportunities makes them a constant danger in the penalty area.

Let's take a look at the weaknesses of Daniela Maria Lopes Ortolan. 

Daniela Maria Lopes Ortolan weakest quality lies in involvement. Indeed, she is poor at involvement compared to other strikers. In involvement, she is weakest in Touches. Here is some useful information about what it means for a player to be weak in involvement:What does it mean for a player to have a low involvement?
Players with a low involvement are not actively engaged in various aspects of the game. Players with low involvement may have limited influence on the match and contribute less to their team's performance. 

How would we describe a player who is less involved in the game?
A player with a low involvement is less engaged in key aspects of the game, possibly contributing less to the team's overall performance and having limited influence on the tempo and structure of the match. 

Are players with low involvement less important to their team?
Players with low involvement are not necessarily less important, but their contributions may be more specific to their roles within the team. For example, strikers who have low involvement but score a lot of goals are often crucial to their teams.

What does it mean for a player to have a high involvement?
Players with high involvement actively and frequently participate in various aspects of the game. High involvement suggests that the players have significant contributions to their team's performance.

Daniela Maria Lopes Ortolan second weakest quality lies in effectiveness. Indeed, she is poor at effectiveness compared to other strikers. In effectiveness, she is weakest in Passes (xT) per 100 receptions. Here is some useful information about what it means for a player to be weak in effectiveness:What does it mean for a player to be bad in effectiveness?
Players who struggle in effectiveness tend to play more simple, choosing safer options rather than taking the initiative in attack. These players might be vulnerable when receiving the ball in dangerous situations and they seldomly win back the ball. The least effective players falter in both defensive and offensive effectiveness.

What does it mean for a player to be good in effectiveness?
Players who are good in effectiveness are conistantly looking forward in attack, making the most of their touches. Furthermore, they rarely lose the ball in dangerous situations and often break down the oppositions attacks. The best players in effectiveness might excell in either the defensive or offensive parts of the game or be very good in both.

If a player's effectiveness rating is low, which metrics should the scout prioritize assessing?
If a player's effectiveness rating is low, the scout should prioritize assessing passes (xT) per reception and possessions won per opponent possession to pinpoint specific areas where the player might be underperforming.

What does a high effectiveness score indicate about a player's overall contributions?
A high effectiveness score indicates that the player excels in multiple aspects of play, including passing, carrying, creating scoring opportunities, and defensive actions, making significant contributions to both offensive and defensive phases of the game.

Daniela Maria Lopes Ortolan third weakest quality lies in progression. Indeed, she is poor at progression compared to other strikers. She is poor in every metric in progression, with Playmaking passes as his worst. Here is some useful information about what it means for a player to be weak in progression:What does it mean for a player to be bad in progression?
Players who rank low in progression might struggle to effectively advance the ball up the field and contribute to their team's attacking play. They may have difficulties executing difficult passes, but it can also be caused by the players being located higher up on the pitch and therefore receiving progressive actions instead of performing them.  

What does it mean for a player to be good in progression?
Players with strong progression skills play a crucial role in building attacks for their team. They can advance the ball into more advanced areas of the pitch through precise passes and ball-carrying, thereby increasing the likelihood of generating goal-scoring opportunities.

What does a high progression score indicate about a player's overall contributions?
A high progression score indicates that the player excels in advancing the ball and creating opportunities, demonstrating strong vision, passing accuracy, and the ability to consistently contribute to the team's offensive dynamics.

What should a scout analyze if a player has a low number of ball progressions?
If a player has a low number of ball progressions, the scout should analyze the player's reluctance or inability to advance the ball, potentially indicating a need for improved vision, passing accuracy, or confidence in carrying the ball forward.

Use this information to answer the user about the football player. Remember the user wants to know: What are Dani Ortolan's strengths and weaknesses?. Answer this query in 2 sentences using the information above. Explain in detail what these strengths and weaknesses mean about what we can expect from the player in terms of style of play and contributions to the team. If the user asks about weaknesses of the player focus only on that, do not write about strengths unless asked. Likewise, if they are interested in strengths focus only on that and not weaknesses. If they do ask specifically about both your answer can be 3 sentences, but otherwise it should be 2 sentences. Make sure to explain what the player's strengths mean in terms of how the player contributes to the team and what weaknesses show about what we should be concerned about in footballing terms. 

## Question 3: How good is Dani Ortolan at passing?

### What the data means
Q: What metrics tell us that a striker is good at pressing?
A: A striker who presses well has lots high recoveries and makes interceptions. They have a high defence intensity and engage in counterpressing.

Q: What can we infer from a striker that is good in both making runs and dribbling?
A: Players who are strong in both making runs and dribbling are likely to be more faster and agile, along with having the technical ability to carry the ball long distances and retain it.

Q: What are the important metrics for a striker who is good at finishing?
A: The primary quality of a good finisher is that they score goals at high rate per ninety. But it is also important to look at how often they convert the chances they get and if they have high quality chances on target.

Q: What does it mean for a player to have a high passes (xT)?
A: A player with a high passes (xT) is able to create a lot of expected threat from passes, and is adept at progressing the ball into more dangerous positions.

Q: How would you describe a striker who is not above average in any metrics?
A: A striker who is not above average in any metrics could be described as not being a standout in any area.

Q: What is passing quality?
A: Passing quality refers to a player's ability to deliver a variety of passes that pose a significant threat to the opposition's defense, leading to goal-scoring opportunities or advantageous positions for the receiving player. It is evaluated by how threatening the passes are, rather than the quantity.

Q: What are the most important metrics/data-points for a striker?
A: How often they score (non-penalty goals per ninety) and how accurate their shooting is (non-penlashot conversion %) are two of the most important metrics for evaluating strikers.

Q: What does it mean for a striker to be good in poaching?
A: A striker who is good in poaching is making the most of their touches in the box. They shoot from very high-probability locations. Typically, these are players who are getting on the end of crosses and shooting mainly from first-time shots close to goal, rather than someone trying to create chances for themselves.

Q: What can we infer from a striker that is good in terms of run quality?
A: Players who rank highly in making runs tend to be faster, as they use their pace to make threatening runs and receive the ball behind the defensive line.

Q: What makes a striker strong technically?
A: A striker who is good in creating for others can be defined as strong technically. A player who is bad in creating and dribbling would be defined as poor technically.

Q: How do we measure if a striker is an aerial threat?
A: A striker who has a good success rate in aerials, wins many aerial dules and frequently makes headed plays, especially in the attacking half, is considered to be an aerial threat.

Q: What is a striker?
A: A striker is the football player whose primary role is to score goals or to assist other players in scoring goals. They often find themselves receiving the ball in the box or making runs to receive the ball high up the pitch.

Q: What does it mean for a striker to be an aerial threat?
A: A striker who isan aerial threat is getting into a lot of aerial duels and winning a lot of them in the final third. They are important to attacks as they are able to compete with centre backs for balls in the air on set pieces and also help retain the ball after a clearances or goal kicks. Typically, these players are taller than average, although there are many examples of shorter strikers who are strong in heading.

Q: Why is it important to have a striker who is good technically?
A: A striker who is good technically as can contribute to attacks with more than just their goalscoring. For modern strikers, it is expected that they can both contribute to the buildup and create threat themselves. Having a striker who is good in goalscoring, creating and running makes them a triple-threat who are hard to defend against.

Q: What qualities do we use to evaluate a striker?
A: We evaluate strikers by their involvement, their hold-up play, their ability to provide for teammates, their aerial threat, their poaching, their finishing, their run quality and their pressing.

Q: How is passing quality measured?
A: Passing quality is a weighted sum of a players performance compared to other players in the same position in passes (xT) (30%), crosses (xT) (20%),  passes into the final third (20 %), passes in the final third (20%) and chance passes (10%).

Q: How do we measure if a striker is good at holding up the ball?
A: Players who are good at holding up the ball can receive long balls played up to them and retain the ball under pressure. They win ariels with a high percent and don't lose the ball.

Q: Explain why involvement can be important for a striker?
A: We often want strikers who help the team build up attacks. Involvement is high when a player drops in to midfield and passes to winger or attacking midfielders by laying the ball off to them. Once they have started the attack, a good striker will run towards the goal, in order to recieve a pass.

Q: What makes a striker a good dribbler of the ball?
A: A good dribbler makes a high number of progressive runs and carries the ball into dangerous areas (high expected threat). They take the ball in to the box, have dribbles which lead to chances and can retain the ball under pressure. Dribbling is not always a quality we look for in a striker, but run quality includes some of these aspects.

Q: What does it mean for a striker to be good in pressing?
A: Strikers who rank highly in defensive intensity are good in pressing. This means they are attempting a lot of defensive actions and winning the ball back.

Q: How is passing quality calculated?
A: Passing quality is calculated as the weighted sum of the z-scores of players in passes (xT) (30%), crosses (xT) (20%),  passes into the final third (20 %), passes in the final third (20%) and chance creating passes (10%), among other players who play the same position.

Q: What does it mean for a striker to be clinical?
A: When describing a striker, clinical means they are very good finishers. This means they have a high np shot conversion % and generally also score more than expected given their chances, that is, they outperform their expected goals.

Q: What are the most important attributes for a striker?
A: The most important attribute for a striker is undeniably goalscoring, as their main job is to put the ball in the back of the net. Some good strikers are good at only goalscoring, but in the modern game, it is almost necessary for a striker to be good in other aspects in order to succeed. Some teams rely on strikers to contribute to the build-up with passing and dribbling ability, while others desire someone who makes a lot of runs in behind. It is largely dependent on what the team and coaches want from their striker.

Q: Would you expect a player with a high amount of chance creating passes to also have a high amount of passes (xT)?
A: You would expect a player with a high amount of chance creating passes to also have a high amount of passes (xT), as chance creating passes often find teammates in good positions, which inherently generate expected threat. If a player ranks highly in chance creating passes but not in passes (xT), then they are likely getting themselves into difficult positions often, and rely on their passing vision to find any teammate, even if the receiver is not in a more threatening position.

Q: What does it mean for a player to have good passing quality?
A: Players with good passing quality have the ability to consistently deliver different types of passes that pose a significant threat to the opposition's defense. Their passes often lead to goal-scoring opportunities or advantageous positions for their teammates.

Q: What are some attributes of a striker with a good run quality?
A: The key to a striker's run quality is making threatening runs with and without the ball and carrying the ball forward. Strikers who are good at runs take the ball into the box themselves and have a high number of penalty area receptions.

Q: What are the important attributes of a striker who has good involvement?
A: A striker is considered to have good involvement if they are active defensively, have lots of touches on the ball and are involved in play leading up to a shot.

Q: What do we mean by holding up the ball?
A: A striker who can hold up the ball is able to receive the ball when a team is counterattcking, often via a long ball from deep in the team's own half. They can then keep control of the ball and find another player to lay it off to. This can be essential in the build up to attacks.

Q: What does it mean for a player to have bad passing quality?
A: Players with bad passing quality often choose safer passing options and struggle to deliver threatening passes.

Q: Why is it important to have a striker with high pressing?
A: Strikers with high pressing are typically harder-working and are able to help the team's defence by spearheading their pressing attempts. They are very important to modern attacks which rely on pressing and counterpressing to win the ball back.

Q: If a striker is strong in attack, but has low pressing, how do we characterise them?
A: A striker who is strong in attack but not in pressing can be described as very attacking, but not defensively minded.

Q: What makes a striker a strong finisher?
A: Strikers with excellent finishing skills tend to exhibit a notably high shot conversion percentage. Furthermore, another sign of their prowess in finishing is when they surpass their expected goals by scoring more frequently or consistently placing their shots in optimal positions, indicating a superior ability to convert opportunities compared to their expected goal values.

Q: How would we define a modern striker?
A: A modern striker is someone who excels in traditional areas that we look for in strikers such as goalscoring, but is also at least average in pressing, making runs and creating for others.

Q: What makes a striker a good targetman?
A: A striker who is strong in primarily heading, but also a player who scores lots of goals and receives the ball in the box could be called a targetman.

Q: What does it indicate about a player's passing quality when they have high passes into the final third (xT) but low passes in the final third (xT)?
A: When a player has high passes into the final third (xT) but a low passes in the final third (xT), it may suggest that they excel in progressing the ball into dangerous areas but may not frequently participate in the final stages of the attacking build-up or goal-scoring opportunities. Their strength lies in initiating attacking moves, often creating opportunities for their teammates to take advantage of the advanced positions they help establish.

Q: What does it mean for a player to have a low crosses (xT)?
A: A player who has a low crosses (xT) is not creating much threat from their crosses. However, they can still be dangerous passers if they rank highly in other passing xT metrics. For instance, there are many excellent chance creators who rarely cross the ball, but rather create threat from central positions.

Q: How do we measure if a striker provides for their teammates?
A: A striker who provides for their teammates ﻿makes a lot of key passes, assists and second assists. They will rank highly in expected goals created and expected assists. Deep completions are also important.

Q: What measurements would convince us that a striker has a high aeriel threat?
A: A striker who wins aeriel duels, who ranks highly in attacking aeriels in particular is considered to have ariel threat.

Q: What metrics does a striker rank well in if they are good at poaching?
A: A good poaching striker has a high number expected goals per shot (which means they come in to good shooting positions), as well as a high expected goals per touch.

Q: What does it indicate about a player's passing quality when they have high passes in the final third (xT) but low passes into the final third (xT)?
A: When a player has high passes in the final third (xT) but a low passes into the final third (xT), it suggests that they are proficient in operating within the attacking third of the field, particularly in the build-up to goal-scoring opportunities. However, their involvement in progressing the ball into those advanced areas might be limited.

Q: How do you describe a player when they have average Passes (xT) adj in the defensive right wing?
A: If a player has average Passes (xT) adj in the defensive right wing, they are solid from the full-back zone without being a threat to the opposition. They can play the dangerous pass here and there, but just as often choose safer options.

Q: What does it say about a player when they have excellent Passes (xT) adj in the defensive right half-space?
A: When a player has excellent Passes (xT) adj in the defensive right half-space, they are great in the narrow right zone while moving the game forward. They often allow their team to increase the tempo by playing vertical passes that move the ball into more dangerous areas.

Q: What does below average Passes (xT) adj in the defensive left wing show about a player?
A: Below average Passes (xT) adj on the defensive left wing shows that a player is not good with finding diagonal or vertical passes from that zone. They are probably not comfortable when moved to the left back position and often find themselves struggling to find options for circulating possession.

Q: When a player has good Passes (xT) adj in the attacking right half-space, what does it mean?
A: if a player has good Passes (xT) in the attacking right half-space, it tells us that they are solid from the right channels. They are a good outlet for their team to craft chances or second-assists by finding the runs of more attacking players.

Q: What does excellent Passes (xT) adj in the opposition penalty area show about a player?
A: Excellent Passes (xT) adj in the opposition penalty area tells us that a player is able to find deft passes even in the tightest of spaces and under most amount of attention. It points to a great vision and close control, not only keeping the ball but creating chances in a zone where the opposition is already crowding.

Q: What do you say about a player when they have below average Passes (xT) adj in the attacking left wing?
A: When a player has below average Passes (xT) adj in the attacking left wing, they are unable to create too many good passes from wide left. They either choose to run with the ball or find safer, more lateral, options to lay the ball off to.

Q: What does poor Passes (xT) adj in the attacking central midfield tell us about a player?
A: Poor passes (xT) adj in the attacking central midfield shows that a player is not a good attacking midfielder from the central spaces. They are not able to play enough line-breaking passes or progress the game even from an advanced area of the pitch, and thus slow their team's tempo down by playing it safe.

Q: What do you say about a player when they have average Passes (xT) adj in the attacking right wing?
A: When a player has average Passes (xT) adj in the attacking right wing, they are just about alright from the right wing but not a creative force. They can sometimes find threatening passes into more dangerous areas, but have the tendency to fall into safety too.

Q: What does outstanding Passes (xT) adj in the attacking left half-space tell us about a player?
A: Outstanding Passes (xT) adj in the attacking left half-space tells us that a player is amongst the best in their league at creating chances from the left channel. They take up those dangerous zones in the pockets and often find wingers or fullbacks overlapping, or find a way to send passes to the centre-forward.

Q: What does it show when a player has poor Passes (xT) adj in the defensive central midfield?
A: If a player has poor Passes (xT) adj in the defensive central midfield, they are less than ideal while playing as a deep-lying playmaker. They have a tendency to play lateral or reverse passes, and are not very good with breaking opposition lines, either diagonally or vertically, from that space.

Q: If a player has good Passes (xT) adj in the defensive left half-space, what does it mean?
A: When a player has a good Passes (xT) adj in the defensive left half-space, it means that they able to progress the ball from the narrow left zones of their half. They are probably a defensive player with good build-up attributes and help their team move the game forward from deeper areas.

### Rule-based description of this player's data for this question
Dani Ortolan is poor at passing quality compared to other strikers. She is below average at crosses (xt) compared to other strikers. She is poor at expected threat from passes into the final third, chance creating passes, expected threat from passes inside of the final third and expected threat from passes compared to other strikers.

Daniela Maria Lopes Ortolan's passes_xt was average in the defensive central midfield and defensive left half-space compared to other strikers. Daniela Maria Lopes Ortolan performed below average in the defensive right half-space, attacking central midfield, own penalty area, attacking right wing and defensive right wing. Daniela Maria Lopes Ortolan performed poor in the attacking left wing, defensive left wing, attacking left half-space, opposition penalty area and attacking right half-space.

## Question 4: How good is Dani Ortolan at dribbling?

### What the data means
Q: What makes a striker a good targetman?
A: A striker who is strong in primarily heading, but also a player who scores lots of goals and receives the ball in the box could be called a targetman.

Q: What is a striker?
A: A striker is the football player whose primary role is to score goals or to assist other players in scoring goals. They often find themselves receiving the ball in the box or making runs to receive the ball high up the pitch.

Q: What can we infer from a striker that is good in terms of run quality?
A: Players who rank highly in making runs tend to be faster, as they use their pace to make threatening runs and receive the ball behind the defensive line.

Q: If a striker is strong in attack, but has low pressing, how do we characterise them?
A: A striker who is strong in attack but not in pressing can be described as very attacking, but not defensively minded.

Q: What makes a striker a strong finisher?
A: Strikers with excellent finishing skills tend to exhibit a notably high shot conversion percentage. Furthermore, another sign of their prowess in finishing is when they surpass their expected goals by scoring more frequently or consistently placing their shots in optimal positions, indicating a superior ability to convert opportunities compared to their expected goal values.

Q: What does it mean for a striker to be good in poaching?
A: A striker who is good in poaching is making the most of their touches in the box. They shoot from very high-probability locations. Typically, these are players who are getting on the end of crosses and shooting mainly from first-time shots close to goal, rather than someone trying to create chances for themselves.

Q: How do we measure if a striker is an aerial threat?
A: A striker who has a good success rate in aerials, wins many aerial dules and frequently makes headed plays, especially in the attacking half, is considered to be an aerial threat.

Q: What can we infer from a striker that is good in both making runs and dribbling?
A: Players who are strong in both making runs and dribbling are likely to be more faster and agile, along with having the technical ability to carry the ball long distances and retain it.

Q: How would we define a modern striker?
A: A modern striker is someone who excels in traditional areas that we look for in strikers such as goalscoring, but is also at least average in pressing, making runs and creating for others.

Q: Explain why involvement can be important for a striker?
A: We often want strikers who help the team build up attacks. Involvement is high when a player drops in to midfield and passes to winger or attacking midfielders by laying the ball off to them. Once they have started the attack, a good striker will run towards the goal, in order to recieve a pass.

Q: What does it mean for a striker to be good in pressing?
A: Strikers who rank highly in defensive intensity are good in pressing. This means they are attempting a lot of defensive actions and winning the ball back.

Q: What does it mean for a player to be good in dribbling?
A: Players who are good in dribbling consistently and successfully generate threat by beating their markers in one-on-one situations. These players are typically very skillful and able to retain possession under pressure.

Q: What metrics does a striker rank well in if they are good at poaching?
A: A good poaching striker has a high number expected goals per shot (which means they come in to good shooting positions), as well as a high expected goals per touch.

Q: What are the important attributes of a striker who has good involvement?
A: A striker is considered to have good involvement if they are active defensively, have lots of touches on the ball and are involved in play leading up to a shot.

Q: Why is it important to have a striker who is good technically?
A: A striker who is good technically as can contribute to attacks with more than just their goalscoring. For modern strikers, it is expected that they can both contribute to the buildup and create threat themselves. Having a striker who is good in goalscoring, creating and running makes them a triple-threat who are hard to defend against.

Q: What are the most important metrics/data-points for a striker?
A: How often they score (non-penalty goals per ninety) and how accurate their shooting is (non-penlashot conversion %) are two of the most important metrics for evaluating strikers.

Q: What are the most important attributes for a striker?
A: The most important attribute for a striker is undeniably goalscoring, as their main job is to put the ball in the back of the net. Some good strikers are good at only goalscoring, but in the modern game, it is almost necessary for a striker to be good in other aspects in order to succeed. Some teams rely on strikers to contribute to the build-up with passing and dribbling ability, while others desire someone who makes a lot of runs in behind. It is largely dependent on what the team and coaches want from their striker.

Q: How do we measure if a striker provides for their teammates?
A: A striker who provides for their teammates ﻿makes a lot of key passes, assists and second assists. They will rank highly in expected goals created and expected assists. Deep completions are also important.

Q: How would you describe a striker who is not above average in any metrics?
A: A striker who is not above average in any metrics could be described as not being a standout in any area.

Q: What makes a striker strong technically?
A: A striker who is good in creating for others can be defined as strong technically. A player who is bad in creating and dribbling would be defined as poor technically.

Q: What measurements would convince us that a striker has a high aeriel threat?
A: A striker who wins aeriel duels, who ranks highly in attacking aeriels in particular is considered to have ariel threat.

Q: How do we measure if a striker is good at holding up the ball?
A: Players who are good at holding up the ball can receive long balls played up to them and retain the ball under pressure. They win ariels with a high percent and don't lose the ball.

Q: Why is dribbling not a part of run quality?
A: Run quality assesses the ability of players to make threatening runs without taking on players. Dribbling past players is a separate quality which is not necessarily correlated with run quality. However, the best players can do both and therefore pose a greater threat.

Q: What qualities do we use to evaluate a striker?
A: We evaluate strikers by their involvement, their hold-up play, their ability to provide for teammates, their aerial threat, their poaching, their finishing, their run quality and their pressing.

Q: What does it mean for a player to be bad in dribbling?
A: Players who are bad in dribbling either struggle to dribble past defenders or do not attempt to do so.

Q: What metrics tell us that a striker is good at pressing?
A: A striker who presses well has lots high recoveries and makes interceptions. They have a high defence intensity and engage in counterpressing.

Q: What are some attributes of a striker with a good run quality?
A: The key to a striker's run quality is making threatening runs with and without the ball and carrying the ball forward. Strikers who are good at runs take the ball into the box themselves and have a high number of penalty area receptions.

Q: What do we mean by holding up the ball?
A: A striker who can hold up the ball is able to receive the ball when a team is counterattcking, often via a long ball from deep in the team's own half. They can then keep control of the ball and find another player to lay it off to. This can be essential in the build up to attacks.

Q: How is dribbling measured?
A: Dribbling is a weighted sum of a players performance compared to other players in the same position in dribbles success % (20%), dribbles (xT) (40%), expected goals created with dribbles (25%) and pressure resistance % (15%).

Q: What does it mean for a striker to be clinical?
A: When describing a striker, clinical means they are very good finishers. This means they have a high np shot conversion % and generally also score more than expected given their chances, that is, they outperform their expected goals.

Q: What does it mean for a striker to be an aerial threat?
A: A striker who isan aerial threat is getting into a lot of aerial duels and winning a lot of them in the final third. They are important to attacks as they are able to compete with centre backs for balls in the air on set pieces and also help retain the ball after a clearances or goal kicks. Typically, these players are taller than average, although there are many examples of shorter strikers who are strong in heading.

Q: What makes a good dribler?
A: Good dribblers consistently and successfully generate threat by beating their markers in one-on-one situations. These players are typically very skillful and able to retain possession under pressure.

Q: Why is it important to have a striker with high pressing?
A: Strikers with high pressing are typically harder-working and are able to help the team's defence by spearheading their pressing attempts. They are very important to modern attacks which rely on pressing and counterpressing to win the ball back.

Q: What is dribbling?
A: Dribbling involves the skill of taking on opposing players one-on-one. It's the ability of maneuvering the ball past defenders while maintaining control, often through quick changes in direction, feints, and close ball control.

Q: How is dribbling calculated?
A: Dribbling is calculated as the weighted sum of the z-scores of players in dribbles success % (20%), dribbles (xT) (40%), expected goals created with dribbles (25%) and pressure resistance % (15%), among other players who play the same position.

Q: What are the important metrics for a striker who is good at finishing?
A: The primary quality of a good finisher is that they score goals at high rate per ninety. But it is also important to look at how often they convert the chances they get and if they have high quality chances on target.

Q: What makes a striker a good dribbler of the ball?
A: A good dribbler makes a high number of progressive runs and carries the ball into dangerous areas (high expected threat). They take the ball in to the box, have dribbles which lead to chances and can retain the ball under pressure. Dribbling is not always a quality we look for in a striker, but run quality includes some of these aspects.

Q: How would we describe a player who has a high number dribbles (xT) on the right attacking wing?
A: A player who has a high number dribbles (xT) on the right attacking wing is able to create a lot of threat from carrying the ball to wide areas and drawing in the opposition. They should be able to beat players wide then cut the ball in to underlapping midfielders or forwards. Having high dribbles (xT) on one of the wings usually means they can take one or more opposition defenders along with them which opens up space for their team to craft a dangerous chance.

Q: How would we describe a player who has good dribbles (xT)  in the penalty box?
A: A player who has a high number idribbles (xT) in the penalty box is exceptional at carving out opportunities in the box. These players are able to dribble expertly in tight spaces and often can find a final pass that can generate a shot.

Q: How would we describe a player who has low dribbles (xT) in the central attacking area in front of goal?
A: A player who has who has low dribbles (xT) in the central attacking area in front of goal is ineffective as an attacking option centrally. They are not proficient at running at the opposition defence.

Q: How would we describe a player who has mostly average numbers in different areas on the pitch for dribbles (xT)?
A: A player who has mostly average numbers in different areas on the pitch for dribbles (xT) doesn't show much creativity in dribbling past the opposition. They would rather look for passing options or lay the ball off to others who have the skills to attack the opposition.

Q: How would we describe a player who has good dribbles (xT)  in the central area in front of goal?
A: A player who has good dribbles (xT)  in the central area in front of goal is a serious threat in the final third. They have the ability to cut through the opposition and open up passing options for the left and right half-spaces.

Q: How would we describe a player who has a good dribbles (xT) in the left half space?
A: A player who has good dribbles (xT) in the left half space can get inside and threaten the box.

Q: How would we describe a player who has poor dribbles (xT)  on the attacking left wing?
A: A player who has poor poor dribbles (xT)  the attacking left wing is not able to get past players in the wide areas. The player is not particularly a threat on the wing.

### Rule-based description of this player's data for this question
Dani Ortolan is poor at dribbling compared to other strikers. She is average at dribble success % compared to other strikers. She is below average at expected goals created with dribbles compared to other strikers. She is poor at expected threat from dribbles and pressure resistance % compared to other strikers.

Daniela Maria Lopes Ortolan's dribbles_xt was good in the attacking central midfield compared to other strikers. Daniela Maria Lopes Ortolan performed average in the own penalty area, defensive right wing and defensive left half-space. Daniela Maria Lopes Ortolan performed below average in the attacking right half-space, defensive right half-space, defensive central midfield, defensive left wing, attacking left wing and attacking right wing. Daniela Maria Lopes Ortolan performed poor in the opposition penalty area and attacking left half-space.

## Question 5: Is Dani Ortolan a threat in the box?

### What the data means
Q: What does it mean for a striker to be good in pressing?
A: Strikers who rank highly in defensive intensity are good in pressing. This means they are attempting a lot of defensive actions and winning the ball back.

Q: How is box threat measured?
A: Box threat is a weighted sum of a players performance compared to other players in the same position in touches in box (20%), box entries from carries (10%), goals (25%), expected goals (25%) and penalty area receptions (20%).

Q: Why are expected assists not a part of box threat?
A: Box threat focuses on the goal-scoring threat and involvement of players inside of the penalty are, rather than their creation. Metrics such as assists, expected assists and key passes are represented in the quality providing teammates.

Q: What can we infer from a striker that is good in both making runs and dribbling?
A: Players who are strong in both making runs and dribbling are likely to be more faster and agile, along with having the technical ability to carry the ball long distances and retain it.

Q: How do we measure if a striker provides for their teammates?
A: A striker who provides for their teammates ﻿makes a lot of key passes, assists and second assists. They will rank highly in expected goals created and expected assists. Deep completions are also important.

Q: What qualities do we use to evaluate a striker?
A: We evaluate strikers by their involvement, their hold-up play, their ability to provide for teammates, their aerial threat, their poaching, their finishing, their run quality and their pressing.

Q: What makes a striker a good dribbler of the ball?
A: A good dribbler makes a high number of progressive runs and carries the ball into dangerous areas (high expected threat). They take the ball in to the box, have dribbles which lead to chances and can retain the ball under pressure. Dribbling is not always a quality we look for in a striker, but run quality includes some of these aspects.

Q: What are some attributes of a striker with a good run quality?
A: The key to a striker's run quality is making threatening runs with and without the ball and carrying the ball forward. Strikers who are good at runs take the ball into the box themselves and have a high number of penalty area receptions.

Q: What are the most important metrics/data-points for a striker?
A: How often they score (non-penalty goals per ninety) and how accurate their shooting is (non-penlashot conversion %) are two of the most important metrics for evaluating strikers.

Q: What does it mean for a player to have a high box threat?
A: Players with a high box threat are often considered goal-scoring threats and highly involved in the final actions of attacks.

Q: What do we mean by holding up the ball?
A: A striker who can hold up the ball is able to receive the ball when a team is counterattcking, often via a long ball from deep in the team's own half. They can then keep control of the ball and find another player to lay it off to. This can be essential in the build up to attacks.

Q: What do you say about a player with high box entries from carries per 90?
A: A player with high box entries from carries per 90 constantly finds themselves in the penalty box by carrying the ball or It makes them a danger for the opposition because they are in a position to create threatening chances from close to the goal.

Q: How do you describe a player with high np xG per 90?
A: A player with high np xG per 90 creates a lot of high-quality chances for themselves in the penalty box. This makes them a goal-scoring threat and a constant worry for the opponent defenders.

Q: How would you describe a striker who is not above average in any metrics?
A: A striker who is not above average in any metrics could be described as not being a standout in any area.

Q: How do we measure if a striker is an aerial threat?
A: A striker who has a good success rate in aerials, wins many aerial dules and frequently makes headed plays, especially in the attacking half, is considered to be an aerial threat.

Q: How do you describe a player with high np xG per 90 but low goals per 90?
A: A player with high np xG per 90 and low goals per 90 creates and gets a lot of chances for themselves but is not clinical with converting them into goals.

Q: What metrics does a striker rank well in if they are good at poaching?
A: A good poaching striker has a high number expected goals per shot (which means they come in to good shooting positions), as well as a high expected goals per touch.

Q: What can we infer from a striker that is good in terms of run quality?
A: Players who rank highly in making runs tend to be faster, as they use their pace to make threatening runs and receive the ball behind the defensive line.

Q: Explain why involvement can be important for a striker?
A: We often want strikers who help the team build up attacks. Involvement is high when a player drops in to midfield and passes to winger or attacking midfielders by laying the ball off to them. Once they have started the attack, a good striker will run towards the goal, in order to recieve a pass.

Q: What is a striker?
A: A striker is the football player whose primary role is to score goals or to assist other players in scoring goals. They often find themselves receiving the ball in the box or making runs to receive the ball high up the pitch.

Q: What does it mean for a striker to be an aerial threat?
A: A striker who isan aerial threat is getting into a lot of aerial duels and winning a lot of them in the final third. They are important to attacks as they are able to compete with centre backs for balls in the air on set pieces and also help retain the ball after a clearances or goal kicks. Typically, these players are taller than average, although there are many examples of shorter strikers who are strong in heading.

Q: Why is it important to have a striker with high pressing?
A: Strikers with high pressing are typically harder-working and are able to help the team's defence by spearheading their pressing attempts. They are very important to modern attacks which rely on pressing and counterpressing to win the ball back.

Q: What makes a striker a good targetman?
A: A striker who is strong in primarily heading, but also a player who scores lots of goals and receives the ball in the box could be called a targetman.

Q: Why are assists not a part of box threat?
A: Box threat focuses on the goal-scoring threat and involvement of players inside of the penalty are, rather than their creation. Metrics such as assists, expected assists and key passes are represented in the quality providing teammates.

Q: How is box threat calculated?
A: Box threat is calculated as the weighted sum of the z-scores of players in touches in box (20%), box entries from carries (10%), non-penalty goals (25%), non-penalty expected goals (25%) and box receptions (20%), among other players who play the same position.

Q: How would we define a modern striker?
A: A modern striker is someone who excels in traditional areas that we look for in strikers such as goalscoring, but is also at least average in pressing, making runs and creating for others.

Q: If a striker is strong in attack, but has low pressing, how do we characterise them?
A: A striker who is strong in attack but not in pressing can be described as very attacking, but not defensively minded.

Q: How do we measure if a striker is good at holding up the ball?
A: Players who are good at holding up the ball can receive long balls played up to them and retain the ball under pressure. They win ariels with a high percent and don't lose the ball.

Q: What is box threat?
A: Box threat assesses a player's ability to make an impact in and around the opposition's penalty area. It considers both the goal-scoring threat and the involvement of players inside of the penalty area.  This quality is particularly relevant for players in attacking roles.

Q: What are the important metrics for a striker who is good at finishing?
A: The primary quality of a good finisher is that they score goals at high rate per ninety. But it is also important to look at how often they convert the chances they get and if they have high quality chances on target.

Q: What makes a striker strong technically?
A: A striker who is good in creating for others can be defined as strong technically. A player who is bad in creating and dribbling would be defined as poor technically.

Q: How do you describe a player with low np goals per 90?
A: A player with low np goals per 90 does not score too many goals.

Q: What are the important attributes of a striker who has good involvement?
A: A striker is considered to have good involvement if they are active defensively, have lots of touches on the ball and are involved in play leading up to a shot.

Q: Why is it important to have a striker who is good technically?
A: A striker who is good technically as can contribute to attacks with more than just their goalscoring. For modern strikers, it is expected that they can both contribute to the buildup and create threat themselves. Having a striker who is good in goalscoring, creating and running makes them a triple-threat who are hard to defend against.

Q: What makes a striker a strong finisher?
A: Strikers with excellent finishing skills tend to exhibit a notably high shot conversion percentage. Furthermore, another sign of their prowess in finishing is when they surpass their expected goals by scoring more frequently or consistently placing their shots in optimal positions, indicating a superior ability to convert opportunities compared to their expected goal values.

Q: What does it mean for a striker to be clinical?
A: When describing a striker, clinical means they are very good finishers. This means they have a high np shot conversion % and generally also score more than expected given their chances, that is, they outperform their expected goals.

Q: What does it mean for a player to have a low box threat?
A: Players with a low box threat do not pose a significant goal-scoring threat and have limited involvement inside of the opposition's penalty area. Players that have a more defensive roles can be expected to have lower box threat.

Q: What do you say about a player with average box touches per 90?
A: A player with average touches in box per 90 takes a typical amount of touches in the opposition penalty box. They aren't a marauding attacking midfielder who constantly bombs the box, but they get into the box whenever necessary.

Q: What does it mean for a player to have low box receptions per 90?
A: A player with low box receptions per 90 is not a constant presence in the opposition penalty box. They are more comfortable playing deeper, possibly as a pivot or playmaker instead of a creative edge high in the midfield.

Q: What measurements would convince us that a striker has a high aeriel threat?
A: A striker who wins aeriel duels, who ranks highly in attacking aeriels in particular is considered to have ariel threat.

Q: What are the most important attributes for a striker?
A: The most important attribute for a striker is undeniably goalscoring, as their main job is to put the ball in the back of the net. Some good strikers are good at only goalscoring, but in the modern game, it is almost necessary for a striker to be good in other aspects in order to succeed. Some teams rely on strikers to contribute to the build-up with passing and dribbling ability, while others desire someone who makes a lot of runs in behind. It is largely dependent on what the team and coaches want from their striker.

Q: What does it mean for a striker to be good in poaching?
A: A striker who is good in poaching is making the most of their touches in the box. They shoot from very high-probability locations. Typically, these are players who are getting on the end of crosses and shooting mainly from first-time shots close to goal, rather than someone trying to create chances for themselves.

Q: What metrics tell us that a striker is good at pressing?
A: A striker who presses well has lots high recoveries and makes interceptions. They have a high defence intensity and engage in counterpressing.

Q: How do you describe a player with good xG adj from outside of the box?
A: A player with good xG adj from outside the box is very good at taking long shots. They fancy themselves to beat the opposition goalkeeper from distance and are a serious threat when left with space to shoot.

Q: How do you describe a player who has poor xG adj from the left side of the box?
A: A player who has poor xG adj from the left side of the box is not very adept at opening up high quality chances from the left channel. They are probably unable to receive the ball in those zones while carrying a leap on the opposition defenders.

Q: How do you describe a player who has outstanding xG adj from the golden zone and six yard box?
A: A player who has outstanding xG adj from the golden zone is a high-quality poacher who gets into great positions to receive chances centrally within the penalty box.

Q: How do you describe a player with below average xG adj from outside of the box?
A: A player who has below average xG adj from outside of the box does find themselves with too many clear shots from distance. They probably get tightly marked, and when they do get the ball, prefer either passing it to an open attacker over shooting from afar.

Q: How do you describe a player who has poor xG adj in the golden zone?
A: A player who has poor xG adj in the golden zone is not very good at finding clear chances in the penalty box. Over a long term, this points at a problem with their off-the-ball movement and stealing a step on the opposition defenders.

Q: How do you describe a player who has Outstanding xG adj in the right side of the box?
A: A player who has outstanding xG adj in the right side of the box is an exceptional attacking threat in the right channels. They like receiving the ball past the opposition defense line and taking shots. It points at great movement and high speed.

Q: How do you describe a player who has average xG adj from the left side of the box?
A: A player who has average xG adj from the left side of the box is a solid shot-taker from the left channel. They are able to move into decent angles to take their shots, either by running into that zone from deeper areas or moving diagonally from within the box.

### Rule-based description of this player's data for this question
Dani Ortolan is below average at box threat compared to other strikers. She is average at np goals and penalty area receptions compared to other strikers. She is below average at np expected goals and box entries from carries compared to other strikers. She is poor at touches in the box compared to other strikers.

Daniela Maria Lopes Ortolan's xg was average in the six yard box compared to other strikers. Daniela Maria Lopes Ortolan performed below average in the outside of the box and golden zone.

## Question 6: Where on the pitch does Dani Ortolan win the ball back?

### What the data means
Q: How do you describe a player who has outstanding defensive actions won in the opposition penalty area?
A: A player who has outstanding defensive actions in the opposition penalty area is an aggressive pressing forward. They take on the opposition defenders during the build-up play and force them into playing harried passes.

Q: How do you describe a player who has poor defensive actions won in their defensive left wing?
A: A player who has poor defensive actions in their defensive left wing is not suited to a left full back role. They are probably more effective defensively in central zones and have a tendency to not make too many defensive duels in the left wide area.

Q: How do you describe a player who has a high defensive actions won in attacking right half-space?
A: A player who has a high defensive actions in the attacking right half-space is a fiesty attacking player when out of possession. They tend to chase down opposition defenders and defensive midfielders during build-up and engage in a lot of tackles and pressures.

Q: How do you describe a player who has below average defensive actions won in the attacking left wing?
A: A player who has below average defensive actions in the attacking left wing is a wide player who doesn't quite contest opposition full backs out of possession. They have a tendency to be slightly lazy without the ball and don't close down or tackle opposition players enough in those areas.

Q: How do you describe a player who has excellent defensive actions in the Defensive central midfield?
A: A player who has a excellent defensive actions in the defensive central midfield breaks the opposition play before they reach the more dangerous areas. They probably operate as defensive midfielders who are asked to shield the defence during an opposition attacking move.

Q: How do you describe a player who has excellent defensive actions in the attacking central midfield?
A: A player who has a excellent defensive actions in the attacking central midfield is an aggressive central midfielder who fights hard for the ball in the middle of the park. They are usually an asset to their team in breaking up opposition build-up.

Q: How do you describe a player who has below average defensive actions won in the Defensive right half-space?
A: A player who has below average defensive actions in the defensive right half space is not a good defender in the right-sided channels. They may be more efficient centrally or out wide but let opposition attackers past them in the channels.

Q: How do you describe a player who has poor defensive actions won in the attacking left half-space?
A: A player who has poor defensive actions in the attacking left half-space does not engage in too many defensive duels in the left channel. They are probably a forward or a left-sided wide player who don't actively hunt down opposition defensive players during build up.

Q: How do you describe a player who has excellent defensive actions won in their Own penalty area?
A: A player who has excellent defensive actions in their own penalty area engages in a lot of defensive duels inside their box. They are a defensive player (a central defender or a defensive midfielder) and are adept at engaging with opposition attackers when they penetrate into the box.

Q: How do you describe a player who has excellent defensive actions won in the attacking right wing?
A: A player who has a excellent defensive actions in the attacking right wing is a winger with an exceptional defensive work rate. They tackle opposition full backs, winning the ball often, and don't let them just circulate the ball easily.

Q: How do you describe a player who has average defensive actions won in the Defensive left half-space?
A: A player who has average defensive actions in the defensive left half space is a sturdy defender in the channels. They are probably not stationed there at all points, but engage in defensive duels when necessary.

Q: How do you describe a player who has excellent defensive actions on the defensive right wing?
A: A player who has excellent defensive actions won in the defensive right wing is a combative full back. They engage heavily with opposition wingers and like their 1v1 duels.

### Rule-based description of this player's data for this question
Daniela Maria Lopes Ortolan's defensive_actions was good in the own penalty area compared to other strikers. Daniela Maria Lopes Ortolan performed average in the attacking left wing, defensive right half-space and defensive left wing. Daniela Maria Lopes Ortolan performed below average in the attacking central midfield, defensive central midfield, defensive left half-space, attacking left half-space and defensive right wing. Daniela Maria Lopes Ortolan performed poor in the opposition penalty area, attacking right wing and attacking right half-space.

## Question 7: Could Dani Ortolan play in a different position?

### What the data means
Q: What is a striker?
A: A striker is the football player whose primary role is to score goals or to assist other players in scoring goals. They often find themselves receiving the ball in the box or making runs to receive the ball high up the pitch.

Q: How do we measure if a striker is good at holding up the ball?
A: Players who are good at holding up the ball can receive long balls played up to them and retain the ball under pressure. They win ariels with a high percent and don't lose the ball.

Q: What are the important attributes of a striker who has good involvement?
A: A striker is considered to have good involvement if they are active defensively, have lots of touches on the ball and are involved in play leading up to a shot.

Q: What makes a striker a strong finisher?
A: Strikers with excellent finishing skills tend to exhibit a notably high shot conversion percentage. Furthermore, another sign of their prowess in finishing is when they surpass their expected goals by scoring more frequently or consistently placing their shots in optimal positions, indicating a superior ability to convert opportunities compared to their expected goal values.

Q: What makes a striker a good dribbler of the ball?
A: A good dribbler makes a high number of progressive runs and carries the ball into dangerous areas (high expected threat). They take the ball in to the box, have dribbles which lead to chances and can retain the ball under pressure. Dribbling is not always a quality we look for in a striker, but run quality includes some of these aspects.

Q: What does it mean for a striker to be good in pressing?
A: Strikers who rank highly in defensive intensity are good in pressing. This means they are attempting a lot of defensive actions and winning the ball back.

Q: If a striker is strong in attack, but has low pressing, how do we characterise them?
A: A striker who is strong in attack but not in pressing can be described as very attacking, but not defensively minded.

Q: How do we measure if a striker is an aerial threat?
A: A striker who has a good success rate in aerials, wins many aerial dules and frequently makes headed plays, especially in the attacking half, is considered to be an aerial threat.

Q: What makes a striker strong technically?
A: A striker who is good in creating for others can be defined as strong technically. A player who is bad in creating and dribbling would be defined as poor technically.

Q: What are the most important metrics/data-points for a striker?
A: How often they score (non-penalty goals per ninety) and how accurate their shooting is (non-penlashot conversion %) are two of the most important metrics for evaluating strikers.

Q: What are the most important attributes for a striker?
A: The most important attribute for a striker is undeniably goalscoring, as their main job is to put the ball in the back of the net. Some good strikers are good at only goalscoring, but in the modern game, it is almost necessary for a striker to be good in other aspects in order to succeed. Some teams rely on strikers to contribute to the build-up with passing and dribbling ability, while others desire someone who makes a lot of runs in behind. It is largely dependent on what the team and coaches want from their striker.

Q: What qualities do we use to evaluate a striker?
A: We evaluate strikers by their involvement, their hold-up play, their ability to provide for teammates, their aerial threat, their poaching, their finishing, their run quality and their pressing.

Q: What does it mean for a striker to be an aerial threat?
A: A striker who isan aerial threat is getting into a lot of aerial duels and winning a lot of them in the final third. They are important to attacks as they are able to compete with centre backs for balls in the air on set pieces and also help retain the ball after a clearances or goal kicks. Typically, these players are taller than average, although there are many examples of shorter strikers who are strong in heading.

Q: What metrics does a striker rank well in if they are good at poaching?
A: A good poaching striker has a high number expected goals per shot (which means they come in to good shooting positions), as well as a high expected goals per touch.

Q: What makes a striker a good targetman?
A: A striker who is strong in primarily heading, but also a player who scores lots of goals and receives the ball in the box could be called a targetman.

Q: What are the important metrics for a striker who is good at finishing?
A: The primary quality of a good finisher is that they score goals at high rate per ninety. But it is also important to look at how often they convert the chances they get and if they have high quality chances on target.

Q: Why is it important to have a striker who is good technically?
A: A striker who is good technically as can contribute to attacks with more than just their goalscoring. For modern strikers, it is expected that they can both contribute to the buildup and create threat themselves. Having a striker who is good in goalscoring, creating and running makes them a triple-threat who are hard to defend against.

Q: What metrics tell us that a striker is good at pressing?
A: A striker who presses well has lots high recoveries and makes interceptions. They have a high defence intensity and engage in counterpressing.

Q: What can we infer from a striker that is good in both making runs and dribbling?
A: Players who are strong in both making runs and dribbling are likely to be more faster and agile, along with having the technical ability to carry the ball long distances and retain it.

Q: What does it mean for a striker to be clinical?
A: When describing a striker, clinical means they are very good finishers. This means they have a high np shot conversion % and generally also score more than expected given their chances, that is, they outperform their expected goals.

Q: What can we infer from a striker that is good in terms of run quality?
A: Players who rank highly in making runs tend to be faster, as they use their pace to make threatening runs and receive the ball behind the defensive line.

Q: What measurements would convince us that a striker has a high aeriel threat?
A: A striker who wins aeriel duels, who ranks highly in attacking aeriels in particular is considered to have ariel threat.

Q: How would you describe a striker who is not above average in any metrics?
A: A striker who is not above average in any metrics could be described as not being a standout in any area.

Q: What do we mean by holding up the ball?
A: A striker who can hold up the ball is able to receive the ball when a team is counterattcking, often via a long ball from deep in the team's own half. They can then keep control of the ball and find another player to lay it off to. This can be essential in the build up to attacks.

Q: Why is it important to have a striker with high pressing?
A: Strikers with high pressing are typically harder-working and are able to help the team's defence by spearheading their pressing attempts. They are very important to modern attacks which rely on pressing and counterpressing to win the ball back.

Q: What does it mean for a striker to be good in poaching?
A: A striker who is good in poaching is making the most of their touches in the box. They shoot from very high-probability locations. Typically, these are players who are getting on the end of crosses and shooting mainly from first-time shots close to goal, rather than someone trying to create chances for themselves.

Q: Explain why involvement can be important for a striker?
A: We often want strikers who help the team build up attacks. Involvement is high when a player drops in to midfield and passes to winger or attacking midfielders by laying the ball off to them. Once they have started the attack, a good striker will run towards the goal, in order to recieve a pass.

Q: How do we measure if a striker provides for their teammates?
A: A striker who provides for their teammates ﻿makes a lot of key passes, assists and second assists. They will rank highly in expected goals created and expected assists. Deep completions are also important.

Q: What are some attributes of a striker with a good run quality?
A: The key to a striker's run quality is making threatening runs with and without the ball and carrying the ball forward. Strikers who are good at runs take the ball into the box themselves and have a high number of penalty area receptions.

Q: How would we define a modern striker?
A: A modern striker is someone who excels in traditional areas that we look for in strikers such as goalscoring, but is also at least average in pressing, making runs and creating for others.

### Rule-based description of this player's data for this question
Dani Ortolan is a unknown footed 28-year-old striker playing for América Mineiro in the Brasileiro Women. She is average at poaching compared to other strikers. She performs well in np goals per box touch. She is good at finishing compared to other strikers. She performs well in np shot conversion %. She is poor at providing teammates compared to other strikers. In providing teammates, she is weakest in xgcreated. She is below average at run quality compared to other strikers. She performs poorly in carries (xt). She is poor at hold up play compared to other strikers. In hold up play, she is weakest in pressure resistance %. She is average at aerial threat compared to other strikers. She is average in every metric in aerial threat. She is poor at pressing compared to other strikers. In pressing, she is weakest in high recoveries. She is poor at involvement compared to other strikers. In involvement, she is weakest in touches.

## Question 8: How good is Dani Ortolan at pressing?

### What the data means
Q: What can we infer from a striker that is good in both making runs and dribbling?
A: Players who are strong in both making runs and dribbling are likely to be more faster and agile, along with having the technical ability to carry the ball long distances and retain it.

Q: What is a striker?
A: A striker is the football player whose primary role is to score goals or to assist other players in scoring goals. They often find themselves receiving the ball in the box or making runs to receive the ball high up the pitch.

Q: What are the important metrics for a striker who is good at finishing?
A: The primary quality of a good finisher is that they score goals at high rate per ninety. But it is also important to look at how often they convert the chances they get and if they have high quality chances on target.

Q: What qualities do we use to evaluate a striker?
A: We evaluate strikers by their involvement, their hold-up play, their ability to provide for teammates, their aerial threat, their poaching, their finishing, their run quality and their pressing.

Q: How is pressing calculated?
A: Pressing is calculated as the weighted sum of the z-scores of players in defensive intensity (25%), high recoveries (35%), interceptions (10%) and counterpressing recoveries (30%), among other players who play the same position.

Q: What makes a striker a strong finisher?
A: Strikers with excellent finishing skills tend to exhibit a notably high shot conversion percentage. Furthermore, another sign of their prowess in finishing is when they surpass their expected goals by scoring more frequently or consistently placing their shots in optimal positions, indicating a superior ability to convert opportunities compared to their expected goal values.

Q: What do we mean by holding up the ball?
A: A striker who can hold up the ball is able to receive the ball when a team is counterattcking, often via a long ball from deep in the team's own half. They can then keep control of the ball and find another player to lay it off to. This can be essential in the build up to attacks.

Q: What measurements would convince us that a striker has a high aeriel threat?
A: A striker who wins aeriel duels, who ranks highly in attacking aeriels in particular is considered to have ariel threat.

Q: What does it mean for a player to rank highly in counterpressures and defensive intensity?
A: A player who ranks highly in counterpressures and defensive intensity has a high defensive engagement and agresssion, and has a good work rate to attempt win the ball back.

Q: How do we measure if a striker provides for their teammates?
A: A striker who provides for their teammates ﻿makes a lot of key passes, assists and second assists. They will rank highly in expected goals created and expected assists. Deep completions are also important.

Q: What makes a striker a good dribbler of the ball?
A: A good dribbler makes a high number of progressive runs and carries the ball into dangerous areas (high expected threat). They take the ball in to the box, have dribbles which lead to chances and can retain the ball under pressure. Dribbling is not always a quality we look for in a striker, but run quality includes some of these aspects.

Q: How would you describe a striker who is not above average in any metrics?
A: A striker who is not above average in any metrics could be described as not being a standout in any area.

Q: What is the relationship between high recoveries and counterpressures?
A: Counterpressures are often performed after the team loses possession high up the pitch, so a successfull counterpressure usually results in an interception from that player or a teammate.

Q: What is pressing?
A: Pressing assesses players' proactive defensive efforts to close down, pressure, or engage an opponent with the ball. It takes into account the number of defensive actions players perform, with an emphasis on counterpressing and high recoveries.

Q: What does it mean for a striker to be clinical?
A: When describing a striker, clinical means they are very good finishers. This means they have a high np shot conversion % and generally also score more than expected given their chances, that is, they outperform their expected goals.

Q: How do we measure if a striker is an aerial threat?
A: A striker who has a good success rate in aerials, wins many aerial dules and frequently makes headed plays, especially in the attacking half, is considered to be an aerial threat.

Q: What does it mean for a striker to be good in pressing?
A: Strikers who rank highly in defensive intensity are good in pressing. This means they are attempting a lot of defensive actions and winning the ball back.

Q: How would we define a modern striker?
A: A modern striker is someone who excels in traditional areas that we look for in strikers such as goalscoring, but is also at least average in pressing, making runs and creating for others.

Q: Why are high recoveries a part of pressing?
A: The primary reason teams adopt a pressing playing style is that winning the ball high up the pitch often generates threatening situations. Consequently, high recoveries are of great importance when measuring pressing. Equally important is contributing to the press without recovering the ball, but the current dataset lacks information about these efforts.

Q: What makes a striker a good targetman?
A: A striker who is strong in primarily heading, but also a player who scores lots of goals and receives the ball in the box could be called a targetman.

Q: What does it mean for a player to have a high amount of counterpressures but low defensive intensity?
A: A player with a high amount of counterpressures but low defensive intensity is likely making a lot of defensive efforts immediately after their team loses possession, but overall they do not make many on ball defensive actions.

Q: What metrics does a striker rank well in if they are good at poaching?
A: A good poaching striker has a high number expected goals per shot (which means they come in to good shooting positions), as well as a high expected goals per touch.

Q: How do we measure if a striker is good at holding up the ball?
A: Players who are good at holding up the ball can receive long balls played up to them and retain the ball under pressure. They win ariels with a high percent and don't lose the ball.

Q: What are some attributes of a striker with a good run quality?
A: The key to a striker's run quality is making threatening runs with and without the ball and carrying the ball forward. Strikers who are good at runs take the ball into the box themselves and have a high number of penalty area receptions.

Q: What are the most important attributes for a striker?
A: The most important attribute for a striker is undeniably goalscoring, as their main job is to put the ball in the back of the net. Some good strikers are good at only goalscoring, but in the modern game, it is almost necessary for a striker to be good in other aspects in order to succeed. Some teams rely on strikers to contribute to the build-up with passing and dribbling ability, while others desire someone who makes a lot of runs in behind. It is largely dependent on what the team and coaches want from their striker.

Q: What are the most important metrics/data-points for a striker?
A: How often they score (non-penalty goals per ninety) and how accurate their shooting is (non-penlashot conversion %) are two of the most important metrics for evaluating strikers.

Q: If a striker is strong in attack, but has low pressing, how do we characterise them?
A: A striker who is strong in attack but not in pressing can be described as very attacking, but not defensively minded.

Q: What about players that don't win the ball but participate in the press?
A: Pressing is a team effort and, therefore, it cannot be fully attributed to the individual. However, the current dataset does not include information about the players who contribute to the pressure but don't make a defensive action. As a result, their efforts cannot be measured.

Q: What metrics tell us that a striker is good at pressing?
A: A striker who presses well has lots high recoveries and makes interceptions. They have a high defence intensity and engage in counterpressing.

Q: What are the important attributes of a striker who has good involvement?
A: A striker is considered to have good involvement if they are active defensively, have lots of touches on the ball and are involved in play leading up to a shot.

Q: What does it mean for a striker to be good in poaching?
A: A striker who is good in poaching is making the most of their touches in the box. They shoot from very high-probability locations. Typically, these are players who are getting on the end of crosses and shooting mainly from first-time shots close to goal, rather than someone trying to create chances for themselves.

Q: Why is it important to have a striker who is good technically?
A: A striker who is good technically as can contribute to attacks with more than just their goalscoring. For modern strikers, it is expected that they can both contribute to the buildup and create threat themselves. Having a striker who is good in goalscoring, creating and running makes them a triple-threat who are hard to defend against.

Q: Explain why involvement can be important for a striker?
A: We often want strikers who help the team build up attacks. Involvement is high when a player drops in to midfield and passes to winger or attacking midfielders by laying the ball off to them. Once they have started the attack, a good striker will run towards the goal, in order to recieve a pass.

Q: How is pressing  measured?
A: Pressing  is a weighted sum of a players performance compared to other players in the same position in defensive intensity (25%), high recoveries (35%), interceptions (10%) and counterpressing recoveries (30%).

Q: What makes a striker strong technically?
A: A striker who is good in creating for others can be defined as strong technically. A player who is bad in creating and dribbling would be defined as poor technically.

Q: What does it mean for a player to be bad in pressing?
A: Players who struggle with pressing may contribute less defensively and find it challenging to disrupt the opponent's play, which isn't solely linked to their defensive work rate, as it can result from unsuccessful efforts.

Q: What can we infer from a striker that is good in terms of run quality?
A: Players who rank highly in making runs tend to be faster, as they use their pace to make threatening runs and receive the ball behind the defensive line.

Q: What does it mean for a player to be good in pressing?
A: Players who are good in pressing have a high defensive work rate and are skilled in winning possession high up on the pitch, which can generate dangerous offensive transitions.

Q: Why is it important to have a striker with high pressing?
A: Strikers with high pressing are typically harder-working and are able to help the team's defence by spearheading their pressing attempts. They are very important to modern attacks which rely on pressing and counterpressing to win the ball back.

Q: What does it mean for a striker to be an aerial threat?
A: A striker who isan aerial threat is getting into a lot of aerial duels and winning a lot of them in the final third. They are important to attacks as they are able to compete with centre backs for balls in the air on set pieces and also help retain the ball after a clearances or goal kicks. Typically, these players are taller than average, although there are many examples of shorter strikers who are strong in heading.

Q: How do you describe a player with below-average defensive intensity in the opposition penalty area?
A: A player with below-average defensive intensity in the opposition penalty area may not apply sufficient pressure on opposition defenders, potentially allowing them more space and time to make decisive passes, which could lead to build-up opportunities.

Q: How do you describe a player with outstanding defensive intensity in the defensive central midfield?
A: A player with outstanding defensive intensity in the defensive central midfield is the heart of the team's defensive efforts in the attacking third, showing exceptional work rate, fierce tackling, and determination to recover possession.

Q: How do you describe a player who shows poor defensive intensity in the attacking central midfield?
A: A player who shows poor defensive intensity in the attacking central midfield may struggle to effectively contribute to the team's defensive shape high in the central areas. They are often being bypassed or outmaneuvered by opponents, highlighting a critical area for improvement in their overall defensive game.

Q: How do you describe a player with excellent defensive intensity in the attacking left half-space?
A: A player with excellent defensive intensity in the attacking left half-space is good at defending vigorously in the left channel, using their energy and tactical intelligence to disrupt the opposition's right-sided defenders any rhythm and regain control of the ball.

Q: How do you describe a player who has excellent defensive intensity in the attacking left wing?
A: A player with excellent defensive intensity in the attacking left wing is a wide player with excellent work rate. They track opposition fullbacks and defenders with vigor and engage in duels whenever possible.

Q: What does excellent defensive intensity in the defensive left wing tell us about a player?
A: Excellent defensive intensity in the left wing tells us that a player engages in a lot of tackles and pressures from the left back area. They are a dominant defensive presence in the team and don't let opponents go past without a fight.

Q: What does poor defensive intensity in the defensive right wing tell us about a player?
A: When a player has poor defensive intensity in the defensive right wing, they are quite passive when opposition attacks from their left hand side. They are probably right-sided midfielders or wingers who are somewhat lazy at tracking opposition runners and retrieving the ball.

Q: How do you describe a player who has below average defensive intensity in the attacking left wing?
A: A player with below average defensive intensity in the attacking right wing is a right-sided wide player who barely engages with opposition full backs. They mostly let the play pass them by, only rarely getting into tackles and pressures on that side.

Q: When a player has average defensive intensity in the attacking right half space, what does it mean?
A: If a player has average defensive intensity in the attacking right half-space, it means that they are quick to press opposition players in the right channels without necessarily being relentless. They are not lazy, and indeed press, but once the ball is played past them, might cool off.

### Rule-based description of this player's data for this question
Dani Ortolan is poor at pressing compared to other strikers. She is average at counterpressing actions compared to other strikers. She is below average at interceptions compared to other strikers. She is poor at defensive intensity and high recoveries compared to other strikers.

Daniela Maria Lopes Ortolan's defensive_intensity was excellent in the own penalty area compared to other strikers. Daniela Maria Lopes Ortolan performed average in the attacking central midfield, defensive central midfield, attacking left half-space, opposition penalty area, defensive right half-space, attacking left wing and defensive left wing. Daniela Maria Lopes Ortolan performed below average in the defensive right wing, defensive left half-space and attacking right wing. Daniela Maria Lopes Ortolan performed poor in the attacking right half-space.

## Question 9: How good is Dani Ortolan in the air?

### What the data means
Q: What are the important metrics for a striker who is good at finishing?
A: The primary quality of a good finisher is that they score goals at high rate per ninety. But it is also important to look at how often they convert the chances they get and if they have high quality chances on target.

Q: How would we define a modern striker?
A: A modern striker is someone who excels in traditional areas that we look for in strikers such as goalscoring, but is also at least average in pressing, making runs and creating for others.

Q: Why is it important to have a striker who is good technically?
A: A striker who is good technically as can contribute to attacks with more than just their goalscoring. For modern strikers, it is expected that they can both contribute to the buildup and create threat themselves. Having a striker who is good in goalscoring, creating and running makes them a triple-threat who are hard to defend against.

Q: How would we describe a player who is average at aerial threat?
A: This player shows moderate ability in aerial challenges, occasionally winning headers but may lack consistency or physical dominance in these aerial duels.

Q: What does it mean for a striker to be clinical?
A: When describing a striker, clinical means they are very good finishers. This means they have a high np shot conversion % and generally also score more than expected given their chances, that is, they outperform their expected goals.

Q: What qualities do we use to evaluate a striker?
A: We evaluate strikers by their involvement, their hold-up play, their ability to provide for teammates, their aerial threat, their poaching, their finishing, their run quality and their pressing.

Q: What makes a striker a strong finisher?
A: Strikers with excellent finishing skills tend to exhibit a notably high shot conversion percentage. Furthermore, another sign of their prowess in finishing is when they surpass their expected goals by scoring more frequently or consistently placing their shots in optimal positions, indicating a superior ability to convert opportunities compared to their expected goal values.

Q: What can we infer from a striker that is good in both making runs and dribbling?
A: Players who are strong in both making runs and dribbling are likely to be more faster and agile, along with having the technical ability to carry the ball long distances and retain it.

Q: How would you describe a striker who is not above average in any metrics?
A: A striker who is not above average in any metrics could be described as not being a standout in any area.

Q: What does it mean for a striker to be an aerial threat?
A: A striker who isan aerial threat is getting into a lot of aerial duels and winning a lot of them in the final third. They are important to attacks as they are able to compete with centre backs for balls in the air on set pieces and also help retain the ball after a clearances or goal kicks. Typically, these players are taller than average, although there are many examples of shorter strikers who are strong in heading.

Q: How is aerial threat calculated?
A: Aerial threat is calculated as the weighted sum of the z-scores of players in aerials won (10%), aerials won % (15%), attacking aerials won (20%), attacking aerials won % (35%) and headed plays (20%), among other players who play the same position.

Q: What are the most important attributes for a striker?
A: The most important attribute for a striker is undeniably goalscoring, as their main job is to put the ball in the back of the net. Some good strikers are good at only goalscoring, but in the modern game, it is almost necessary for a striker to be good in other aspects in order to succeed. Some teams rely on strikers to contribute to the build-up with passing and dribbling ability, while others desire someone who makes a lot of runs in behind. It is largely dependent on what the team and coaches want from their striker.

Q: If a striker is strong in attack, but has low pressing, how do we characterise them?
A: A striker who is strong in attack but not in pressing can be described as very attacking, but not defensively minded.

Q: What makes a striker strong technically?
A: A striker who is good in creating for others can be defined as strong technically. A player who is bad in creating and dribbling would be defined as poor technically.

Q: How do 'attacking aerials won' and 'attacking aerials won %' together shape a player's aerial profile in front of the goal?
A: Together, these aspects shape a player's aerial profile in front of the goal by highlighting their effectiveness and efficiency in offensive aerial situations, crucial for scoring or creating chances in the air.

Q: How do we measure if a striker provides for their teammates?
A: A striker who provides for their teammates ﻿makes a lot of key passes, assists and second assists. They will rank highly in expected goals created and expected assists. Deep completions are also important.

Q: What is aerial threat?
A: Aerial threat refers to a player's ability to pose a danger and get into scoring opportunities in the air, often in set-pieces.

Q: What does it mean for a player to have a low aerial threat?
A: Players who rank badly in aerial threat rarely win offensive aerial duels and usually do not pose a goal-scoring danger in the air.

Q: What are the important attributes of a striker who has good involvement?
A: A striker is considered to have good involvement if they are active defensively, have lots of touches on the ball and are involved in play leading up to a shot.

Q: How do we measure if a striker is good at holding up the ball?
A: Players who are good at holding up the ball can receive long balls played up to them and retain the ball under pressure. They win ariels with a high percent and don't lose the ball.

Q: What can we infer from a striker that is good in terms of run quality?
A: Players who rank highly in making runs tend to be faster, as they use their pace to make threatening runs and receive the ball behind the defensive line.

Q: Why are aerials won a part of aerial threat?
A: While aerial threat primarily assesses a player's offensive danger in the air, it's important to consider their overall aerial strength. Players who consistently win aerial duels demonstrate greater aerial prowess and, consequently, a heightened aerial threat.

Q: How important are 'attacking aerials won' for a player's aerial threat?
A: Attacking aerials won'  are crucial for a player, indicating their ability to win headers in offensive situations, particularly in creating scoring opportunities or directing headers on target.

Q: What do we mean by holding up the ball?
A: A striker who can hold up the ball is able to receive the ball when a team is counterattcking, often via a long ball from deep in the team's own half. They can then keep control of the ball and find another player to lay it off to. This can be essential in the build up to attacks.

Q: Why are headed plays a part of aerial threat?
A: A player's ability to successfully pass the ball with their head and head the ball towards the goal is indicative of their aerial threat. It shows that they are able to control the ball with their head and to get into goal-scoring positions.

Q: What is a striker?
A: A striker is the football player whose primary role is to score goals or to assist other players in scoring goals. They often find themselves receiving the ball in the box or making runs to receive the ball high up the pitch.

Q: How do we measure if a striker is an aerial threat?
A: A striker who has a good success rate in aerials, wins many aerial dules and frequently makes headed plays, especially in the attacking half, is considered to be an aerial threat.

Q: What does it mean for a player to be an aerial threat?
A: Players who rank highly in aerial threat are threatining in the air offensively. They win a high percentage of their aerial duels, especially in the attacking 60 % of the field, and frequently make headed passes or headed shots.

Q: What does it mean for a striker to be good in poaching?
A: A striker who is good in poaching is making the most of their touches in the box. They shoot from very high-probability locations. Typically, these are players who are getting on the end of crosses and shooting mainly from first-time shots close to goal, rather than someone trying to create chances for themselves.

Q: What does it mean for a striker to be good in pressing?
A: Strikers who rank highly in defensive intensity are good in pressing. This means they are attempting a lot of defensive actions and winning the ball back.

Q: What measurements would convince us that a striker has a high aeriel threat?
A: A striker who wins aeriel duels, who ranks highly in attacking aeriels in particular is considered to have ariel threat.

Q: What metrics tell us that a striker is good at pressing?
A: A striker who presses well has lots high recoveries and makes interceptions. They have a high defence intensity and engage in counterpressing.

Q: How would we describe a player who is outstanding at aerial threat?
A: An outstanding player in this area is highly effective in winning aerial battles, arriving with good timing to balls from crosses, and contributing significantly to aerial dominance.

Q: How does a player's overall 'aerial threat' influence their role in set-pieces?
A: A player's overall 'aerial threat' directly influences their role in set-pieces. Players with high skill in aerial threat are often targeted in offensive set-pieces for headers.

Q: What makes a striker a good dribbler of the ball?
A: A good dribbler makes a high number of progressive runs and carries the ball into dangerous areas (high expected threat). They take the ball in to the box, have dribbles which lead to chances and can retain the ball under pressure. Dribbling is not always a quality we look for in a striker, but run quality includes some of these aspects.

Q: Explain why involvement can be important for a striker?
A: We often want strikers who help the team build up attacks. Involvement is high when a player drops in to midfield and passes to winger or attacking midfielders by laying the ball off to them. Once they have started the attack, a good striker will run towards the goal, in order to recieve a pass.

Q: What are the most important metrics/data-points for a striker?
A: How often they score (non-penalty goals per ninety) and how accurate their shooting is (non-penlashot conversion %) are two of the most important metrics for evaluating strikers.

Q: How is aerial threat measured?
A: Aerial threat is a weighted sum of a players performance compared to other players in the same position in aerials won (10%), aerials won % (15%), attacking aerials won (20%), attacking aerials won % (35%) and headed plays (20%).

Q: What makes a striker a good targetman?
A: A striker who is strong in primarily heading, but also a player who scores lots of goals and receives the ball in the box could be called a targetman.

Q: What are some attributes of a striker with a good run quality?
A: The key to a striker's run quality is making threatening runs with and without the ball and carrying the ball forward. Strikers who are good at runs take the ball into the box themselves and have a high number of penalty area receptions.

Q: Why is it important to have a striker with high pressing?
A: Strikers with high pressing are typically harder-working and are able to help the team's defence by spearheading their pressing attempts. They are very important to modern attacks which rely on pressing and counterpressing to win the ball back.

Q: What metrics does a striker rank well in if they are good at poaching?
A: A good poaching striker has a high number expected goals per shot (which means they come in to good shooting positions), as well as a high expected goals per touch.

Q: How do you describe a player with below average attacking aerials won adj in the opposition penalty area?
A: A player with below average attacking aerials won adj in the opposition penalty area might struggle with the physical or technical aspects of aerial play, often getting outmatched by defenders, which diminishes their effectiveness in creating scoring opportunities.

Q: What does poor attacking aerials won adj in the attacking central midfield and good attacking aerials won adj in the opposition penalty box show us about a player?
A: Poor attacking aerials won adj in the attacking central midfield and good attacking aerials won adj in the opposition penalty box shows that a player is comfortable contesting 1v1 headers from deep crosses, but might struggle to play as a target forward who receives the ball high on the pitch from lofted deliveries. It could be down to a comfort from lateral movement of the ball compared to the more vertical movement of a long ball from the defence.

Q: What does excellent attacking aerials won adj in the attacking left half-space tell us about a player?
A: A player with excellent attacking aerials won adj in the attacking left half-space is highly effective at leveraging their aerial strength to gain control and create opportunities, often setting up chances or scoring goals from aerial situations from second balls.

Q: How do you describe a player who has poor attacking aerials won adj in the attacking central midfield?
A: A player who has poor attacking aerials won adj in the attacking central midfield may not effectively utilize their aerial opportunities to advance play or might be physically outmatched, resulting in a loss of key battles that could otherwise pivot the game in their team's favor.

### Rule-based description of this player's data for this question
Dani Ortolan is average at aerial threat compared to other strikers. She is good at aerials won compared to other strikers. She is average at attacking aerials won, aerials won % and headed plays compared to other strikers. She is below average at attacking aerials won % compared to other strikers.

Daniela Maria Lopes Ortolan's attacking_aerials_won was outstanding in the defensive right wing compared to other strikers. Daniela Maria Lopes Ortolan performed excellent in the attacking left half-space and attacking left wing. Daniela Maria Lopes Ortolan performed good in the defensive right half-space. Daniela Maria Lopes Ortolan performed average in the attacking right wing, attacking right half-space, opposition penalty area, attacking central midfield and defensive left wing. Daniela Maria Lopes Ortolan performed below average in the defensive left half-space and defensive central midfield.

## Question 10: Does Dani Ortolan get involved in games?

### What the data means
(none)

### Rule-based description of this player's data for this question
(none)

## Answers to rate

### Answer b05-587f08 (to question 7)
Dani Ortolan demonstrates notable strengths in her finishing ability and non-penalty shot conversion percentage, indicating she has the potential to score goals effectively as a striker. However, her weaknesses in providing for teammates, run quality, and poor hold-up play suggest she may struggle to contribute to the build-up play and link with midfielders and wingers, which are essential attributes for a successful striker. In making this assessment, I have compared her skills as a striker to her current position and noted that, unlike wingers who often focus on creating chances and providing crosses, strikers typically need to combine goal-scoring prowess with more active involvement in both build-up and pressing, which Ortolan currently lacks.

### Answer b05-daa428 (to question 4)
Dani Ortolan has struggled to make an impact with her dribbling skills. While she can occasionally complete a dribble successfully, she often fails to create significant chances and tends to falter under pressure, making it difficult for her to contribute effectively in attacking situations.

Daniela Maria Lopes Ortolan demonstrated solid dribbling ability in the attacking central midfield, marking her as a competent playmaker among strikers. However, she faced challenges across various other areas, particularly in the opposition penalty area and attacking left half-space where her impact was minimal, highlighting a struggle to influence the game's flow when moving beyond the central zone.

### Answer b05-09af9e (to question 10)
Only modestly: in 823 minutes as a centre-forward she averaged about 14 touches and 17 receptions per 90 and was involved in about 25% of her team's possessions (207 of 843), falling to about 12 touches per 90 and 22% of possessions in 407 minutes as a second striker, so she's more of an end-of-move finisher (3 goals from 1.60 xG, 12 shots) than someone heavily involved in the build-up.

### Answer b05-89aa15 (to question 8)
Dani Ortolan struggles significantly with pressing in her role as a striker. Her lack of intensity and effectiveness in high recoveries and interceptions means she does not contribute significantly to her team's defensive efforts.

Daniela Maria Lopes Ortolan showcases an excellent defensive commitment within her own penalty area, indicating a solid foundational aspect of her game. However, her overall defensive contributions are relatively mixed across the pitch, with average performances in various central and wide areas, but notably below average on the right side and poor in the attacking right half-space.

### Answer b05-fac20f (to question 9)
Dani Ortolan shows a solid ability to win aerial duels, ranking well in that aspect compared to her peers. However, she struggles with her success rate in attacking situations and her overall aerial threat remains typical.

Daniela Maria Lopes Ortolan has been impressive at winning aerial duels on the defensive right wing, showcasing her aerial prowess in that area more than other strikers. Additionally, she displays excellent ability in the attacking left half-space and left wing, adding a significant threat to her game there, while maintaining decent aerial performances across various other positions, including the opposition penalty area. However, she struggles to impact the game significantly in the defensive left half-space and central midfield.

### Answer b05-aa5bf0 (to question 4)
Across about 1,250 league minutes in 2026, mostly at centre-forward with some time as a second striker, Dani Ortolan tried only 5 dribbles and completed 4, which is 80%. That works out to roughly 0.36 attempts per 90, so dribbling is a very small part of her game, and the success rate means little on such a small sample. Her carrying shows the same pattern: 19 carries, all completed, for only about 0.35 total xT, and only 0.05 xG came from her dribbles. She's better described as a target and hold-up striker who draws fouls (29 suffered) and keeps the ball about 62% of the time under pressure, rather than as a real dribbling threat. I didn't compare her with other strikers in the league.

### Answer b05-7f8046 (to question 8)
Dani Ortolan's pressing ability in the Brazilian Brasileiro Women's 2026 season showed mixed results. She managed defensive actions every game, with notable intensities in some matches, including a standout performance with 7 defensive duels and 6 tackles in one game. However, her counter-pressing numbers were low, as evidenced by only a few counterpresses and possessions won. While she displayed decent defensive duels success rates, her overall defensive output suggests room for improvement in creating recoveries or disrupting opponent plays effectively.

### Answer b05-9e0637 (to question 3)
Ortolan's passing quality leaves much to be desired, with significant struggles indicating she is less impactful in creating chances through her passing. She does not demonstrate consistency in delivering threatening passes or providing opportunities for her teammates.

Ortolan shows moderate passing abilities in the defensive central midfield and left half-space areas but finds it challenging to impact the game elsewhere. Her performance significantly dips in attacking positions, especially on the left side and in the opposition's penalty area, indicating struggles to create from those zones.

### Answer b05-5c4fb1 (to question 6)
Dani Ortolan wins the ball back very rarely: in the zones I could see, she has only 2 recorded ball recoveries all season, one on the attacking-half left wing (as a second striker) and one on the attacking-half right wing (as a centre-forward). Most of her defensive work happens on the attacking-half left wing, with 6 defensive actions and 4 of 7 defensive duels won (as CF, LW and SS), plus 3 defensive actions in the attacking central zone and 5 in her own box, the box ones mostly aerial duels at defensive set pieces. The data output was cut off, so I couldn't check the penalty box or her own-half zones beyond her own box, but the visible numbers point to a forward who presses mainly down the left in the opposition half.

### Answer b05-242288 (to question 10)
There was an error getting the data.

### Answer b05-9bd9a8 (to question 5)
Not much, on this evidence: Dani Ortolan scores efficiently when she gets chances, but she rarely gets on the ball in the box. In about 1,250 league minutes in 2026, mostly at centre-forward, she has 4 goals (3 not from penalties, plus 1 of 2 penalties scored) from 15 non-penalty shots worth about 2.0 xG. Per 90 minutes, that comes to roughly 1.1 shots, 0.14 xG and only about 1.1 touches in the box, with 26 passes received in the penalty area all season. When she does get there she is dangerous, at about 0.13 xG per box touch, so the problem is getting her into the box more often rather than her finishing, especially since her side has only about 39% of the ball in her centre-forward minutes.

### Answer b05-0d5035 (to question 9)
Dani Ortolan's aerial ability is below average when assessed in the Brazilian Brasileiro Women 2026 season. She participated in 20 aerial duels across several matches but was successful only 7 times, yielding a winning percentage of 35%. Specifically, her attacking aerial duel success rate was 32%, while her defensive aerial duel success rate was slightly better at 40%. This indicates that while she is involved in a number of aerial contests, she struggles to assert consistent dominance in the air. Her aerial prowess is an area that likely needs improvement to make her more effective as a striker.

### Answer b05-3e378e (to question 1)
Dani Ortolan, a 28-year-old Brazilian, has played about 1,250 minutes in the 2026 Brasileiro Women, which is roughly 14 full matches. She has mostly led the line as a centre-forward (about 823 minutes) and also spent around 407 minutes as a second striker, with brief spells on either wing. She has scored 4 goals from 17 shots (3 of them non-penalty goals, plus 1 scored from 2 penalties) on about 2.0 xG, so she is finishing slightly above expectation at around 0.29 goals per 90. Her creative output has been low, with no assists, 2 key passes, 4 shot assists and just 0.12 xA, and she has completed only about 72% of her passes. Her team has averaged only around 40% possession in her matches, so she has done a lot of work off the ball: 29 interceptions, 29 fouls won and about 62% of the ball kept under pressure. Her duels have been weaker, though, with only about 32% of 68 aerials and 24% of 74 defensive duels won, so overall she has been an efficient but low-volume striker in a team that often doesn't have the ball.

### Answer b05-251ad1 (to question 2)
Dani Ortolan's strengths lie in her finishing ability and defensive heading, making her a reliable goal-scorer who maximizes her chances and a significant aerial presence in defense. However, her weaknesses in involvement and progression indicate that she may not frequently engage in build-up play or contribute effectively to advancing the ball, which could limit her overall impact on the team's offensive dynamics.

### Answer b05-18f2cd (to question 4)
Dani Ortolan has shown strong dribbling abilities during the 2026 Brazilian Brasileiro Women season. She successfully completed all 12 of her carries (100% success rate), which highlights her commendable ball control. Additionally, she attempted six dribbles, out of which four were successful, resulting in an overall success rate of 66.7%. Her dribbling contributions also generated expected threat values (xT) of 0.1226, showcasing her effectiveness in progressing the ball through dribbles.

### Answer b05-2d1690 (to question 1)
Dani Ortolan is a striker who has shown some promise in front of goal, particularly when it comes to finishing. This season, she has demonstrated her ability to convert opportunities effectively, boasting a strong shot conversion percentage and a respectable number of goals per box touch. However, her overall contribution to the team has been limited, as she struggles in providing for her teammates and lacks significant involvement in build-up play, reflected in her low touch count. Additionally, Ortolan exhibits weaknesses in hold-up play, especially under pressure, making it difficult for her to retain possession. She also falls short in pressing and defensive contributions, with a low number of high recoveries. Overall, while Ortolan has the potential to be a reliable goalscorer, her lack of involvement and overall team play may hinder her effectiveness in a more dynamic attacking role.

### Answer b05-eaa5f3 (to question 7)
In the 2026 Brasileirão Women season, Dani Ortolan primarily played as a center-forward (CF) but also contributed as a second striker (SS) and occasionally as a left-winger (LW) or right-winger (RW). Historically, she has also played in midfield and various attacking roles during previous seasons. While her main expertise lies in forward positions, she has demonstrated versatility to adapt to other roles when needed.

### Answer b05-204800 (to question 9)
In the air, Dani Ortolan is a weak striker. In about 1,250 minutes of the 2026 Brasileiro Women season, she won only 22 of 68 aerial duels, or 32%, which is well below what you would want from a centre-forward. She contests plenty of high balls, roughly 4.9 per 90, so she is often used as a target, but she rarely comes out on top. Her attacking aerials are the weakest part, with 14 won out of 51 (about 27%), and as a second striker she won just 3 of 15. She does better on defensive headers, winning 15 of 35 (about 43%), but she made only 6 headed plays all season, so there is little sign that heading adds anything to her attacking game.

### Answer b05-120899 (to question 5)
Dani Ortolan struggles to make a significant impact in the box, as evidenced by her below-average numbers in several key metrics, including touches in the box and box entries from carries. While she manages to score and receive the ball in the penalty area at an average level, her overall box threat is noticeably limited compared to her peers.

Daniela Maria Lopes Ortolan displayed average finishing ability in the six-yard box, indicating she can capitalize on close-range opportunities. However, her performance drops significantly when attempting shots from the outside of the box and within the golden zone.

### Answer b05-2ff662 (to question 3)
Dani Ortolan has shown mixed passing abilities during the 2026 Brasileiro Women season while primarily playing as a striker. Across matches, her pass accuracy varied significantly, from 50% to 100%, averaging between 12-17 passes per match. However, her ability to contribute progressive passes, creative plays, key passes, or assists has been generally low, limiting her impact in playmaking. Her best games showed an improvement in delivering precise passes and some contribution to xThreat.

### Answer b05-c31280 (to question 1)
Dani Ortolan had a noteworthy season in the 2026 Brasileiro Women, playing across multiple attacking positions—center-forward, support striker, left winger, and right winger. She logged 1,252 minutes, with most of her time spent as a center-forward (66% of total minutes) and support striker (33%). Her productivity was solid, scoring three goals (two non-penalty) and converting one penalty from two attempts. With 12 shots and a conversion rate of 20%, her expected goals (xG) total was 1.6, outperforming her xG by 0.4. She contributed to building play as well, adding 2 key passes and creating 0.1 xG via assists. While her defensive output was modest, she managed 15 interceptions and maintained a tackle success rate of 57% when defensive duels were attempted.

### Answer b05-fbc815 (to question 6)
Daniela Maria Lopes Ortolan shows a commendable ability to defend effectively in her own penalty area for a striker. However, her contributions drop off significantly in other areas of the pitch, particularly in the attacking third and on the right side. Overall, while she excels in protecting her goal, her defensive effectiveness diminishes as she moves further up the field.

### Answer b05-9ee988 (to question 7)
Yes, and the best fit is second striker: in 2026 she played 407 of her 1,253 league minutes there (32.5%), with the rest almost all at centre-forward (823 minutes, 65.7%), so she already splits her time between the two. She has also played wide before, mostly in 2021, when 43% of her 599 minutes came at left wing (96), right wing (69), right wing-forward (46) and left attacking midfield (66), and in 2020, when 27% came on the wings. She has barely played wide in 2026 (about 22 minutes), so a move to the wing would rely on what she did in earlier seasons, while I only looked at where she played, not how well she performed in each position.

### Answer b05-beb490 (to question 10)
Dani Ortolan gets moderately involved in games with a consistent presence in both offensive and defensive metrics, showing activity in receptions, passes, and occasional goal-scoring contributions.

### Answer b05-ac5ff2 (to question 2)
Dani Ortolan excels in aerial duels, contributing positively in attacking positions with goals and effective touches in the penalty area. However, her weaknesses include low efficiency in progressive passing, possession involvement, and minimal ball progression metrics.

### Answer b05-8ffdc6 (to question 5)
Currently, I could not retrieve specific goal-scoring metrics for Dani Ortolan. Further details such as total shots or goal conversion for her shot locations, including the penalty area, are needed to determine her threat level in the box definitively. Would you like me to attempt retrieving this data again or provide generalized insights?

### Answer b05-4c03ef (to question 2)
Strengths: Dani Ortolan has been a clinical finisher. She has scored 4 goals (3 non-penalty, plus 1 of 2 penalties) from about 1.9 xG across roughly 1,230 minutes as a centre-forward and second striker, and she wins plenty of fouls (29 drawn), holds the ball well under pressure (59% as a CF, 70% as a second striker) and completed 4 of her 5 dribbles.

Weaknesses: She offers little physically or as a creator, winning only 33% of her aerials as a CF (27% as a second striker) and 19–27% of her defensive duels, and she has 0 assists, just 0.12 xA, 3 progressive passes and only about 1.1 non-penalty shots per 90 minutes as a CF, so her scoring relies on finishing efficiency rather than volume.

### Answer b05-3d383a (to question 3)
Passing is not a strong part of Dani Ortolan's game, though I only have her own numbers and didn't compare her with other strikers in the league. In about 1,250 minutes of the 2026 Brasileiro Women, she made 163 passes, or roughly 12 per 90 minutes, and completed 119 of them (73%). That's 72% in her main centre-forward role and 78% when she played just behind the striker. She rarely moves the ball forward or sets up chances: she made only 5 progressive passes and 2 key passes all season, had 4 passes that led to shots, completed 2 of 6 crosses, got no assists and created just 0.12 expected assists. Her passing is mostly simple link-up play, while her value comes from scoring (4 goals from about 1.9 expected goals) and from her work off the ball rather than from creating chances.

### Answer b05-1c7f9e (to question 6)
Dani Ortolan predominantly wins the ball back in attacking zones, particularly in the left and right halves and wings of the attacking half, as well as the central areas. She has contributed notable defensive actions, such as duels, aerial challenges, and ball recoveries, in these zones. Her involvement in defensive work extends occasionally into her own box, showcasing her ability to drop back when needed, particularly strong in aerial duels in defensive situations.

### Answer b05-165149 (to question 8)
Dani Ortolan works hard without the ball, but her pressing doesn't win it back often enough to call her a good presser. In about 823 minutes as a centre-forward she had 45 defensive duels (around 4.9 per 90) but won only 27%, with 7 counterpresses, just 1 of which led to a recovery, and only 1 high recovery all season. In about 407 minutes as a second striker she pressed more often (8 counterpresses and 27 duels, roughly 1.8 and 6 per 90), but her duel win rate fell to 19% and she won possession just twice. Overall she gives a willing pressing effort, but her low success rates and very few high regains mean it adds little defensively, though I haven't compared her with other strikers in the league to confirm that.

## Results file
Write your ratings to: /Users/davsu428/GitHub/vivid-report/papers/0002-twelve-earpiece/Code/outputs/wordalisation-test/agent-judge/results-05.jsonl