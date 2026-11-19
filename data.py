"""The Happy Tails Adoption Center's adoption applications. Ready to use: you don't need to change this file.

Each application holds what the applicant sent (name, email, age, pet_name, pet_type, has_yard), and two fields the
center adds: its status, and the staff's private staff_notes, which must never be sent to anyone who asks for an
application. The routes read and change the APPLICATIONS list. Keep it the same list: add to it with
APPLICATIONS.append().
"""
import copy

STARTING_APPLICATIONS = [
    {"id": 1, "name": "Maya", "email": "maya@example.com", "age": 34, "pet_name": "Biscuit", "pet_type": "dog",
     "has_yard": True, "status": "approved", "staff_notes": "Met Biscuit twice. Great with big dogs."},
    {"id": 2, "name": "Theo", "email": "theo@example.com", "age": 27, "pet_name": "Pepper", "pet_type": "cat",
     "has_yard": False, "status": "received", "staff_notes": "Third-floor apartment. Check the lease allows cats."},
    {"id": 3, "name": "Rosa", "email": "rosa@example.com", "age": 61, "pet_name": "Clover", "pet_type": "rabbit",
     "has_yard": True, "status": "visit booked", "staff_notes": "Has kept rabbits before. Call her vet."},
]

APPLICATIONS = copy.deepcopy(STARTING_APPLICATIONS)


def reset_applications():
    """Puts the applications back to the three above. The tests call it before each test, so every test starts the same."""
    APPLICATIONS.clear()
    APPLICATIONS.extend(copy.deepcopy(STARTING_APPLICATIONS))
