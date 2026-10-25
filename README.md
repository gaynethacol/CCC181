# LicenseQ

LicenseQ is a student queue-management prototype for LTO Tubod, Iligan City. It is being developed to help applicants join and track two queues: application and testing, and printed-card collection. Front-desk employees will manage tickets through a staff dashboard. The current version displays sample tickets for both queues.

## Run locally

Create a virtual environment:

```bat
python -m venv .venv
```

Install dependencies:

```bat
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start Flask:

```bat
.venv\Scripts\python.exe -m flask --app app run --debug
```

Open http://127.0.0.1:5000 in your browser.

## Current limitations

Tickets use fictional sample data stored in a Python list. This prototype is not connected to official LTO systems.

## Staff access

The staff dashboard is open without login for this classroom prototype.
It is intended for local testing with fictional data. Staff authentication
will be added in a later course activity.

Staff can filter queues, call applicants, mark tickets as served or no-show,
move an absent applicant to the end, and transfer eligible applicants to
printed-card collection.

No-show removes a ticket from the active list. Use “Absent — move to end”
when the applicant should remain in the queue.