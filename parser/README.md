# IPZ Project PDF serializer CLI program

### Set Up:
```sh
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### Usage:
```sh
./venv/bin/python3 ./soccermatches/pdf_parse.py -i {INPUT PDF FILE}
# >>> json on stdout
```

##### #TODO:
- switch from `pip` and `venv` to `poetry`
- fix regexes
- ~~fix output types~~
- ~~parse pages 2 and 3~~
- adhere to schema
- testing

schema in `matchreport.schema.json` should be _final_
