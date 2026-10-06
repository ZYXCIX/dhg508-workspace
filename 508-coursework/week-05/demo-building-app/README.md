# Demo: which Lingnan building is this?

A minimal app, not a skill: a web page, a small server, a model, and a
database. Drop or paste a photo; the page sends it to the server; the server
asks the model which building it shows, looks that building up in the Week 3
database, and sends the answer back.

```sh
python3 server.py          # then open http://localhost:8000
PORT=8765 python3 server.py   # if 8000 is already in use
```

Python standard library only; nothing to install. The database and archive
photos are read from `../../week-03/demo-buildings/`.

| File | What it does |
|---|---|
| `static/index.html` | the page: drop / paste / click, then the result card (plain HTML + JavaScript) |
| `server.py` | the server: serves the page, receives the photo at `POST /api/identify`, calls `ask_model()`, looks up `buildings.db` |
| `fixtures/model-response.json` | a saved answer that stands in for the model |

## It looks smart. It is a fixture.

`ask_model()` in `server.py` does **not** call any model. It returns
`fixtures/model-response.json` for every photo, and the page shows the badge
"model: fixture". Drop any photo and you get 惺亭.

That is the one spot to replace. A real version sends the image to a model
API and asks for JSON (`building_id`, `confidence`, `reason`); the rest of the
app stays the same.
