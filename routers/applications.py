"""The Happy Tails Adoption Center's applications router: for you to finish.

ApplicationIn, the body of POST /applications, and its rules:
  name       text of 1 to 80 characters                 email      a valid email address
  age        a whole number, 18 or over                 pet_name   text of 1 to 40 characters
  pet_type   "dog", "cat" or "rabbit", exactly          has_yard   true or false; false when it isn't sent

ApplicationOut, every answer: id, name, email, age, pet_name, pet_type, has_yard and status. Never staff_notes.

Every request it should answer, with its status code and body:

  POST /applications                   201, the new application as an ApplicationOut, kept in APPLICATIONS. For the body
                                       {"name": "Sam", "email": "sam@example.com", "age": 29, "pet_name": "Juniper",
                                        "pet_type": "cat", "has_yard": false}
                                       the answer is {"id": 4, "name": "Sam", "email": "sam@example.com", "age": 29,
                                       "pet_name": "Juniper", "pet_type": "cat", "has_yard": false, "status": "received"}:
                                       its id is one more than the number of applications, its status is always
                                       "received", and it's kept with "staff_notes": "" (empty)
  POST /applications, a broken rule    422, FastAPI's own answer, with an entry whose loc names the field, such as
                                       ["body", "age"] for an age of 17
  POST /applications, with "status"    201, as above: the body can't set status or staff_notes, so the status is
  or "staff_notes" in the body         "received" and the notes are kept empty
  GET /applications/1                  200, application 1 as an ApplicationOut, with no staff_notes
  GET /applications/99                 404, {"detail": "There's no application 99."}
  GET /applications/abc                422, FastAPI's own answer: an application's id is a whole number

The docs page shows ApplicationIn as the body of POST /applications, and ApplicationOut as the answer of both routes.
"""
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field

from data import APPLICATIONS

router = APIRouter(prefix="/applications", tags=["applications"])

# Write the two models, ApplicationIn and ApplicationOut, here. Then add the two routes below them.
