PatentsView API Wrapper
===================================

The purpose of this API Wrapper is to extend the functionality of the 
[PatentsView API](patentsview.org/api/). The wrapper can take in a query, retrieve multiple data points, and then convert
and merge the results into a CSV file. 

## How To Use the API Wrapper
1. Clone or download this repository
```bash
git clone https://github.com/CSSIP-AIR/PatentsView-APIWrapper.git
```

2. Install dependencies
```bash
cd PatentsView-APIWrapper
pip install -r requirements.txt
```

3. Modify the sample config file `sample_config.cfg`

4. Run the API Wrapper using Python 3: (via the CLI as seen below or via `generate_dataset.bat`)
```bash
python api_wrapper.py sample_config.cfg
```

## How to modify your query configuration file
Below is a description of each parameter that defines each query.

### Query Name
The name of the query, and the name given to the resulting file (for example, [QUERY1] produces QUERY1.csv). If your configuration file contains multiple queries, each query should have a distinct name. Query parameters must directly follow the query name. 

### Entity
The type of object you want to return. This must be one of the PatentsView API endpoints:
```
    "patents"
    "inventors"
    "assignees"
    "locations"
    "cpc_subsections"
    "uspc_mainclasses"
    "nber_subcategories"
```

### Directory
The absolute path of the directory of your input file and results. Use forward slashes (`/`) instead of backward slashes (`\`). For Windows, this may look like:

```directory = "/Users/jsennett/Code/PatentsView-APIWrapper"```

For OSX/Unix systems:

```directory = "C:/Users/jsennett/Code/PatentsView-APIWrapper"```

### Fields
The fields that will be returned in the results. Valid fields for each endpoint can be found in the [PatentsView API Documentation](https://api.patentsview.org/doc.html). Fields should be specified as an array of strings, such as:

```fields = ["patent_number", "patent_title", "patent_date"]```


### Criteria
Rules, written in the PatentsView API syntax, to be applied to each query. Each criteria can specify multiple rules combined with OR or AND operators. If multiple criteria are listed, they will be combined with the AND operator. Multiple criteria should be named criteria1, criteria2, criteria3, etc.

For example, the following criteria will limit results to patents from Jan 1 to Dec 31, 2015 with a patent abstract containing either "cell" or "mobile".
```
criteria1 = {"_gte":{"patent_date":"2015-1-1"}}
criteria2 = {"_lte":{"patent_date":"2015-12-31"}}
criteria3 = {"_or":[{"_contains":{"patent_abstract":"cell"}, {"_contains":{"patent_abstract":"mobile"}]}
```

### Sort (optional)
The fields and directions over which the output file will be sorted. This should be specified as an array of JSON objects, pairing the field with its direction. The sort order will follow the array order.
To sort just by patent number (ascending):

```sort = [{"patent_number": "asc"}]```

To sort first by patent_date (descending), and then by patent title (ascending):

```sort = [{"patent_date": "desc"}, {"patent_title":, "asc"}]```

## Large Queries
Some queries may be too large for the API to return all at once. In these cases, the query should be broken up into multiple sub-queries. The `merge_datasets.py` script will combine all csv files in the current working directory into one large dataset to assist in these scenarios.

## Compatibility

The API wrapper is currently compatible with Python 3.

## License

Users are free to use, share, or adapt the material for any purpose, subject to the standards of the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

Attribution should be given to PatentsView for use, distribution, or derivative works.

## See also

[USPTO PatentsView](https://www.patentsview.org/web/#viz/relationships)

[PatentsView API](https://api.patentsview.org/doc.html)

[PatentsView Query Language](https://api.patentsview.org/query-language.html)
