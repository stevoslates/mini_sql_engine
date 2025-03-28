# Mini SQL Engine

A **mini SQL engine** built with **B-tree indexes** and a **SQL parser powered by Lark**.  
Currently supports basic `SELECT`, `FROM`, and `WHERE` queries.

---

## Motivation

While reading *Designing Data-Intensive Applications*, I realized how much I’d taken database internals for granted. So wanted to try implement something to help my understanding. Was going to dive straight into a distributed systems project, but probably beneficial to start from the start.

---

## What It Does

- Parses SQL queries using a grammar written with Lark
- Supports `SELECT * FROM table WHERE column = value`-style queries
- Uses a B-tree for indexing one column (e.g., `email`) to speed up lookups
- Loads data from a JSON file and simulates a basic table structure

---

## Planned Improvements

- Add binary search within B-tree nodes (currently uses linear scan inside nodes)
- Support multiple indexes on different columns  
    - Let the user define indexes at table load time  
    - Choose the best index dynamically based on the query
- Add support for `INSERT` statements to update the table at runtime
