# LicenseQ — Week 4 Validation

## 10a. Browser validation

| Rule | Layer | How I tested it | What happened |
|---|---|---|---|
| Full name is required | Browser | I left the form empty and clicked Get a ticket. | Chrome stopped at Full name and displayed “Please fill out this field.” |
| Contact number must be 11 digits starting with 09 | Browser | I entered `Test Applicant`, typed `123` as the contact number, selected Application and Testing, and submitted. | Chrome blocked submission and displayed “Please match the requested format.” |
| A queue must be selected | Browser | I entered a name and `09000000001`, left the queue unselected, and submitted. | Chrome blocked submission and prompted me to select an item from the list. |

The Join form uses `required` for all three inputs. The name field has `maxlength="100"`. The contact field has `maxlength="11"` and `pattern="09[0-9]{9}"`.

## 10b. Flask validation

I used `curl.exe` to send POST requests directly to `/join`, bypassing browser validation. Each request changed one field while the other two were valid.

| Rule | Layer | Request sent | What happened |
|---|---|---|---|
| Full name is required | Flask | Empty name, contact `09000000001`, service `1` | HTTP 400 |
| Contact number must match the required format | Flask | Name `Test Applicant`, contact `123`, service `1` | HTTP 400 |
| Selected service must exist | Flask | Name `Test Applicant`, contact `09000000001`, service `-1` | HTTP 400 |

I ran `SELECT COUNT(*) FROM tickets;` before and after the three requests. The count was **5 before and 5 after**. No ticket was created.

## 10c. PostgreSQL validation

I tested the constraints directly in PostgreSQL, bypassing Flask.

| Rule | Layer | How I tested it | Exact PostgreSQL error |
|---|---|---|---|
| FOREIGN KEY — ticket must reference an existing service | Database | Inserted a ticket with an existing user ID and service ID `-1`. | `ERROR:  insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` |
| CHECK — ticket status must be allowed | Database | Tried to change ticket `1` to `lost`. | `ERROR:  new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| UNIQUE — service name must be unique | Database | Tried to insert another `Application and Testing` service with the same duration. | `ERROR:  duplicate key value violates unique constraint "uq_services_name"` |
| CHECK — average duration must be positive | Database | Tried to insert `Validation Zero Minutes` with `avg_minutes = 0`. | `ERROR:  new row for relation "services" violates check constraint "ck_services_avg_minutes_positive"` |
| NOT NULL — applicant name is required | Database | Tried to insert a user with `name = NULL` and contact number `09000000001`. | `ERROR:  null value in column "name" of relation "users" violates not-null constraint` |
| ON DELETE RESTRICT — referenced services cannot be deleted | Database | Tried to delete service `1` while a ticket referenced it. | `ERROR:  update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` |

### Valid insert and database defaults

I inserted a ticket using only an existing `user_id` and `service_id`. PostgreSQL returned:

| id | status | created_at | queued_at |
|---|---|---|---|
| 13 | waiting | 2026-11-01 20:39:11.244825+00 | 2026-11-01 20:39:11.244825+00 |

PostgreSQL generated the ticket ID, set the status to `waiting`, and filled in both timestamps. I rolled back the transaction after recording the result.

## 10d. SQL f-string check

I searched the tracked Python files from Windows Command Prompt:

```bat
git grep -nE "f[[:punct:]].*(SELECT|INSERT|UPDATE|DELETE)" -- "*.py"
echo %ERRORLEVEL%
```

The search printed no matching lines and returned exit code `1`.