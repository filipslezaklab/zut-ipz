import PyPDF2, re, datetime
from matchreport import MatchReport
from typing import Tuple, List, Dict
import pandas as pd

ALLOW_MISSING = True

RE_TIME = "\d*:?\d*:\d\d"
RE_NUMBER = "\d+\.?\d+"
RE_DATETIME = "\d{4}-\d{2}-\d{2}, \d{2}:\d{2}"

def str_time_to_seconds(s:str)->int:
  '''
  turns string formated as \
  `'hh:mm:ss'`/`'mm:ss'`/`'ss'` \
  into number of seconds \
  '''
  out = 0
  for i,v in enumerate(s.split(":")[::-1]):
    out += int(v) * ( 60**i )
  return out

def physical_overview_from_page(
    page_txt:str
  )->'pd.DataFrame':
  RE_PLAYER_ROW = "".join(
    ["\n" , "[^\n]+", RE_TIME ] + 
    ["\n" + "[^\n]+" ] * 12
  )
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
    "distance_3",
    "distance_2",
    "distance_1",
  ]
  data = []
  for player_row in re.findall(RE_PLAYER_ROW,page_txt):
    r = player_row.split("\n")
    m = re.search(RE_TIME,r[1])
    r[0] = r[1][:m.span()[0]]
    r[1] = r[1][m.span()[0]:]
    data += [dict(zip(columns,r))]
  data = pd.DataFrame(data)
  data[data=="None"]=0
  data["seconds_played"] = data["seconds_played"].map(str_time_to_seconds)

  columns_numeric = [
    "total_distance", "top_speed"  ,"avg_speed"  ,
    "sprints_dist"  , "hsr_dist"   ,"distance_4" ,
    "distance_3"    , "distance_2" ,"distance_1" ,
  ]
  data[columns_numeric] = data[columns_numeric].astype(float)

  columns_int = [
    "seconds_played","high_intensity_activity","sprints_no","hst_no"
  ]
  data[columns_int] = data[columns_int].astype(int)

  return data
  

def summary_from_page(
    pg0_txt:str
  )->Tuple[Dict,Dict]:

  m = re.search(
    RE_DATETIME, pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    match_date = pg0_txt[
      m.span()[0]:m.span()[1]
    ]
    match_date = datetime.datetime.strptime(
      match_date,"%Y-%m-%d, %H:%M"
    )
  else:
    match_date = None


  m = re.search(
    "\n[^\n]*NET PLAYING TIME[^\n]*\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    playing_time = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ]
    [
      playing_time ,
      playing_time_net,
      playing_time_1st,
      playing_time_2nd
    ] = re.findall(
      RE_TIME,playing_time
    )
    # TODO str->seconds
  else:
    playing_time     = None
    playing_time_net = None
    playing_time_1st = None
    playing_time_2nd = None

  m = re.search(
    "\n[^\n]*\n" + RE_DATETIME,
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    stadium = pg0_txt[
      m.span()[0]:m.span()[1]
    ]
    stadium = stadium.strip().split("\n")[0]
  else:
    stadium = stadium

  m = re.search(
    "\n[^\n]*\nv\n[^\n]*\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    team1,_,team2 = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ].split("\n")
  else:
    team1 = None
    team2 = None


  m = re.search(
    "\s\d+ - \d+\s",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    goals1,goals2 = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ].split("-")
    goals1 = int(goals1)
    goals2 = int(goals2)
  else:
    goals1 = None
    goals2 = None


  m = re.search(
    "\n\d+%\nPOSSESSION\n\d+%\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    possession1,_,possession2 = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ].split("\n")
    possession1 = float(possession1.replace("%",""))/100.0
    possession2 = float(possession2.replace("%",""))/100.0
  else:
    possession1 = None
    possession2 = None


  m = re.search(
    "\n\s*[\d?\d:?]+ \([^\n]*\)"+
    "\n\s*NET POSS\. TIME"+
    "\n\s*[\d?\d:?]+ \([^\n]*\)\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    net_poss_time1,_,net_poss_time2 = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ].split("\n")
    net_poss_time1,net_poss_time_1st1,net_poss_time_2nd1 = re.findall(
      "\d+:\d+",net_poss_time1
    )
    net_poss_time2,net_poss_time_1st2,net_poss_time_2nd2 = re.findall(
      "\d+:\d+",net_poss_time2
    )
    #TODO: str -> seconds
  else:
    net_poss_time1     = None
    net_poss_time_1st1 = None
    net_poss_time_2nd1 = None
    net_poss_time2     = None
    net_poss_time_1st2 = None
    net_poss_time_2nd2 = None


  m = re.search(
    "\n\d+.\d+m\nDISTANCE\n\d+.\d+m\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    distance1,_,distance2 = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ].split("\n")
    distance1 = float(distance1[:-1])
    distance2 = float(distance2[:-1])
  else:
    distance1 = None
    distance2 = None


  m = re.search(
    "\n\d+\nSPRINTS\n\d+\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    sprints1,_,sprints2 = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ].split("\n")
    sprints1 = int(sprints1)
    sprints2 = int(sprints2)
  else:
    sprints1 = None
    sprints2 = None



  m = re.search(
    "\n\d+\nHIGH SPEED RUNS\n\d+\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    high_speed_runs1,_,high_speed_runs2 = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ].split("\n")
    high_speed_runs1 = int(high_speed_runs1)
    high_speed_runs2 = int(high_speed_runs2)
  else:
    high_speed_runs1 = None
    high_speed_runs2 = None



  m = re.search(
    "\n\d+\.\d+m\nSPRINT DISTANCE\n\d+\.\d+m\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    sprint_distance1,_,sprint_distance2 = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ].split("\n")
    sprint_distance1 = float(sprint_distance1[:-1])
    sprint_distance2 = float(sprint_distance2[:-1])
  else:
    sprint_distance1 = None
    sprint_distance2 = None




  m = re.search(
    "\n[^\n]* \(\d+\.\d+km/h\)\nTOP SPEED\n[^\n]* \(\d+\.\d+km/h\)\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    top_speed1_full,_,top_speed2_full = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ].split("\n")
    top_speed1 = re.findall("\([^()]*\)",top_speed1_full)[-1]
    top_speed_player1 = top_speed1_full[:-len(top_speed1)].strip()
    top_speed1 = float(top_speed1[1:-1].replace("km/h",""))

    top_speed2 = re.findall("\([^()]*\)",top_speed2_full)[-1]
    top_speed_player2 = top_speed1_full[:-len(top_speed2)].strip()
    top_speed2 = float(top_speed2[1:-1].replace("km/h",""))
  else:
    top_speed_player1 = None
    top_speed_player2 = None
    top_speed1        = None
    top_speed2        = None

  m = re.search(
    "\n[^\n]* \(\d+\.\d+m\)\nMAX DISTANCE\n[^\n]* \(\d+\.\d+m\)\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    max_distance1,_,max_distance2 = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ].split("\n")
    max_distance_player1, max_distance1 = max_distance1.split("(")
    max_distance_player2, max_distance2 = max_distance2.split("(")
    max_distance_player1 = max_distance_player1.strip()
    max_distance_player2 = max_distance_player2.strip()
    max_distance1 = float(max_distance1[:-2])
    max_distance2 = float(max_distance2[:-2])
  else:
    max_distance_player1 = None
    max_distance_player2 = None
    max_distance_player1 = None
    max_distance_player2 = None
    max_distance1        = None
    max_distance2        = None


  m = re.search(
    "\n[^\n]* \(\d+\)\s*MAX SPRINTS\s*[^\n]* \(\d+\)\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    max_sprints1,_,max_sprints2 = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ].split("\n")
    max_sprints_player1, max_sprints1 = max_sprints1.split("(")
    max_sprints_player2, max_sprints2 = max_sprints2.split("(")
    max_sprints_player1 = max_sprints_player1.strip()
    max_sprints_player2 = max_sprints_player2.strip()
    max_sprints1 = int(max_sprints1[:-1])
    max_sprints2 = int(max_sprints2[:-1])
  else:
    max_sprints_player1  = None
    max_sprints_player2  = None
    max_sprints_player1  = None
    max_sprints_player2  = None
    max_sprints1         = None
    max_sprints2         = None
  
  summary = [{
    "team_name"           : team1,
    "goals"               : goals1 ,
    "possession"          : possession1 ,
    "net_poss_time"       : str_time_to_seconds(net_poss_time1) ,
    "net_poss_time_1st"   : str_time_to_seconds(net_poss_time_1st1) ,
    "net_poss_time_2nd"   : str_time_to_seconds(net_poss_time_2nd1) ,
    "distance"            : distance1 ,
    "sprints"             : sprints1 ,
    "high_speed_runs"     : high_speed_runs1 ,
    "sprint_distance"     : sprint_distance1 ,
    "top_speed"           : top_speed1 ,
    "top_speed_player"    : top_speed_player1 ,
    "max_distance"        : max_distance1 ,
    "max_distance_player" : max_distance_player1 ,
    "max_sprints"         : max_sprints1 ,
    "max_sprints_player"  : max_sprints_player1 ,
  },
  {
    "team_name"           : team2,
    "goals"               : goals2 ,
    "possession"          : possession2 ,
    "net_poss_time"       : str_time_to_seconds(net_poss_time2) ,
    "net_poss_time_1st"   : str_time_to_seconds(net_poss_time_1st2) ,
    "net_poss_time_2nd"   : str_time_to_seconds(net_poss_time_2nd2) ,
    "distance"            : distance2 ,
    "sprints"             : sprints2 ,
    "high_speed_runs"     : high_speed_runs2 ,
    "sprint_distance"     : sprint_distance2 ,
    "top_speed"           : top_speed2 ,
    "top_speed_player"    : top_speed_player2 ,
    "max_distance"        : max_distance2 ,
    "max_distance_player" : max_distance_player2 ,
    "max_sprints"         : max_sprints2 ,
    "max_sprints_player"  : max_sprints_player2 ,
  }]
  summary = pd.DataFrame(summary)

  meta = [{
      "date"              : match_date,
      "stadium"           : stadium,
      "duration"          : str_time_to_seconds(playing_time),
      "playtime"          : str_time_to_seconds(playing_time_net),
      "playtime_1st"      : str_time_to_seconds(playing_time_1st),
      "playtime_2nd"      : str_time_to_seconds(playing_time_2nd),
  }]
  meta = pd.DataFrame(meta)

  return summary , meta


def match_report_from_pdf(
    file_name:str,
  )->'MatchReport':
  
  pdf = PyPDF2.PdfReader(file_name)
  
  pg0_txt = pdf.pages[0].extract_text()
  pg1_txt = pdf.pages[1].extract_text()
  pg2_txt = pdf.pages[2].extract_text()

  out = MatchReport()
  out.summary, out.meta = summary_from_page(pg0_txt)
  out.physical_overview[0]["players"] = physical_overview_from_page(pg1_txt)
  out.physical_overview[1]["players"] = physical_overview_from_page(pg2_txt)
  out.physical_overview[0]["team_name"] = out.summary.loc[0]["team_name"]
  out.physical_overview[1]["team_name"] = out.summary.loc[1]["team_name"]

  return out