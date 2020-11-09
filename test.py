import firebird

client = firebird.Client(
    'S0gFm6gDo9o6GId-5xJfC8-3oPUHaHe-Mn-FKyq53eYn3Hh75N4q6i1a80Jwo9nl7pvQSJx9M51H4tRD39M_R9Nl0gdtw-FCvi6y0bSGZXKBG3nw65DZZ-oNAgPu9-X6wkT-3KpR3nyNhcXvtzTOa01daUHYZ12iJdvMuEQxF1o',
    api_base_url='http://api.firebird.local'
)

# Many
all_numbers = firebird.resources.Number.all(client)

# One
number = firebird.resources.Number.one(client, '441885483068')

# Many
number_page = firebird.resources.Number.many(client)

# Get node
node = number.node

# Set node
number.node = {"node_type": "forward", "edges": {}, "messages": [], "whisper": "", "number": "+441234111111"}

number.node = firebird.nodes.ForwardNode('+441234222223')
