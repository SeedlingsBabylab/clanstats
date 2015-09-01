# clanstats



## usage

### clanstats.py

This script will output the long form speaker/classifier data when given a single .cex clan file. It takes 3 arguments.

``` bash
$: python clanstats.py  /path/to/clanfile.cex   /path/to/output   window_size
```

### cs_folder.py

This script will run clanstats.py on every clan file in a directory passed as argument.

``` bash
$: python cs_folder.py  /path/to/clanfiles/  /output/path/
```

This script also produces a single .csv file containing the aggregate data from all the files it just processed (named aggregate_long.csv). It'll combine all the .csv's in the output directory (that was originally passed as an argument), so if you have .csv files in there that weren't a result of what cs_folder.py just did, it'll combine those as a part of the aggregate_long.csv output as well. Make sure there's only .csv files in the output directory or else the script will throw an error when trying to concatenate those files.
