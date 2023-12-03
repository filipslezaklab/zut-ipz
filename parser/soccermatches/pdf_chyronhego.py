import PyPDF2, re, datetime
from matchreport import MatchReport

ALLOW_MISSING = True

def match_report_from_pdf(
    file_name:str,
  )->'MatchReport':
  
  pdf = PyPDF2.PdfReader(file_name)
  pg1 = pdf.pages[0]
  pg0_txt = pg1.extract_text()

  m = re.search(
    "\d{4}-\d{2}-\d{2}, \d{2}:\d{2}",
    pg0_txt,
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
    "\n.*NET PLAYING TIME.*\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    playing_time = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ]
    [playing_time , playing_time_net,
    playing_time_1st, playing_time_2nd] = re.findall(
      "\d*:?\d+:\d+",playing_time
    )
    # TODO str->seconds
  else:
    playing_time     = None
    playing_time_net = None
    playing_time_1st = None
    playing_time_2nd = None

  m = re.search(
    "\n.*\n\d{4}-\d{2}-\d{2}, \d{2}:\d{2}",
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
    "\n.*\nv\n.*\n",
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
    "\n\s*[\d?\d:?]+ \(.*\)"+
    "\n\s*NET POSS\. TIME"+
    "\n\s*[\d?\d:?]+ \(.*\)\n",
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
    "\n\d+.\d\dm\nDISTANCE\n\d+.\d\dm\n",
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
    "\n.* \(\d+\.\d+km/h\)\nTOP SPEED\n.* \(\d+\.\d+km/h\)\n",
    pg0_txt,
  )
  if m is not None and ALLOW_MISSING:
    top_speed1,_,top_speed2 = pg0_txt[
      m.span()[0]+1:m.span()[1]-1
    ].split("\n")
    top_speed_player1, top_speed1 = top_speed1.split("(")
    top_speed_player2, top_speed2 = top_speed2.split("(")
    top_speed_player1 = top_speed_player1.strip()
    top_speed_player2 = top_speed_player2.strip()
    top_speed1 = float(top_speed1[:-5])
    top_speed2 = float(top_speed2[:-5])
  else:
    top_speed_player1 = None
    top_speed_player2 = None
    top_speed1        = None
    top_speed2        = None

  m = re.search(
    "\n.* \(\d+\.\d+m\)\nMAX DISTANCE\n.* \(\d+\.\d+m\)\n",
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
    "\n.* \(\d+\)\s*MAX SPRINTS\s*.* \(\d+\)\n",
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

  out = MatchReport()
  
  out.summary.loc[0]={
    "team_name"           : team1,
    "goals"               : goals1 ,
    "possession"          : possession1 ,
    "net_poss_time"       : net_poss_time1 ,
    "net_poss_time_1st"   : net_poss_time_1st1 ,
    "net_poss_time_2nd"   : net_poss_time_2nd1 ,
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
  }

  out.summary.loc[1]={
    "team_name"           : team2,
    "goals"               : goals2 ,
    "possession"          : possession2 ,
    "net_poss_time"       : net_poss_time2 ,
    "net_poss_time_1st"   : net_poss_time_1st2 ,
    "net_poss_time_2nd"   : net_poss_time_2nd2 ,
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
  }

  out.meta.loc[0]={
      "date"              : match_date,
      "stadium"           : stadium,
      "duration"          : playing_time,
      "net_play_time"     : playing_time_net,
      "duration_1st" : playing_time_1st,
      "duration_2nd" : playing_time_2nd,
  }

  return out