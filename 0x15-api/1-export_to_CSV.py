#!/usr/bin/python3
""" a Python script that, using this REST API, for a given employee ID,
returns information about his/her TODO list progress and export the 
data in the CSV format.. """

import csv
import requests
import sys

base_url = "https://jsonplaceholder.typicode.com/"


def do_request():
    """create a request"""
    if len(sys.argv) < 2:
        return print("USAGE:", __file__, "< employee_id >")
    emp_id = sys.argv[1]
    try:
        _emp_id = int(emp_id)
    except ValueError:
        print("Employee ID must be an integer")

    resp = requests.get(base_url + "users/" + emp_id)
    if resp.status_code == 404:
        return print("User Id not found")
    elif resp.status_code != 200:
        return print("Error status code: ", resp.status_code)
    user = resp.json()

    resp = requests.get(base_url + "todos/")
    if resp.status_code != 200:
        return print("Error status code: ", resp.status_code)
    todos = resp.json()

    user_todos = [todo for todo in todos if todo.get("userId") == user.get("id")]
    completed = [todo for todo in user_todos if todo.get("completed")]
    ''' write data to csv file
    Format: "USER_ID","USERNAME","TASK_COMPLETED_STATUS","TASK_TITLE"'''
    with open(emp_id + ".csv", "w", newline="") as csv_file:
        fieldnames = ["userId", "username", "completed", "title"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for line in user_todos:
            writer.writerow(
                {
                    "userId": line.get("userId"),
                    "username": user.get("username"),
                    "completed": line.get("completed"),
                    "title": line.get("title"),
                }
            )


if __name__ == "__main__":
    do_request()
