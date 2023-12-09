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
- ~~testing~~

#### Test Results
```
found 824 .pdf files to test! running tests...
----------------------------------------------
 status  cnt                    message  percent
      0  622                        ok! 0.754854
      1   17              failed parse! 0.020631
      2  185 parsed, failed validation! 0.224515
```

schema in `matchreport.schema.json` should be _final_
