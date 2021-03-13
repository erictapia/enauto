# Aggregated Query

* retrieves records from the vManage statistics database
* aggregation can get sum, count, average, min, and max from the retrieved records

## A query consists of three sections

1. size: (optional)
    * Not used but if present it must be 0

2. query: (optional)
    * default (no query defined): records for the last 24 hours
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

3. aggregation:
    * field:
      * grouping of one or more property fields, like a SQL Group by statement
      * keys:
        * property: name of property to be included
        * size: number of data instances to include in the aggregation
        * order: sort order, asc or desc
        * sequence: order in which to group the fields
    * metrics:
      * aggregation for properties with numeric values
      * keys:
        * property: name of a numeric property included in the data statistics
        * type: type of metric aggregation operation
          * avg, cardinality, max, min, or sum
        * order: sort order, asc or desc
    * histogram:
      * aggregation for properties with date fields
      * keys:
        * property: name of property to be included
        * type: time period over which aggregated data is selected
          * second, minute, hour, day, month, year, or quarter
        * interval: interval to apply to the date-type
          * default: 1
          * optional
        * order: sort order, asc or desc

## JSON Structure

```python
{
    "size": 0,

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

    "aggregation": {
        "field": [
          {
            "property": "field-name",
            "size": number,
            "order": "(asc | desc)",
            "sequence": number
          }
        ],

        "metrics": [
          {
            "property": "field-name",
            "type": "aggregation-operation",
            "order": "(asc | desc)"
          }

        ],

        "histogram": {

        }
    }
}
```

## Determine field name and data type

* use the ../fields to get a JSON array of properties, data type, and options

## Example aggregation query body

* query:
  * select statistics
    * (last 24 hours) AND
    * (device ID 1.1.12.1) AND
    * (family in standard, encrypted, network management, or network service)
  * aggregate:
    * aggregate in 30 min intervals
    * group by family
    * sum the data octets

```python
{
  "query": {
    "condition": "AND",

    "rules": [
      {
        "value": [
          "24"
        ],
        "field": "entry_time",
        "type": "date",
        "operator": "last_n_hours"
      },
      {
        "value": [
          "1.1.12.1"
        ],
        "field": "vdevice_name",
        "type": "string",
        "operator": "in"
      },
      {
        "value": [
          "Standard",
          "Encrypted",
          "Network Management",
          "Network Service"
        ],
        "field": "family",
        "type": "string",
        "operator": "in"
      }
    ]
  },

  "aggregation": {
    "field": [
      {
        "property": "family",
        "sequence": 1,
        "size": 4
      }
    ],

    "metrics": [
      {
        "property": "octets",
        "type": "sum"
      }
    ],

    "histogram": {
      "property": "entry_time",
      "type": "minute",
      "interval": 30,
      "order": "asc"
    }
  }
}
```
