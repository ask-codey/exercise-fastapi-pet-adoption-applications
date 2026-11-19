# Exercise: Pet Adoption Applications

Exercise code for the lesson **Exercise: Pet Adoption Applications** in the Python Web APIs course on [ask-codey.com](https://www.ask-codey.com).

The Happy Tails Adoption Center takes adoption applications through its website, and its API takes whatever it's sent: an empty name, an applicant of 12, a pet the center doesn't have. Worse, when an applicant looks up their application, the API sends back the staff's private notes too. You'll finish the center's FastAPI app with two Pydantic models: one with the rules every application must follow, and one that chooses what goes back out. Tests send good and bad applications to the app and check what comes back.

## What's here

- `routers/applications.py`: the applications router, for you to finish. The comment at its top lists the rules for an application, the fields every answer has, and every request the router should answer, with the status code and the body. For now it has no routes, so every request answers 404.
- `routers/__init__.py`: makes the `routers` folder a package, so `main.py` can bring in `routers/applications.py`. Ready to use.
- `main.py`: makes the app, `app = FastAPI(title="Happy Tails")`, and adds the applications router with `app.include_router`. Ready to use.
- `data.py`: the center's three applications, in the list `APPLICATIONS`, and `reset_applications()`, which the tests use to put the applications back before each test. Each application has a `status` and private `staff_notes`. Ready to use.
- `tests/test_applications.py`: tests that send requests to your app and check each answer. You don't need to change this file.
- `requirements.txt`: the packages the app and the tests need (FastAPI and what it runs on, and pytest), at exact versions. Ready to use.
- `pytest.ini`: tells pytest where the tests are and where to find `main.py`. Ready to use.
- `.gitignore`: tells Git to leave out the virtual environment and the files Python and pytest make as they run. Ready to use.

## Before you start

The app and the tests need FastAPI and pytest, and they go in a virtual environment: a private set of packages for this folder only. In VS Code's terminal, in this folder, run these three commands.

On Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On a Mac (zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- The first command makes the virtual environment, in a folder named `.venv`.
- The second turns it on for this terminal: the prompt starts with `(.venv)` from then on.
- The third installs the packages `requirements.txt` lists into it. It takes a minute: FastAPI brings several packages with it, among them Pydantic and `email-validator`, which `EmailStr` needs.

*Virtual Environments and pip* explains all three. The `.venv` folder is in `.gitignore`, so Git leaves it out: these commands make it again on any computer.

If PowerShell answers that running scripts is disabled on this system, run this once, then run the second command again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Each new terminal starts with the virtual environment off. If the prompt doesn't start with `(.venv)`, run the second command again. (VS Code often turns it on for you.)

## Run it

```bash
fastapi dev main.py
```

Then open `http://127.0.0.1:8000/docs` in your browser. The docs page lists every route the app has: none yet, until you add them. Click a route, then **Try it out** and **Execute**, to send it a real request. Scroll to **Schemas** at the bottom to see your two models. The app restarts each time you save a file. Stop it with **Ctrl+C**.

## Check your work

```bash
pytest
```

No server needs to be running: the tests hand each request straight to the app. At first every test fails: that is expected, because the router has no routes yet, so every request answers 404. Each piece you finish turns its tests green. A failing test's message says what it sent, what it expected and what came back, for example *POST /applications with "age": 17 should answer 422, but it answered 404 with {"detail":"Not Found"}*

## The rules

- Write the two models and the two routes in `routers/applications.py`, on its `router`, which already has the prefix `/applications` and the tag `applications`. Don't change `main.py`, `data.py` or the tests.
- `ApplicationIn` is the body of `POST /applications`. Its six fields and their rules:
  - `name`: text of 1 to 80 characters;
  - `email`: a valid email address;
  - `age`: a whole number, 18 or over;
  - `pet_name`: text of 1 to 40 characters;
  - `pet_type`: exactly `"dog"`, `"cat"` or `"rabbit"`;
  - `has_yard`: true or false, and false when the body doesn't send it.
- Every rule lives in `ApplicationIn`, so FastAPI answers 422 for a broken rule before your route runs. Don't check the fields by hand.
- `ApplicationOut` is every answer: `id`, `name`, `email`, `age`, `pet_name`, `pet_type`, `has_yard` and `status`. It never has `staff_notes`.
- A new application's id is one more than the number of applications, its status is `"received"`, and it's kept in `APPLICATIONS` with `"staff_notes": ""`. The body can't set the status or the notes.
- `GET /applications/{application_id}` answers 404 with `{"detail": "There's no application 99."}` (with the id asked for) when there's no such application.

## Tips

- Start with `ApplicationIn`: `Field(min_length=..., max_length=...)` for text, `Field(ge=...)` for a number, `Literal[...]` for the pet types and `EmailStr` for the email. A default of `False` makes `has_yard` optional.
- `ApplicationOut` is a plain model with eight fields and no rules.
- The route's body is an `ApplicationIn`. Build the dictionary to keep with `model_dump()`, adding the id, the status and the empty notes.
- `response_model=ApplicationOut` on a route's decorator leaves out every key the model doesn't name, `staff_notes` included.
- Under the prefix, the path of `POST /applications` is the empty string `""`, and one application's is `"/{application_id}"`. A path of `"/"` puts the route at `/applications/`, with a slash.

## Hand it in

When it works, push your solution to a public repo of your own on GitHub, then paste that repo's address into **Submit your exercise** on the lesson page at [ask-codey.com](https://www.ask-codey.com). That's what completes the lesson. The lesson page shows the Git commands, step by step.
