"""
Data for testing the API requests.
"""

patch_object_by_id_params = [
    ("GENERATE_NEW_ID", "FAKE_DATA", "Patched User", 200),
    ("GENERATE_NEW_ID", "FAKE_DATA", "", 200),
    ("GENERATE_NEW_ID", {}, "Patched User", 200),
    ("GENERATE_NEW_ID", {}, "", 400),
    ("GENERATE_NEW_ID", [], "Patched User", 200),
    ("GENERATE_NEW_ID", "FAKE_DATA", [], 200),
    ("GENERATE_NEW_ID", [], [], 400),
    ("NON_EXISTING_ID", "FAKE_DATA", "User", 404),
]

get_object_by_id_params = [
    ("GENERATE_NEW_ID", 200),
    ("NON_EXISTING_ID", 404),
]

post_object_params = [
    ({}, "", 200),
    ({}, "User", 200),
    ("FAKE_DATA", "", 200),
    ("FAKE_DATA", "User", 200),
    ([], "User", 400),
    ("FAKE_DATA", [], 400),
    ([], [], 400),
]

put_object_by_id_params = [
    ("GENERATE_NEW_ID", {}, "", 200),
    ("GENERATE_NEW_ID", {}, "User", 200),
    ("GENERATE_NEW_ID", "FAKE_DATA", "", 200),
    ("GENERATE_NEW_ID", "FAKE_DATA", "User", 200),
    ("NON_EXISTING_ID", "FAKE_DATA", "User", 404),
    ("GENERATE_NEW_ID", [], "User", 400),
    ("GENERATE_NEW_ID", "FAKE_DATA", [], 400),
    ("GENERATE_NEW_ID", [], [], 400),
]
