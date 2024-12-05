from flask import send_from_directory
from server.agent import Agent
from dotenv import load_dotenv
import os
import re


def get_all_reimage_tickets():
    """
    Returns a list of all the tickets that have the tag "Reimage".
    """
    output = []
    # Set up the requester
    load_dotenv()
    key = os.getenv("API_KEY")
    url = os.getenv("HELPDESK_URL")
    requester = Agent(key, url)
    output_raw = requester.filteredTicketGetRequest("tag:Reimage%20AND%20status:<4")
    for ticket in output_raw:
        curr_ticket = {}
        curr_ticket["title"] = f"#{ticket['id']} - {format_title(ticket['subject'])}"
        curr_ticket["agent"] = requester.getUser(ticket["responder_id"])
        curr_ticket["created_at"] = format_date(ticket["created_at"])
        curr_ticket["tasks"] = get_tasks(ticket["id"], requester)
        output.append(curr_ticket)
    return output


def ticket_get(ticket_id: int):
    """
    Uses the Agent class to get the ticket with the specified ID.
    """
    load_dotenv()
    key = os.getenv("API_KEY")
    url = os.getenv("HELPDESK_URL")
    requester = Agent(key, url)
    return reimage_ticket(ticket_id, requester)


def reimage_ticket(ticket_id: int, requester: Agent):
    """
    Uses the Agent class to get the ticket with the specified ID and format it.
    """
    ticket_raw = requester.ticketGetRequest(ticket_id)
    output = {}
    if "error" in ticket_raw:
        output["error"] = ticket_raw["error"]
    else:
        output["title"] = format_title(ticket_raw["ticket"]["subject"])
        output["agent"] = requester.getUser(ticket_raw["ticket"]["responder_id"])
        output["created_at"] = format_date(ticket_raw["ticket"]["created_at"])
        output["tasks"] = get_tasks(ticket_id, requester)
    return output


def format_title(title: str):
    """
    Formats the title from the helpdesk API to remove the ticket number.
    """
    return title.split(" - ")[1]

def format_date(date: str):
    """
    Formats the date from the helpdesk API to the format MM/DD/YYYY.
    """
    output = date.split("T")[0].split("-")
    return f"{output[1]}/{output[2]}/{output[0]}"


def get_tasks(ticket_id: int, requester: Agent):
    """
    Use the requester to get the tasks for the ticket with the specified ID.
    This function returns a list of the tasks for the ticket.
    """
    tasks_raw = requester.tasksGetRequest(ticket_id)
    tasks = []
    for task in tasks_raw:
        task = clean_string(task)
        if task.strip() != '':
            tasks.append(task.strip())
    return tasks

def clean_string(s):
    # Remove HTML tags
    s = re.sub(r'<.*?>', '', s)
    # Remove \n and \u00a0 characters
    s = s.replace('\n', '').replace('\u00a0', '')
    return s
