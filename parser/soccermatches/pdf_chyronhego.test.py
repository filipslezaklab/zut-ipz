#!/usr/bin/python3
import os, jsonschema, json, argparse

from pdf_chyronhego import match_report_from_pdf

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
JSON_SCHEMA_FILE = os.path.join(BASE_DIR,"..","match_report.schema.json")

with open(JSON_SCHEMA_FILE) as FILE:
  JSON_SCHEMA = json.loads(FILE.read())

def test(json_str:str)->bool:
    jsonschema.validate(
      json.loads(json_str),
      JSON_SCHEMA
    )
    return True

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
    pass
  elif os.path.isfile(args.input):
    match_report = match_report_from_pdf(args.input)
    test(match_report.to_json())
