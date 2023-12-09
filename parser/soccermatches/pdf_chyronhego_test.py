#!/usr/bin/python3
import os, jsonschema, json, argparse
import pandas as pd, numpy as np

from pdf_chyronhego import match_report_from_pdf

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
JSON_SCHEMA_FILE = os.path.join(BASE_DIR,"..","match_report.schema.json")

with open(JSON_SCHEMA_FILE) as FILE:
  JSON_SCHEMA = json.loads(FILE.read())

def test_directory(dir_name:str)->'pd.DataFrame':
  
  out = pd.DataFrame(
    data=[],
    columns=[
      "status",
      "message",
    ]
  )
  
  for root, dirs, files in os.walk(dir_name):
    for file in files:
      if ".pdf" not in file:
        continue

      try:
        match_report = match_report_from_pdf(
          os.path.join(root,file)
        )
      except Exception as err:
        out.loc[
          os.path.join(root,file)
        ] = {
          "status":1,
          "message":str(err),
        }
        continue

      try:
        jsonschema.validate(
          json.loads(match_report.to_json()),
          JSON_SCHEMA
        )
      except Exception as err:
        out.loc[
          os.path.join(root,file)
        ] = {
          "status":2,
          "message":str(err),
        }
        continue

      out.loc[
        os.path.join(root,file)
      ] = {
        "status":0,
        "message":"ok! :)",
      }
  
  return out


if __name__ == "__main__":
  args_parser = argparse.ArgumentParser(
    description="CLI utility for testing parser",
  )
  args_parser.add_argument(
    "-i","--input",
    required=True,
    help="test pdf file or directory with test pdf files",
  )

  args = args_parser.parse_args()

  if os.path.isdir(args.input):
    file_cnt = 0
    for root, dirs, files in os.walk(args.input):
      for file in files:
        if ".pdf" not in file: continue
        file_cnt += 1
    msg = f"found {file_cnt} .pdf files to test! running tests..."
    print(msg,flush=True)
    print("-"*len(msg),flush=True)

    test_results = test_directory(args.input)
    test_summary = pd.DataFrame.from_dict(
      dict(zip(
        ("status", "cnt"),
        np.unique(test_results["status"],return_counts=True)
      ))
    )
    test_summary["message"] = test_summary["status"].map({
      0:"ok!",
      1:"failed parse!",
      2:"parsed, failed validation!",
    })
    test_summary["percent"] = test_summary["cnt"]/np.sum(test_summary["cnt"])
    print(test_summary.to_string(index=False))
    quit(0)

  elif os.path.isfile(args.input):
    try:
      match_report = match_report_from_pdf(
        args.input
      )
    except Exception as err:
      print("failed parse!")
      print("-------------")
      print(str(err))
      quit(1)
    
    try:
      jsonschema.validate(
        json.loads(match_report.to_json()),
        JSON_SCHEMA,
      )
    except Exception as err:
      print("parsed, failed validation!")
      print("--------------------------")
      print(str(err))
      quit(2)

    print("ok! :)")
    print("------")
    quit(0)
  
  print(f"'{args.input}' doesn't seem to be valid file or directory!")
  quit(1)
