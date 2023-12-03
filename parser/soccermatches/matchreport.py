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
    ]
  )
  meta = pd.DataFrame(
    data=[],
    columns=[
      "date",
      "stadium",
      "duration",
      "net_play_time",
      "duration_1st",
      "duration_2nd",
    ]
  )

  def to_json(self,**kwargs)->str:
    return json.dumps({
      "meta"    : json.loads(
        self.meta.transpose()[0].to_json()
      ),
      "summary" : json.loads(
        self.summary.transpose().to_json()
      ),
    },ensure_ascii=False,**kwargs)
  
  def __repr__(self) -> str:
    return "report from match '{}' vs '{}' [@{}]".format(
      self.summary.index[0],
      self.summary.index[1],
      str(self.meta["date"].iloc[0])
    )