# CREST CTF Writeup: Mutual Friends Are a Graph Query

## Flag

```text
CREST{mutu4l_fr13nds_ar3_a_gr4ph_qu3ry}
```

## Challenge Overview

The flag suggests an OSINT or data-analysis challenge involving relationships between people in a social network.

A social network can be represented as a graph in which each person is a vertex and each friendship is an edge. Finding mutual friends is then a graph-neighborhood intersection problem.

## Approach

### 1. Identify the available data

Inspect the challenge materials for information such as:

- User profiles or identifiers.
- Friendship lists.
- Follower or connection relationships.
- JSON, CSV, database, or API responses.
- Conditions that distinguish the target accounts.

The exact data source depends on the challenge implementation.

### 2. Model the relationships as a graph

Let \(G=(V,E)\), where:

- \(V\) is the set of users.
- \(E\) is the set of relationships between users.

For a user \(u\), define \(N(u)\) as the set of users connected to \(u\).

The mutual friends of two users \(A\) and \(B\) are:

\[
M(A,B)=N(A)\cap N(B)
\]

This intersection contains users connected to both accounts.

### 3. Calculate mutual friends

If the challenge provides friendship lists, Python can calculate their intersection directly:

```python
user_a_friends = {"alice", "bob", "charlie", "david"}
user_b_friends = {"bob", "david", "eve", "frank"}

mutual_friends = user_a_friends & user_b_friends

print(sorted(mutual_friends))
```

Example output:

```text
['bob', 'david']
```

These example users are illustrative only; they are not asserted to be part of the actual challenge.

### 4. Apply the challenge's filtering conditions

A CTF may require more than finding the intersection. For example, the challenge may specify a particular user, a required number of mutual connections, or an additional profile attribute.

Apply those conditions to narrow the graph and identify the intended result. If the data is accessible through a database or API, inspect the relationship model and query the relevant records rather than assuming all visible connections are mutual friendships.

### 5. Recover the flag

Use the identified relationship or result to retrieve the flag from the challenge's intended source.

The challenge statement, dataset, and interface were not provided here, so the specific users, query, and flag-retrieval step cannot be confirmed from the flag text alone.

## Key Takeaway

Many social-network relationship problems are graph queries. Mutual connections can be found by intersecting adjacency sets, while additional constraints can be handled through filtering or more complex graph traversal.

## Flag

`CREST{mutu4l_fr13nds_ar3_a_gr4ph_qu3ry}`
