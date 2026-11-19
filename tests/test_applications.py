# Tests for the applications router. Run them with: pytest (in the exercise folder, with the virtual environment active).
# Each test sends one request to the app, the request in its name, and checks the status code and the body that come
# back. TestClient hands each request straight to the app, so no server needs to be running. A failing test says what
# it sent, what it expected and what came back.
# You don't need to change this file. The chapter Testing an API, two chapters on, shows how tests like these are written.
import pytest
from fastapi.testclient import TestClient

from data import APPLICATIONS, STARTING_APPLICATIONS, reset_applications
from main import app

client = TestClient(app)

SAM = {"name": "Sam", "email": "sam@example.com", "age": 29, "pet_name": "Juniper", "pet_type": "cat", "has_yard": False}
SAM_OUT = {"id": 4, "name": "Sam", "email": "sam@example.com", "age": 29, "pet_name": "Juniper", "pet_type": "cat",
           "has_yard": False, "status": "received"}


@pytest.fixture(autouse=True)
def fresh_applications():
    """Puts the applications back to the three in data.py before every test, so one test's application isn't there in the next."""
    reset_applications()


def check_status(request, response, status):
    """Fails with a message that says what the request answered, when its status code isn't the one expected."""
    assert response.status_code == status, (
        f"{request} should answer {status}, but it answered {response.status_code} with {response.text}"
    )


def check_body(request, response, body):
    """Fails with a message that says what came back, when the body isn't the one expected."""
    assert response.json() == body, f"{request} should answer {body!r}, but it answered {response.json()!r}."


def check_problem_at(request, response, field):
    """Checks a 422 from FastAPI whose detail has an entry at ["body", field], so the rule is in ApplicationIn."""
    check_status(request, response, 422)
    detail = response.json().get("detail")
    places = [entry.get("loc") for entry in detail] if isinstance(detail, list) else []
    assert ["body", field] in places, (
        f"{request} should answer 422 with a problem at ['body', '{field}'], from a rule in ApplicationIn, "
        f"but its detail is {detail!r}."
    )


def post_sam(**changes):
    """Sends Sam's application, with any field changed, and gives back the answer."""
    return client.post("/applications", json={**SAM, **changes})


def test_1_post_sam_answers_201_with_id_4_status_received_and_no_staff_notes():
    response = post_sam()
    check_status("POST /applications with Sam's application", response, 201)
    check_body("POST /applications with Sam's application", response, SAM_OUT)


def test_2_post_sam_then_get_applications_4_finds_it():
    post_sam()
    response = client.get("/applications/4")
    check_status("GET /applications/4, after POST /applications with Sam's application,", response, 200)
    check_body("GET /applications/4, after POST /applications with Sam's application,", response, SAM_OUT)


def test_3_post_sam_keeps_it_with_empty_staff_notes():
    post_sam()
    assert len(APPLICATIONS) == 4, (
        f"After POST /applications, APPLICATIONS should hold 4 applications, but it holds {len(APPLICATIONS)}."
    )
    assert APPLICATIONS[3] == {**SAM_OUT, "staff_notes": ""}, (
        f"Sam's application should be kept as {({**SAM_OUT, 'staff_notes': ''})!r}, but it's {APPLICATIONS[3]!r}."
    )


def test_4_post_without_has_yard_answers_201_with_has_yard_false():
    body = {key: value for key, value in SAM.items() if key != "has_yard"}
    response = client.post("/applications", json=body)
    check_status("POST /applications with no has_yard", response, 201)
    check_body("POST /applications with no has_yard", response, SAM_OUT)


def test_5_post_with_status_approved_and_staff_notes_answers_status_received():
    response = post_sam(status="approved", staff_notes="Approve at once!")
    request = "POST /applications with \"status\": \"approved\" and \"staff_notes\" in the body"
    check_status(request, response, 201)
    check_body(request, response, SAM_OUT)
    assert APPLICATIONS[3].get("staff_notes") == "", (
        f"The body can't set staff_notes: it should be kept as \"\", but it's {APPLICATIONS[3].get('staff_notes')!r}."
    )


def test_6_post_an_empty_name_answers_422_at_name():
    check_problem_at("POST /applications with \"name\": \"\"", post_sam(name=""), "name")


def test_7_post_an_81_character_name_answers_422_at_name():
    check_problem_at("POST /applications with a name of 81 characters", post_sam(name="S" * 81), "name")


def test_8_post_an_80_character_name_answers_201():
    check_status("POST /applications with a name of 80 characters", post_sam(name="S" * 80), 201)


def test_9_post_age_17_answers_422_at_age():
    check_problem_at("POST /applications with \"age\": 17", post_sam(age=17), "age")


def test_10_post_age_18_answers_201():
    check_status("POST /applications with \"age\": 18", post_sam(age=18), 201)


def test_11_post_pet_type_hamster_answers_422_at_pet_type():
    check_problem_at("POST /applications with \"pet_type\": \"hamster\"", post_sam(pet_type="hamster"), "pet_type")


def test_12_post_an_email_with_no_at_sign_answers_422_at_email():
    request = "POST /applications with \"email\": \"sam.example.com\""
    check_problem_at(request, post_sam(email="sam.example.com"), "email")


def test_13_post_an_empty_pet_name_answers_422_at_pet_name():
    check_problem_at("POST /applications with \"pet_name\": \"\"", post_sam(pet_name=""), "pet_name")


def test_14_get_applications_1_answers_200_with_no_staff_notes():
    response = client.get("/applications/1")
    check_status("GET /applications/1", response, 200)
    maya = {key: value for key, value in STARTING_APPLICATIONS[0].items() if key != "staff_notes"}
    check_body("GET /applications/1", response, maya)


def test_15_get_applications_99_answers_404_theres_no_application_99():
    response = client.get("/applications/99")
    check_status("GET /applications/99", response, 404)
    check_body("GET /applications/99", response, {"detail": "There's no application 99."})


def test_16_get_applications_abc_answers_422():
    check_status("GET /applications/abc", client.get("/applications/abc"), 422)


def test_17_the_docs_page_shows_applicationin_and_applicationout():
    paths = client.get("/openapi.json").json()["paths"]
    post = paths.get("/applications", {}).get("post")
    get = paths.get("/applications/{application_id}", {}).get("get")
    assert post is not None and get is not None, (
        "The docs page should list POST /applications and GET /applications/{application_id}, but it lists: "
        + (", ".join(paths) or "no routes") + "."
    )
    body = post.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {}).get("$ref", "")
    assert body.endswith("/ApplicationIn"), (
        f"The body of POST /applications should be ApplicationIn, but the docs page shows {body or 'no model'}."
    )
    for name, route, status in (("POST /applications", post, "201"), ("GET /applications/{application_id}", get, "200")):
        answer = route.get("responses", {}).get(status, {}).get("content", {}).get("application/json", {})
        ref = answer.get("schema", {}).get("$ref", "")
        assert ref.endswith("/ApplicationOut"), (
            f"The answer of {name} should be ApplicationOut, but the docs page shows {ref or 'no model'}: "
            "give the route a return type, or response_model=."
        )
