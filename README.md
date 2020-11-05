# Firebird Python Library

The Firebird Python library provides a pythonic interface to the Firebird API.


## Installation

```
pip install firebird
```

## Requirements

- Python 3.7+


# Usage

```Python

import firebird


client = firebird.Client('your_api_key...')

# Fetch a number
number = firebird.resource.Number.one(client, '...')

```
