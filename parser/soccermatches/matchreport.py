import json, pandas as pd
from typing import *

class MatchReport:
  summary = pd.DataFrame(
    data=[],
    columns=[
      "team_name",
      "goals",
      "possession",
      "net_poss_time",
      "net_poss_time_1st",
      "net_poss_time_2nd",
      "distance",
      "sprints",
      "high_speed_runs",
      "sprint_distance",
      "top_speed",
      "top_speed_player",
      "max_distance",
      "max_distance_player",
      "max_sprints",
      "max_sprints_player"
    ],
    index=[0]
  )

  meta = pd.DataFrame(
    data=[],
    columns=[
      "stadium",
      "date",
      "duration",
      "playtime",
      "playtime_1st",
      "playtime_2nd",
    ],
    index=[0,1]
  )

  physical_overview = [{
    "team_name":"",
    "players":pd.DataFrame(
      data=[],
      columns=[
        "player_name",
        "seconds_played",
        "total_distance",
        "top_speed",
        "avg_speed",
        "high_intensity_activity",
        "sprints_dist",
        "sprints_no",
        "hsr_dist",
        "hst_no",
        "distance_4",
        "distance_4",
        "distance_4",
        "distance_4",
      ]
    ),
  }]*2

  def to_json(self,indent=None)->str:
    return json.dumps({
      "meta"    : json.loads(
        self.meta.transpose()[0].to_json()
      ),
      "summary" : [i for i in self.summary.transpose().to_dict().values()],
      "physical_overview" : [
        {
          "team_name":self.physical_overview[0]["team_name"],
          "players":[
            i for i in
            self.physical_overview[0]['players'
              ].transpose().to_dict().values()
          ]
        },
        {
          "team_name":self.physical_overview[1]["team_name"],
          "players":[
            i for i in
            self.physical_overview[1]['players'
              ].transpose().to_dict().values()
          ]
        },
      ]
    },ensure_ascii=False,indent=indent)
  
  def __repr__(self) -> str:
    return "report from match '{}' vs '{}' [@{}]".format(
      self.summary.index[0],
      self.summary.index[1],
      str(self.meta["date"].iloc[0])
    )