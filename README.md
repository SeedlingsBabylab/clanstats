# clanstats

wiki documentation [here](http://wiki.bcs.rochester.edu/Seedlings/Clanstats)

## usage

### clanstats.py

This script will output the long form speaker/classifier data when given a single .cex clan file. It takes 3 arguments.
The .cex file (first argument) can also be replaced by the .csv output produced by parse_clan.
If the input is a parse_clan csv file, the window size will be 0.

``` bash
$: python clanstats.py  /path/to/clanfile.cex   /path/to/output   window_size
```

### cs_folder.py

This script will run clanstats.py on every clan file (or parse_clan .csv) in a directory passed as argument.

``` bash
$: python cs_folder.py  /path/to/clanfiles/   /output/path/   window_size
```

If there are parse_clan csv files in the folder being batch processed, the window_size will automaticaly be set as 0.
This means the clan files will be processed with the window, while the csv's will not.
If you need window size consistency across all the outputs, use a window_size of 0, or leave the csv files
out of the folder being batch processed.

This script also produces a single .csv file containing the aggregate data from all the files it just processed (named aggregate_long.csv). It'll combine all the .csv's in the output directory (that was originally passed as an argument), so if you have .csv files in there that weren't a result of what cs_folder.py just did, it'll combine those as a part of the aggregate_long.csv output as well. Make sure there's only .csv files in the output directory or else the script will throw an error when trying to concatenate those files.
