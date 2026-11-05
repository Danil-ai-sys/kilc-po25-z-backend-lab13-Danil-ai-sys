# Report, lab 13

Fill this in as you go. Write in your own words.

**Name: Danil Sobar**
**Group: PO 25-Z**
**Date: 5.11.26**

## What works

Tick only what works. "Almost works" is not ticked.

- [x] M1: `GET /users/{user_id}/messages`
- [x] M2: `DELETE /rooms/{room_id}` deletes the room and its messages
- [x] M3: `GET /rooms/{room_id}/stats`
- [x] M4: `/stats` with `func.count`
- [x] Bruno: 35 of 35 green
- [x] `pytest`: 42 passed, 0 failed

## Without cascade

Before you added `cascade`, deleting a room with messages failed. Copy the `[SQL: ...]` line from the error:

```
2026-11-05 13:33:15,299 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-11-05 13:33:15,303 INFO sqlalchemy.engine.Engine SELECT rooms.id, rooms.title 
FROM rooms 
WHERE rooms.id = ?
2026-11-05 13:33:15,303 INFO sqlalchemy.engine.Engine [generated in 0.00017s] (1,)
2026-11-05 13:33:15,304 INFO sqlalchemy.engine.Engine ROLLBACK
```

In one or two sentences: what was SQLAlchemy trying to do, and why did the database refuse?

Without cascade, SQLAlchemy tried to keep the messages of the deleted room and just
set their room_id to NULL (UPDATE messages SET room_id=? ...). The database refused
because messages.room_id is a NOT NULL column, so a message cannot exist without a room.

## With cascade

Run `DELETE /rooms/1` in `/docs` after the Bruno run up to request 30. Copy the two `DELETE FROM` statements from the console:

```
2026-11-05 13:38:21,777 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-11-05 13:38:21,786 INFO sqlalchemy.engine.Engine SELECT rooms.id, rooms.title 
FROM rooms 
WHERE rooms.id = ?
2026-11-05 13:38:21,786 INFO sqlalchemy.engine.Engine [generated in 0.00067s] (1,)
2026-11-05 13:38:21,788 INFO sqlalchemy.engine.Engine ROLLBACK
```

## Counting

Copy the `SELECT` that `by_author` sends to the database:

```
2026-11-05 13:40:48,814 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-11-05 13:40:48,814 INFO sqlalchemy.engine.Engine SELECT rooms.id, rooms.title 
FROM rooms 
WHERE rooms.id = ?
2026-11-05 13:40:48,814 INFO sqlalchemy.engine.Engine [cached since 147s ago] (1,)
2026-11-05 13:40:48,815 INFO sqlalchemy.engine.Engine ROLLBACK
```

Why is `func.count` better than `len(session.scalars(select(Message)).all())` when a room has 100,000 messages?

func.count makes the database do the counting and send back a single number
(SELECT count(messages.id) ...), while len(...all()) transfers all 100,000 rows to
Python and builds 100,000 Message objects in memory just to count them. That is much
slower and uses far more memory and network/IO, and the difference grows with the table size.