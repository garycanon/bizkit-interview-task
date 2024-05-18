from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!

    search_id = args.get("id")
    search_name = args.get("name", "").lower()
    search_age = args.get("age")
    search_occupation = args.get("occupation", "").lower()

    matched_users = []
    added_user_ids = set()

    def add_user(user, priority_list):
        if user["id"] not in added_user_ids:
            priority_list.append(user)
            added_user_ids.add(user["id"])

    if search_id:
        for user in USERS:
            if user["id"] == search_id:
                add_user(user, matched_users)
                break

    matched_by_name = []
    matched_by_age = []
    matched_by_occupation = []

    for user in USERS:
        if user["id"] in added_user_ids:
            continue
        if search_name and search_name in user["name"].lower():
            add_user(user, matched_by_name)
        elif search_age and user["age"] in range(int(search_age) - 1, int(search_age) + 2):
            add_user(user, matched_by_age)
        elif search_occupation and search_occupation in user["occupation"].lower():
            add_user(user, matched_by_occupation)

    matched_users.extend(matched_by_name)
    matched_users.extend(matched_by_age)
    matched_users.extend(matched_by_occupation)

    return matched_users

