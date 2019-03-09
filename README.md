# api_ripper

api_ripper is a regex powered source sniffer that hopes to find strings that look similar to api endpoints.
This is accomplished by matching strings in source code to various url schemas and common api keywords.

# Usage
python3 get_api_routes.py path [--keywords path_to_keywords]

A keywords file should be of this format:
```
regular_expression, weight

dev, 10
api, 10
[/]v[1,2,3], 5
...
```

provided is a basic keywords.txt file

# Output
output is produced as an out.txt
