#!/usr/bin/python3

import argparse, os

from pdf_chyronhego import match_report_from_pdf

if __name__ == "__main__":

  args_parser = argparse.ArgumentParser(
    prog="parse",
    description="CLI utility meant for prasing PDF's",
  )

  args_parser.add_argument(
    "-i","--input",
    required=True,
    help="pdf file to be converted",
  )

  args_parser.add_argument(
    "-o","--output",
    default=None,
    help="output file to be written to. "+
         "If none is provided: output will be "+
         "printed out to standard output.",
  )

  args_parser.add_argument(
    "-f","--format",
    choices=["json","csv","xml"],
    default="json",
    help="output format of parsed pdf",
  )

  args_parser.add_argument(
    "--json-pretty",
    action='store_true',
    help="output human-readable json",
  )

  args = args_parser.parse_args()
  
  if os.path.isfile(args.input) == False:
    raise FileNotFoundError(f"file '{args.input}' not found!")
  
  match_report = match_report_from_pdf(args.input)

  if args.json_pretty == True:
    print(match_report.to_json(indent=4))
    quit(0)
  print(match_report.to_json())
  
  
  