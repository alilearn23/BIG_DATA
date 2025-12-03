# TP08: Simulating MapReduce Jobs on Google Colab
## Ali Lakhoues
## Results Summary

### 1. Count Requests per Status Code
```
HTTP 200: 10 requests
HTTP 403: 2 requests
HTTP 404: 5 requests
HTTP 500: 3 requests
```

### 2. Count Requests per URL
```
/about.html: 2 requests
/checkout: 3 requests
/contact.html: 3 requests
/images/logo.png: 2 requests
/index.html: 5 requests
/login: 2 requests
/products.html: 3 requests
```

### 3. Total Response Size per Status
```
HTTP 200: 8182 bytes
HTTP 403: 128 bytes
HTTP 404: 2560 bytes
HTTP 500: 384 bytes
```

### 4. Error Requests Only (exclude 200)
```
HTTP 403: 2 requests
HTTP 404: 5 requests
HTTP 500: 3 requests
```

---

## Implemented Functions

### Mapper
```python
def mapper(line):
    fields = line.strip().split(',')
    if len(fields) != 7 or fields[0].startswith('#'):
        return []
    status = fields[5]
    return [(status, 1)]
```

### Shuffle
```python
from collections import defaultdict

def shuffle(mapped_data):
    grouped = defaultdict(list)
    for key, value in mapped_data:
        grouped[key].append(value)
    return grouped
```

### Reducer
```python
from collections import defaultdict

def reducer(mapped_data):
    grouped = defaultdict(int)
    for key, value in mapped_data:
        grouped[key] += value
    return grouped
```

### Combine
```python
mapped = []
with open("weblogs.txt", "r") as f:
    for line in f:
        mapped.extend(mapper(line))

reduced = reducer(mapped)

for code, count in sorted(reduced.items()):
    print(f"HTTP {code}: {count} requests")
```
