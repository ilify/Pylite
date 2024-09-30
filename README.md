# PyLite

**Pylite** is a lightweight, Python-based database library that leverages the power of Pandas dataframes as its core structure. It allows for efficient data manipulation and querying while maintaining simplicity and ease of use. Designed for small to medium-sized projects.

## Features

- **Lightweight and Simple**: Minimal setup and configuration needed.
- **Pandas-Integrated**: Uses Pandas DataFrames for efficient data storage and manipulation.
- **In-Memory Database**: Stores data in memory for fast access, with options to save/load to disk.
- **Supports Multiple Formats**: Load data from CSV, JSON, Excel, and other formats supported by Pandas.

## Usage
### Create a Database

```python
db = Database()
```

### Create a Table

```python
db.CreateTable("Users").AddColumns(
    name=str,
    age=int,
    email=str
)
```

### Insertion

```python
db.Users.Insert(
    name="John",
    age=50,
    email="test@example.com"
)
```

### Conditional Read
```python
db.Users[db.Users.age > 32]
db.Users[db.Users.age.between(20,30)]
db.Users[(db.Users.age >= 20) & (db.Users.age <= 30)]
# Output : John 50 test@example.com
```
### Deletion
```python
db.Users.Delete(db.Users.age.between(20,30))
```


## Installation ( Comming Soon 😐)

<!-- 
To install **Pylite**, use pip:
```bash
pip install pylite -->