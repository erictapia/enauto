# Simple Query

## A query consists of four sections

1. size: (optional)
    * number of statistics records to retrieve
    * default: 10,000
    * data type: integer

2. query: (required)
    * one or more rules used to select records from the statistics database
    * condition:
      * condition used to filter statistics records with a query having multiple rules
      * AND: record must match all rules
      * OR: record must match at least one rule
    * rules:
      * one or more rules used to collect statistics records
      * rule components:
        * field:
          * the name of the statistics property name
        * type:
          * property value data type
        * value:
          * value to query for
        * operator:
          * the type of operator to perform filtering of statistics records
          * date operator
            * between {date1}, {date2} where date is in yyyy-MM-dd format
            * last_{n}_days where n is the number of days before current date
            * last_{n}_hours where n is the number of hours before current time
            * last_{n}_weeks where n is the number of weeks before the current week
          * numeric operator
            * equal {value}
            * greater {value}
            * in {value1}, ..., {value_n}
            * less {value}
            * less_or_equal {value}
            * not_equal {value}
            * not_in value1, ..., {value_n}
          * string operator
            * equal {value}
            * in {value1}, ..., {value_n}
            * not_equal {value}
            * not_in {value1}, ..., {value_n}

3. sort:
    * to sort on multiple fields by field-order pairs
    * sorts by JSON object sequence
    * data type: array of JSON objects
    * JSON object:
      * field:
        * field name to sort by  
      * order: (optional)
        * sorts the field by the specified order, asc or desc
        * default: sort by data creation time

4. fields:
    * statistics data fields returned
    * default: all fields
    * data type: array of strings

## JSON Structure

```python
{
    "size": integer,

    "query": {
        "condition": "AND | OR",

        "rules": [
            {
                "field": "field-name",

                "type": "data-type",

                "value": [
                    "value"
                ],

                "operator": "operator"
            }
        ]
    },

    "sort": [
        {
            "field": "field-name",

            "order": "(asc | desc)"
        }
    ],

    "fields": [
        "field-name"
    ]
}
```

## Property name and data type

* use the ../fields to get a JSON array of properties, data type, and options

## Example simple query body

* query:
  * Select up to 100 records
  * (last_24_hours) AND (critical in severity_level) AND (security in component)

```python
{
  "size": 100,
    "query": {
        "condition": "AND",
        "rules": [
            {
                "value": ["24"],
                "field": "entry_time",
                "type": "date",
                "operator": "last_n_hours"
            },
            {
                "value": ["critical"],
                "field": "severity_level",
                "type": "string",
                "operator": "in"
            },
            {
                "value": ["security"],
                "field": "component",
                "type": "string",
                "operator": "in"
            }
        ]
    }
}
```
