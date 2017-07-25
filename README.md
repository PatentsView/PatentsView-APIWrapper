PatentsView API Wrapper
===================================

The purpose of this API Wrapper is to extend the functionality of the 
[PatentsView API](patentsview.org/api/). The wrapper can take in a list of 
values (such as patent numbers), retrieve multiple data points, and then convert
and merge the results into a CSV file. 

## How To Use the API Wrapper
1. Clone or download this repository
2. Modify the *"config.cfg"* file to point to your input file(s) and specify 
    your queries.
3. Run the API Wrapper using Python 3


```powershell
git clone https://github.com/CSSIP-AIR/PatentsView-APIWrapper.git
cd PatentsView-APIWrapper
python api_wrapper.py
```

## How to specify a query
The PatentsView API Wrapper reads in query specifications from the configuration
file *"config.cfg"*, in which you may specify where the input list of values to query can be found. 

### Input file(s)
Input files must be text files containing a list of values (such as patent 
numbers), each separated by a new line. The file *"sample_file.txt"* provides an
example of the correct format.

### Configuration File
Specify queries in the *"config.cfg"* file. To do so, modify the required and 
optional parameters to point to the input file and specify the fields and 
criteria applied to the search.

###### Required Parameters:

- __*\[QUERY_NAME\]*__: defines the query that will be made. Multiple queries 
may be specified, as shown in the example configuration file *"config.cfg"*.

- __*entity*__: the type of object that will be returned. Must be one of: 

      ["patents", "inventors", "assignees", "locations", "cpc_subsections", 
      "uspc_mainclasses", "nber_subcategories"]

- __*directory*__: the folder containing the input list of values to query

- __*input_file*__: the filename of the input list of values to query. The input 
file should be a text file with a list of values separated by newlines.

- __*input_type*__: the type of value in the input_file. The full lists of 
input_types can be found in the 
[PatentsView API Documentation](http://www.patentsview.org/api/doc.html). 
Common input types include:

      ["patent_number", "inventor_id", "assignee_id", "cpc_subsection_id", 
      "location_id", "uspc_mainclass_id"]

- __*fields*__: a list of fields to be included in the resulting output

###### Optional Parameters:
Optional parameters can be commented out or deleted if not in use.

- sort: the field over which the output file will be sorted 

- __*criteria1, criteria2, ...*__ : allow for additional criteria to be applied to 
the query. Multiple criteria are combined with AND operators, but a single 
criterion may be written using an OR operator with multiple criteria. For example:

    To limit results to patents from Jan. 1, 2014 to Dec. 31, 2016.

      criteria1 = {"_gte":{"patent_date":"2014-01-01"}
      criteria2 = {"_lte":{"patent_date":"2016-12-31"}

    To limit results to patents before Jan. 1, 2014 OR after Dec. 31, 2016.

      criteria1 = {"_or":[{"_lte":{"patent_date":"2014-01-01"}, {"_gte":{"patent_date":"2016-12-31"}]}

	A full syntax guide for specifying criteria can be found at the 
    [PatentsView Query Language](http://www.patentsview.org/api/query-language.html) page.
	 
###### Example

This example will query the **patents** endpoint for each **patent_number** in 
**"C:/path/to/input_file/sample_file.txt"** for patents from **2015 or earlier**. 
The resulting output will be called **"QUERY1.csv"**, with **"patent_number", 
"patent_title",** and **"patent_date"** sorted by the **patent_number** column.

```cfg
[QUERY1]
entity = "patents"
input_file = "sample_file.txt"
directory = "C:/path/to/input_file"
input_type = "patent_number"
fields = ["patent_number", "patent_title", "patent_date"]
criteria1 = {"_lte":{"patent_date":"2015-12-31"}}
# criteria2 = 
sort = "patent_number"
```