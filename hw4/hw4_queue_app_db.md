# Give Your Queue App a Database

| | |
| --- | --- |
| **Topic** | PostgreSQL, Docker and data persistence |
| **Common application** | Queue Management System |
| **Course learning outcomes** | CLO 1, CLO 2 |
| **Points** | 100 |
| **Format** | Self-paced and asynchronous. Work through Parts 0 to 11 in order, at your own pace. |
| **Released** | Monday, October 26, 2026 |
| **Due** | **TBD** |
| **Type** | Individual |

## Overview

In Week 3 you started your own queue app: a join form, a My place page and a staff dashboard, built for your own setting and tested with your personas. Two things are still missing.

- **Your app has no written requirements yet.** You built the screens straight from your personas. Before you design a database, you need a list of what the app must do, with an ID for each item, because every table and column you create must be there for a reason.
- **Your app has no memory.** Every ticket still lives in a Python list called `TICKETS`. Press Ctrl+C, run Flask again, and the whole queue is gone. In debug mode it even disappears every time you save a file.

**This week you write your requirements, and your app gets a memory.** By the end of this activity:

1. **Your requirements are written down** in `docs/requirements.md`: functional and non-functional requirements with IDs (such as FR-01), priorities, and a clear mark on every requirement that stores data. You check them with a real person from your setting.
2. **PostgreSQL runs in a Docker container**, described in a `compose.yaml` file in your repository, with its password kept out of Git.
3. **Your schema is designed from those requirements**: an entity-relationship diagram (ERD) with at least three related tables, keys and constraints.
4. **SQLAlchemy models and migrations** create those tables, and the migration scripts are committed with your code.
5. **Your three Week 3 screens read and write the database**, with working create, read, update and delete (CRUD) and validation in three layers.
6. **You prove it**: restart Flask and Docker, and every ticket is still there.

Keep this sentence in mind all week. It is the test your app must pass: *when a person joins your queue, their ticket must still be there after the server restarts, and no one else can take their place.*

Everything you build this week is used again. Your requirement IDs are used in every issue, pull request and report from now on. In Week 6 a REST API serves the same data, and in Week 7 you measure and speed up the queries.

### What you need

- Your Week 3 app, merged into `main` and tagged `week3`, in a **public** GitHub repository
- Your Week 3 personas (`docs/week3/personas.md`) and your usability test notes
- 10 minutes with one person from your setting, in person or by chat, to check your requirements (Part 1)
- **Docker** and the other software in **Before you start**, below. Install Docker before the week starts; it is a large download.
- Python 3.11 or newer, VS Code, Git and Google Chrome (from Weeks 2 and 3)
- A diagram tool for the ERD: draw.io, dbdiagram.io, or pen and paper
- About 11 to 13 hours spread across the week

### Before you start: install the software

Do this first, on good Wi-Fi. Docker can take an hour or more to set up the first time, especially on Windows.

| Software | Do I need it? | Download size | Get it from | Check that it works |
| --- | --- | --- | --- | --- |
| **Docker Desktop** (Windows or macOS) | **Yes, new this week** | about 600 MB | docker.com/products/docker-desktop | `docker --version` and `docker compose version` |
| **Docker Engine** with the Compose plugin (Linux) | Instead of Docker Desktop, on Linux | about 100 MB | docs.docker.com/engine/install | `docker compose version` |
| **PostgreSQL 17 image** | Yes; Docker downloads it for you | about 150 MB | `docker pull postgres:17` | `docker images` lists `postgres 17` |
| Python 3.11 or newer | Already installed in Week 2 | | python.org | `python --version` |
| VS Code | Already installed | | code.visualstudio.com | |
| Git | Already installed | | git-scm.com | `git --version` |
| Google Chrome | Already installed in Week 3 | | google.com/chrome | |
| PostgreSQL 17 installer | **Only** if your laptop cannot run Docker | about 350 MB | postgresql.org/download | `psql --version` |

Nothing else needs a separate download. The Python packages are installed with `pip` in Part 5, draw.io and dbdiagram.io run in the browser, and `curl` comes with Windows 10 and 11, macOS and Linux.

**Installing Docker on Windows**

1. Check that virtualization is on: open Task Manager → **Performance** → **CPU** and look for *Virtualization: Enabled*. If it says *Disabled*, turn on **Intel VT-x** or **AMD-V (SVM)** in your laptop's BIOS or UEFI settings. Search for your laptop model if you are not sure how.
2. Open PowerShell **as Administrator** and run `wsl --install`. Restart when it asks you to.
3. Install Docker Desktop and keep the option **Use WSL 2 instead of Hyper-V** ticked. Restart again if asked.
4. Open Docker Desktop and wait until it says *Engine running*.

**Installing Docker on macOS:** download the version for your chip. Choose **Apple silicon** for M1, M2, M3 or M4 Macs, or **Intel chip** for older Macs. You can check in the Apple menu → **About This Mac**. Drag it to Applications, open it, and wait until it says *Engine running*.

**Installing Docker on Linux:** follow the Docker Engine guide for your distribution, including the Compose plugin. Then run `sudo usermod -aG docker $USER` and log out and back in, so you can run `docker` without `sudo`.

**Then, on every system,** check it and download the database image in advance:

```
docker run --rm hello-world
docker pull postgres:17
```

The first command should print *Hello from Docker!*

Docker Desktop runs best with **8 GB of RAM** or more. With 4 GB it works, but close other apps while it runs. If you cannot get Docker working after following these steps, read the **No Docker?** box in Part 4 and use the PostgreSQL 17 installer instead. Do this early in the week, not on the due date.

### Time plan

| Part | What you do | Time |
| --- | --- | --- |
| 0 | Get ready for Week 4 | 30 min |
| 1 | Write your requirements | 1.5 h |
| 2 | Design your schema and draw your ERD | 1.5 h |
| 3 | Self-review of your schema | 30 min |
| 4 | Run PostgreSQL in Docker | 1 h |
| 5 | Connect Flask and write your models | 1.5 h |
| 6 | Your first migration and starting data | 45 min |
| 7 | Create: joining the queue | 1 h |
| 8 | Read: My place and the staff dashboard | 1 h |
| 9 | Update and delete, and a second migration | 1.5 h |
| 10 | Validation in three layers | 45 min |
| 11 | Prove it persists, report and submission | 1 h 15 min |

---

## Part 0: Get ready for Week 4

**Goal:** a clean branch, Docker working, and no secrets in your repository.

1. In your repository, create a GitHub issue:
   - **Title:** `Week 4: persist the queue in PostgreSQL`
   - **Description:** one sentence on the goal for now. After Part 1, edit the issue and list the requirement IDs this week covers.
   - **Labels:** `feature`, `Must` · **Milestone:** MVP
2. Branch from an up-to-date `main`:

   ```
   git switch main
   git pull origin main
   git switch -c feature/week4-database
   ```

3. Check that Docker works (see **Before you start** if you have not installed it yet). Open Docker Desktop first (on Windows and macOS it must be running), then in a terminal:

   ```
   docker --version
   docker compose version
   docker run --rm hello-world
   ```

   The last command should print *Hello from Docker!* If it fails on Windows, check that WSL 2 is installed (`wsl --status`) and that virtualization is turned on in your BIOS. If your laptop cannot run Docker at all, read the **No Docker?** box in Part 4 before you go on.

4. **New this week:** make sure your repository is **public**, so your instructor can open your report link. On GitHub, open your repository → **Settings** → **General** → scroll to **Danger Zone** → **Change visibility** → **Make public**. Because anyone can see a public repository, the next step matters even more.

5. Make sure no password file was ever committed. Both commands should print nothing:

   ```
   git ls-files .env
   git log --all --oneline -- .env
   ```

   If either prints something, a `.env` file is in your Git history. Removing it in a new commit is not enough, because the old commit still holds it. Run `git rm --cached .env`, add `.env` to `.gitignore`, commit, and **never reuse that password**.

**Checkpoint 0**

- [x] The issue exists and you are on `feature/week4-database`.
- [x] `docker run --rm hello-world` prints *Hello from Docker!* (or you have planned the local PostgreSQL fallback).
- [x] Your repository is public.
- [x] No `.env` file is tracked by Git.

---

## Part 1: Write your requirements

**Goal:** a written list of what your app must do, each item with an ID, a priority, and a mark showing whether it stores data. Your database is designed from this list in Part 2, and every later week refers back to these IDs.

A requirement is a promise about what the app does, written so that anyone can test it. In Week 3 you built screens from your personas; now you write down what those screens do, and what the app still has to do, as a list you can check off. Create **`docs/requirements.md`**. It is not in a `week4` folder because it is a living document: you will add to it and update the status of each item every week.

### 1a. Describe your setting and the problem

Start the file with a short header:

```markdown
# <YourApp> requirements

**Setting:** [Office, business or event, e.g. "University clinic, weekday mornings"]
**People who wait:** [Who they are; link your persona, e.g. Mika in docs/week3/personas.md]
**People who serve:** [Who they are; link your persona]

**Problem statement:** [User] needs a way to [need] because [insight].
```

Write the problem statement from your personas and your Week 3 usability test, for example: *"A student who visits the clinic between classes needs a way to know when it is their turn without standing in line, because they lose their place whenever they step out."*

### 1b. Functional requirements

A functional requirement says **what the app does**. Write at least **10**, in a table:

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | A student can join the queue for a service by entering their name and email. | Must | **Yes** | Built (Week 3) |
| FR-02 | A student can see their ticket number, status, and how many people are ahead of them. | Must | **Yes** | Built (Week 3) |
| FR-03 | A staff member can call the next waiting ticket for a service. | Must | **Yes** | Built (Week 3) |
| FR-04 | A staff member can mark a called ticket as served or no-show. | Must | **Yes** | Built (Week 3) |
| FR-05 | A student can leave the queue before being called. | Must | **Yes** | Built (Week 3) |
| FR-06 | A staff member can add, rename and switch off a service. | Must | **Yes** | This week |
| FR-07 | A staff member can see how many people left before being served, per service, per day. | Should | **Yes** | Later |
| FR-08 ★ | A senior citizen or person with a disability can join a priority lane that is served first. | Should | **Yes** | Later |
| FR-09 | A student can switch the page to a larger text size. | Could | No | Later |

Rules for good requirements:

- **Start with the user:** *"A [person] can [do something]."* Each row is one action.
- **Make it testable.** Someone else should be able to try it and say yes or no. *"The app is easy to use"* is not testable; *"A student can join the queue in under 30 seconds"* is.
- **Give every requirement an ID** (FR-01, FR-02, …). Never reuse or renumber an ID, even if you drop that requirement; mark it *Dropped* instead.
- **Priority** is one of **Must**, **Should**, **Could** or **Won't (this semester)**.
- Mark requirements that are specific to your setting with **★**, such as a priority lane, a preferred barber, or a counter number. You need **at least three ★**.
- **Stores data?** is **Yes** if the app must still remember something after the server restarts. These rows are the input for your database in Part 2, so be careful with this column.
- **Status** is *Built (Week 3)*, *This week*, *Later* or *Dropped*. Start with what you already built in Week 3, then add your personas' top tasks that are not built yet.

If your Week 3 personas have a top-tasks table with requirement IDs, update those IDs to match this list.

### 1c. Non-functional requirements

A non-functional requirement says **how well** the app must work. Write at least **4**, each with a number or a clear test. Include at least one about data, since that is this week's topic:

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | No ticket is lost when the server or the database restarts. | Reliability | Must |
| NFR-02 | Two people can never get the same ticket, even if they join at the same moment. | Data integrity | Must |
| NFR-03 | My place loads in under 2 seconds on mobile data. | Performance | Should |
| NFR-04 | Every screen scores 90 or higher in the Lighthouse accessibility check. | Accessibility | Must |
| NFR-05 | No password or secret key is stored in the repository. | Security | Must |

### 1d. Your MVP

Under the tables, write:

- **MVP:** the list of IDs that make up your minimum viable product (usually all the *Must* rows), and one or two sentences on why this is the smallest version that still solves the problem.
- **Out of scope:** at least two features you will **not** build this semester, and why.

### 1e. Check your requirements with a real person

Show your list to **one person from your setting**, either someone who waits or someone who serves, for about 10 minutes. You can meet in person or send it by chat. Not a CCC181 classmate. Ask them:

1. Is anything missing that you would need?
2. Is anything here wrong, or not important to you?
3. Which three matter most to you?

At the bottom of `requirements.md`, add a short table:

| Who (role only, no full name) | What they said | What I changed |
| --- | --- | --- |
| Clinic nurse | "We also need to know who was a no-show twice this week." | Added FR-10 (Should) |

Make **at least one change** from what you heard, or explain why you kept the list as it is. Then add a link to `docs/requirements.md` in your `README.md`, and edit your Part 0 issue to list the requirement IDs this week covers.

**Checkpoint 1**

- [x] `docs/requirements.md` has the setting, a problem statement, at least 10 functional requirements (at least 3 ★) and at least 4 non-functional requirements.
- [x] Every requirement has an ID and a priority; every functional requirement has *Stores data?* and *Status* filled in.
- [x] The MVP and out-of-scope lists are written.
- [x] The feedback table shows one real person's comments and what you changed.
- [x] `README.md` links to `docs/requirements.md`, and your issue lists the requirement IDs.
- [x] Committed: `git commit -m "Add requirements (#<issue>)"`

---

## Part 2: Design your schema and draw your ERD

**Goal:** decide which tables your app needs, what goes in each, and how they connect, **before** writing any code. The ERD is the wireframe of your database.

Create `docs/week4/schema.md` and work through 2a to 2e in it.

### 2a. Find the nouns in your requirements

Copy each requirement from Part 1 with **Stores data? = Yes** into a table and **bold** the nouns. Nouns are candidate tables; details about a noun are columns.

| Req ID | Requirement | Nouns | Table or column? |
| --- | --- | --- | --- |
| FR-01 | A **student** can join the **queue** for a **service** by entering their **name** and **email**. | student, queue, service, name, email | users, *(not a table)*, services, users.name, users.email |
| FR-02 | A student can see their **ticket number**, **status**, and how many people are **ahead** of them. | ticket number, status, ahead | tickets.id, tickets.status, *(computed)* |

Two rules from this week's lecture:

- **The queue is not a table.** It is all tickets with status `waiting` for one service, ordered by the time they joined.
- **Store facts, not results.** Store *when* a ticket was created (`created_at`); compute the position when you need it. A stored position would need rewriting for many rows every time someone joins or leaves.

### 2b. List your tables and columns

Start from ClinicQ's three tables and change them for your setting:

| Table | ClinicQ columns |
| --- | --- |
| `users` | id, name, email, role |
| `services` | id, name, avg_minutes |
| `tickets` | id, user_id, service_id, status, created_at, called_at |

Your schema needs **at least three related tables**. Add what your setting needs. Look back at the extra fields you added in Week 3 (a student ID, a priority lane, a preferred barber) and decide where each one belongs by asking: *is this a fact about the person, about the service, or about this one visit?*

- A student ID is about the person, so it goes in `users`.
- Whether this visit uses the priority lane may change every visit, so it goes in `tickets`.
- A preferred barber is a person the shop employs, so it may need its own `barbers` table, with `tickets.barber_id` pointing to it.

If your setting has staff who work several services, that is a many-to-many relationship and needs a join table such as `staff_services(user_id, service_id)`. A fourth table is not required, but most real settings need one.

### 2c. Choose types and constraints on purpose

In `schema.md`, write one row for **every column** of every table:

| Table | Column | PostgreSQL type | Constraint | Why |
| --- | --- | --- | --- | --- |
| tickets | id | integer, generated | PRIMARY KEY | Generated by the database, never reused |
| users | email | varchar(120) | NOT NULL UNIQUE | One account per email |
| tickets | status | varchar(20) | NOT NULL, CHECK (status IN (…)) | Only waiting, called, served, no-show, left |
| tickets | created_at | timestamptz | NOT NULL DEFAULT now() | Time zone safe; set by the database |
| tickets | service_id | integer | NOT NULL REFERENCES services(id) | No ticket for a missing service |
| services | avg_minutes | integer | CHECK (avg_minutes > 0) | Rejects impossible values |

Your schema must use **every one** of these at least once: PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE, CHECK, and a `timestamptz` column. Never store dates, times or numbers as text.

### 2d. Draw the ERD

Draw your tables as boxes in draw.io, dbdiagram.io, or on paper (take a clear photo). For each table, show:

- the table name, every column, and which columns are **PK** and **FK**
- a line for every relationship, labelled with its kind: **1 : N** (one-to-many), **N : M** (many-to-many, through a join table) or **1 : 1**

Under the diagram in `schema.md`, **read each relationship aloud** in one sentence, as ClinicQ does: *"One user has many tickets. One service has many tickets. Each ticket belongs to exactly one user and one service."* The foreign key always sits on the "many" side.

For each foreign key, also decide **what happens when the parent row is deleted**: block it (`RESTRICT`), delete the children too (`CASCADE`), or set the key to empty (`SET NULL`). Write your choice and the reason. For ClinicQ, deleting a service must not delete its old tickets, because the clinic needs them for reports, so tickets use `RESTRICT`.

Save the image as `docs/week4/erd.png` (or `.jpg` or `.pdf`) and show it in `schema.md` with `![ERD](erd.png)`.

### 2e. Check that it is normalized

Answer these three questions in `schema.md`:

1. **One value per cell (1NF):** does any column hold a list, such as `"Haircut, Shave"`?
2. **Depends on the whole key (2NF):** in each join table, does every extra column depend on *both* keys?
3. **No hidden copies (3NF):** would you ever have to update the same fact, such as a person's email or a service's name, in more than one row?

If the answer to any of these is yes, split that data into its own table and link it with a key.

**Checkpoint 2**

- [x] `docs/week4/schema.md` has the nouns table, the full types-and-constraints table, the relationship sentences, the delete rules, and the normalization answers.
- [x] The ERD has at least three related tables, with PKs, FKs and every relationship labelled.
- [x] Your schema uses PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE, CHECK and `timestamptz` at least once each.
- [x] No column stores a result that can be computed, such as a position in line.
- [x] Committed: `git commit -m "Add Week 4 schema design and ERD (#<issue>)"`

---

## Part 3: Self-review of your schema

**Goal:** catch design mistakes while they are still cheap to fix. Changing a box in a diagram takes a minute; changing a table full of data takes a migration.

Put your ERD away for at least an hour, then review it as if it were someone else's. Answer each question:

1. **Coverage:** does every requirement in `docs/requirements.md` marked *Stores data? = Yes* have a table or column for it? Does each persona's top task from Week 3 have the data it needs? Is there any table or column that **no** requirement needs? (Then either a requirement is missing, or the column is.)
2. **One fact in one place:** is any fact stored in more than one row or table?
3. **Facts, not results:** am I storing anything I could compute instead, such as a position, a count or a waiting time?
4. **Bad data:** think of the mistakes your personas could make (a double tap, a typo in an email, picking the wrong service). Which constraint stops each one from reaching the database?
5. **Deletes:** for every foreign key, did I choose RESTRICT, CASCADE or SET NULL on purpose? Would any delete destroy history the staff need?
6. **Types:** is every moment in time a `timestamptz`? Is anything stored as text that should be a number, a date or a true/false value?

Write the review in `docs/week4/schema-review.md`, with **at least three** entries in this format:

> **Works well:** one thing in the schema that works and why.
> **Problem:** one problem you found, and which question above found it.
> **Change:** what you changed in the ERD and `schema.md`, or why you kept it.

Update your ERD and `schema.md` with the changes before you start Part 4.

**Checkpoint 3**

- [ ] `docs/week4/schema-review.md` has at least three *Works well / Problem / Change* entries.
- [ ] Your ERD and `schema.md` are updated, or the review explains why you kept them.
- [ ] Committed.

---

## Part 4: Run PostgreSQL in Docker

**Goal:** a PostgreSQL database running in a container, started with one command, with its password outside Git.

### 4a. Write `compose.yaml`

Create `compose.yaml` in the root of your repository. Replace every `yourapp` with a short lowercase name for your app, with no spaces (for example `barberq`):

```yaml
services:
  db:
    image: postgres:17
    container_name: yourapp-db
    environment:
      POSTGRES_USER: yourapp
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: yourapp
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U yourapp -d yourapp"]
      interval: 5s
      timeout: 3s
      retries: 10

volumes:
  pgdata:
```

What to notice:

- **`postgres:17`**, never `latest`, so everyone runs the same version. A newer major version can refuse to open an older data folder.
- **`${POSTGRES_PASSWORD}`** is read from a `.env` file next to `compose.yaml`. The password never appears in a committed file.
- **`pgdata`** is a named volume. The container can be deleted and recreated; the data stays in the volume.
- **`healthcheck`** lets `docker compose ps` tell you when the database is ready, not just started.

### 4b. Keep the password out of Git

Create **`.env`** (never committed):

```
POSTGRES_PASSWORD=change-me
DATABASE_URL=postgresql+psycopg://yourapp:change-me@localhost:5432/yourapp
```

Use your own password in both lines. Read the URL left to right: `postgresql+psycopg` is the database and the Python driver, `yourapp:change-me` is the user and password, and `localhost:5432/yourapp` is the host, port and database name.

Add `.env` to `.gitignore`:

```
.env
```

Then create **`.env.example`** with the same variable names but placeholder values, and **commit it**. It tells your instructor which variables your app needs, without giving away your password:

```
POSTGRES_PASSWORD=change-me
DATABASE_URL=postgresql+psycopg://yourapp:change-me@localhost:5432/yourapp
```

Check: `git status` should list `.env.example` and `compose.yaml`, and should **not** list `.env`.

### 4c. Start the database and look inside

These are the commands you will use every day:

| Command | What it does |
| --- | --- |
| `docker compose up -d` | Start the database in the background |
| `docker compose ps` | Check that it is running and **healthy** |
| `docker compose logs db` | Read the database's output when something fails |
| `docker compose exec db psql -U yourapp` | Open a SQL prompt inside the container |
| `docker compose down` | Stop and remove the container; **the data stays** in the volume |
| `docker compose down -v` | Also deletes the volume and **all your data** |

Start it and open a SQL prompt:

```
docker compose up -d
docker compose ps
docker compose exec db psql -U yourapp
```

At the `yourapp=#` prompt, type `SELECT version();` and press Enter. You should see *PostgreSQL 17*. Type `\dt` to list tables (there are none yet) and `\q` to quit. Commands that start with a backslash are psql commands, not SQL.

**If something goes wrong:**

- *"port is already allocated"*: another PostgreSQL is already using port 5432 on your laptop. Change the port line to `"5433:5432"` and change `localhost:5432` to `localhost:5433` in `.env` and `.env.example`.
- *"Cannot connect to the Docker daemon"*: Docker Desktop is not running. Open it and wait until it says it is running.
- *Password errors after you changed `.env`*: the password is only set the first time the volume is created. Run `docker compose down -v` once to start fresh (this deletes the data, which is fine now because there is none).

> **No Docker?** If your laptop truly cannot run Docker, install PostgreSQL 17 directly from postgresql.org. Open `psql -U postgres` and run `CREATE USER yourapp WITH PASSWORD 'your-password';` and then `CREATE DATABASE yourapp OWNER yourapp;`. Your `DATABASE_URL` stays the same, and the Flask code does not change. Use `psql -U yourapp -d yourapp` wherever this activity says `docker compose exec db psql -U yourapp`, and restart the PostgreSQL service wherever it says `docker compose down` and `up -d`. **Still commit `compose.yaml`** so your instructor can run your app, and say in your report that you used the fallback.

**Checkpoint 4**

- [x] `docker compose ps` shows your database as **healthy**.
- [x] `SELECT version();` in psql shows PostgreSQL 17.
- [x] `compose.yaml` and `.env.example` are committed; `.env` is in `.gitignore` and not tracked.
- [x] Committed: `git commit -m "Run PostgreSQL in Docker Compose (#<issue>)"`

---

## Part 5: Connect Flask and write your models

**Goal:** your tables written as Python classes, and Flask connected to the database.

### 5a. Install the packages

With your virtual environment active:

```
pip install Flask-SQLAlchemy Flask-Migrate "psycopg[binary]" python-dotenv
pip freeze > requirements.txt
```

| Package | What it does |
| --- | --- |
| Flask-SQLAlchemy | Connects SQLAlchemy, the ORM, to Flask |
| Flask-Migrate | Adds `flask db` commands for migrations (it uses Alembic) |
| psycopg | The PostgreSQL driver for Python (version 3) |
| python-dotenv | Loads `.env`, so Flask can read `DATABASE_URL` |

### 5b. Write `models.py`

Create `models.py` next to `app.py`. This is ClinicQ's version, written from its ERD. **Write yours from your own ERD**: your tables, your columns, your constraints.

```python
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    role: Mapped[str] = mapped_column(String(20), default="visitor", server_default="visitor")

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint("role IN ('visitor', 'staff')", name="ck_users_role"),
    )


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    avg_minutes: Mapped[int] = mapped_column(default=10)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")

    __table_args__ = (
        CheckConstraint("avg_minutes > 0", name="ck_services_avg_minutes"),
    )


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(20), default="waiting", server_default="waiting")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    called_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="RESTRICT"))

    user: Mapped["User"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'left')",
            name="ck_tickets_status",
        ),
    )
```

What to notice:

- **`Mapped[int]`** makes a NOT NULL column. **`Mapped[datetime | None]`** makes it nullable: a waiting ticket has not been called yet, so `called_at` can be empty.
- **`String(80)`** becomes `varchar(80)`. **`DateTime(timezone=True)`** becomes `timestamptz`.
- **`default`** is filled in by Python; **`server_default`** becomes part of the table, so rows inserted from psql get it too.
- **`relationship(back_populates=...)`** adds an attribute that loads the linked row, on both sides. You can now write `ticket.service.name` and `ticket.user.email`, in Python and in templates.
- **Name every `CheckConstraint`**, so error messages and migrations can refer to it.
- The statuses match your Week 3 app. Use the statuses **your** setting needs.

**Make it yours:** add the columns and tables from your ERD, including the setting-specific fields you placed in Part 2b. For a many-to-many join table, make a class with two foreign keys that together form the primary key (`primary_key=True` on both).

### 5c. Connect Flask

At the top of `app.py`, add the imports and configuration. Keep your Week 3 `secret_key`:

```python
import os

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Service, Ticket, User, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)
```

`db` lives in `models.py` and is imported here, which avoids circular imports. If Flask stops with `KeyError: 'DATABASE_URL'`, your `.env` file is missing or not in the folder you run Flask from.

**See the SQL.** An ORM still runs SQL; it just writes it for you. Add `SQLALCHEMY_ECHO=1` to your `.env` and every query Flask sends is printed in the terminal. Turn it on at least once this week and read what it prints, then remove the line.

**Checkpoint 5**

- [x] `models.py` has a class for every table in your ERD, with the keys, constraints and relationships from your `schema.md`.
- [x] `requirements.txt` lists Flask-SQLAlchemy, Flask-Migrate, psycopg and python-dotenv with pinned versions.
- [x] `flask --app app routes` runs without errors.
- [x] Committed: `git commit -m "Add SQLAlchemy models (#<issue>)"`

---

## Part 6: Your first migration and starting data

**Goal:** the tables created in PostgreSQL by a migration script that lives in Git, and your services added by one command.

### 6a. Create and apply the migration

```
flask --app app db init
flask --app app db migrate -m "initial tables"
flask --app app db upgrade
```

| Command | What it does | How often |
| --- | --- | --- |
| `flask db init` | Creates the `migrations/` folder | Once per project |
| `flask db migrate -m "..."` | Compares your models to the database and **writes** a script | Every time models change |
| `flask db upgrade` | **Runs** the scripts the database has not had yet | After every migrate, and after every pull |
| `flask db downgrade` | Undoes the last script | When you made a mistake |

**Review before you upgrade.** Open the new file in `migrations/versions/`. It is readable Python with an `upgrade()` that creates your tables and a `downgrade()` that drops them. Check that every table, column, `nullable=False`, `UniqueConstraint`, `CheckConstraint` and `ForeignKeyConstraint` from your `schema.md` is there. Autogenerate guesses; if it guessed wrong, fix your models, delete the unapplied script, and run `migrate` again.

Then check the result in psql:

```
docker compose exec db psql -U yourapp
\dt
\d tickets
```

`\d` shows each column's type, whether it can be empty, its default, and every constraint. You will put this output in your report.

Two rules:

- **Do not use `db.create_all()`.** It only creates missing tables, never adds a column to a table that exists, and keeps no history.
- **Never edit a migration that has already been applied** (on your laptop, or after you pushed it). Write a new migration instead.

### 6b. Add your starting services

Every copy of your app needs the same services. Instead of typing them into psql, add a small command to `app.py`, using **your** services from Week 3:

```python
@app.cli.command("seed")
def seed():
    """Add the starting services if they are not there yet."""
    starting = [("Consultation", 15), ("Medical certificate", 5)]
    for name, minutes in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name, avg_minutes=minutes))
    db.session.commit()
    print("Services are ready.")
```

Run `flask --app app seed`, then run it again. The second run must not add duplicates. Check with `SELECT * FROM services;` in psql.

**Checkpoint 6**

- [x] `\dt` lists all your tables, and `\d` for each one shows the constraints from your `schema.md`.
- [x] The `migrations/` folder is committed, including the script in `migrations/versions/`.
- [x] `flask --app app seed` adds your services and is safe to run twice.
- [x] Committed: `git commit -m "Add initial migration and seed command (#<issue>)"`

---

## Part 7: Create: joining the queue

**Goal:** the join form saves a ticket in PostgreSQL instead of the `TICKETS` list.

**Delete the `SERVICES` and `TICKETS` lists** from `app.py`. From now on all data comes from the database. Flask will show errors wherever your routes still use them; Parts 7 to 9 replace each one.

Add a helper that returns the services for the join form, then replace your Week 3 `join_form` and `join` routes:

```python
def all_services():
    return db.session.scalars(db.select(Service).order_by(Service.name)).all()


@app.get("/join")
def join_form():
    return render_template("join.html", services=all_services(), form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    service = db.session.get(Service, service_id) if service_id else None

    errors = {}
    if not name or len(name) > 80:
        errors["name"] = "Enter your name (up to 80 characters)."
    if "@" not in email or len(email) > 120:
        errors["email"] = "Enter a valid email address."
    if service is None:
        errors["service_id"] = "Choose a service."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors=errors), 400

    user = db.session.scalar(db.select(User).filter_by(email=email))
    if user is None:
        user = User(name=name, email=email)
    ticket = Ticket(user=user, service=service)
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Something went wrong saving your ticket. Please try again.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors={}), 409

    flash(f"You joined the queue. Your ticket is #{ticket.id}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))
```

Walk through it top to bottom:

1. **Read and clean** the input: strip spaces, lowercase the email, convert the service to a number.
2. **Validate**, and check that the service really exists in the database. The length limits match the `String(80)` and `String(120)` columns.
3. **Reuse or create the user.** A person who comes back with the same email gets a new ticket, not a second account, because `users.email` is UNIQUE.
4. **Add and commit.** Nothing is saved until `db.session.commit()`. Adding the ticket also adds the new user, because of the relationship.
5. **Redirect** to My place (Post/Redirect/Get, from Week 2), so a refresh cannot create a second ticket. After the commit, `ticket.id` holds the number PostgreSQL generated.

The `try/except IntegrityError` is the database saying no. If two requests with the same new email arrive at the same moment, both pass the Python check, but only one can insert the user. The other gets an `IntegrityError`, and the session **must be rolled back** before it can be used again.

**Your Week 3 templates now get objects instead of dictionaries.** In every template, change `ticket.number` and `t.number` to `.id`. `join.html` needs no change, because `s.id` and `s.name` work the same for objects.

**Make it yours:** save the setting-specific fields from your Week 3 form into the columns you gave them in Part 2b (on `User`, on `Ticket`, or in your own table), with the same server-side checks as before.

**Checkpoint 7**

- [x] The `SERVICES` and `TICKETS` lists are gone from `app.py`.
- [x] Joining creates a row in `tickets`, shown by `SELECT * FROM tickets;` in psql.
- [x] Joining twice with the same email (try different capital letters) creates two tickets but only one row in `users`.
- [x] An empty or invalid form still shows the Week 3 error messages and saves nothing.
- [x] Committed.

---

## Part 8: Read: My place and the staff dashboard

**Goal:** My place and the staff dashboard read from the database, and position in line is computed, not stored.

### 8a. Position in line

Add this helper. It counts the tickets that are still waiting for the same service and joined earlier. Filtering and counting happen in the database, not in Python:

```python
def people_ahead(t):
    """Count tickets still waiting for the same service that joined before t."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.service_id == t.service_id,
                   Ticket.status == "waiting",
                   Ticket.created_at < t.created_at))
    return db.session.scalar(stmt)
```

### 8b. My place and its JSON route

Replace your Week 3 `ticket` and `ticket_status` routes:

```python
@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return render_template("ticket.html", ticket=t, service=t.service,
                           ahead=people_ahead(t))


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return {"status": t.status, "ahead": people_ahead(t)}
```

`db.get_or_404` returns the row by its primary key, or a proper 404 page for a ticket that does not exist. Your Week 3 JavaScript that refreshes My place every 10 seconds keeps working, because the JSON looks the same.

### 8c. Show times in Philippine time

PostgreSQL stores `timestamptz` values in UTC. Add a template filter to `app.py` so people see their own local time:

```python
from datetime import timedelta, timezone

PH_TIME = timezone(timedelta(hours=8))  # Philippine time has no daylight saving


@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Oct 26, 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""
```

On My place, add the time the person joined: `Joined {{ ticket.created_at|local }}`.

### 8d. The staff dashboard

Replace your Week 3 `staff_dashboard` route:

```python
@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    stmt = (db.select(Ticket)
            .where(Ticket.status.in_(["waiting", "called"]))
            .order_by(Ticket.created_at))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    queue = db.session.scalars(stmt).all()
    return render_template("staff.html", queue=queue, services=all_services(),
                           selected=service_id)
```

`db.select(...)` only builds the query; `db.session.scalars(stmt).all()` runs it and returns a list of `Ticket` objects. In `staff.html`, replace the Week 3 lookups with the relationships: `{{ t.user.name }}` instead of `{{ t.name }}`, and `{{ t.service.name }}` instead of `{{ names[t.service_id] }}`. Add a **Joined** column with `{{ t.created_at|local }}`.

Do not use the old `Ticket.query` style you may find online. It is legacy in SQLAlchemy 2.0.

**Checkpoint 8**

- [x] My place shows the number, service, status, position and the time joined, read from the database.
- [x] `/queue/99999` shows a 404 page, not a server error.
- [x] The staff dashboard lists waiting and called tickets in the order they joined, filters by service, and shows each person's name through `t.user.name`.
- [x] No `position` column exists anywhere in your schema.
- [x] Committed.

---

## Part 9: Update and delete, and a second migration

**Goal:** staff actions and leaving the queue change the database, your app has at least one real delete, and you change the schema safely with a second migration.

### 9a. Update: staff actions

Replace your Week 3 `staff_action` route. Updating is: load the object, change its attributes, commit.

```python
STAFF_ACTIONS = {"call": "called", "serve": "served", "no-show": "no-show"}


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = STAFF_ACTIONS.get(action)
    if new_status is None:
        abort(404)
    t = db.get_or_404(Ticket, ticket_id)
    t.status = new_status
    if new_status == "called":
        t.called_at = func.now()  # the database fills in the time
    db.session.commit()
    flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard"))
```

Update your **Call next** button the same way: find the first waiting ticket with `.filter_by(status="waiting").order_by(Ticket.created_at).limit(1)` and `db.session.scalar(stmt)`, set its status to `called`, and commit. If no one is waiting, flash a message instead.

### 9b. Soft delete: leaving the queue

When a person leaves, **keep the row** and change its status. The staff need it later to report how many people left before being served.

```python
@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    if t.status == "waiting":
        t.status = "left"  # soft delete: the row stays for reports
        db.session.commit()
    flash("You left the queue.", "info")
    return redirect(url_for("index"))
```

### 9c. Hard delete: removing a mistaken ticket

Sometimes a row should really go, for example a test ticket or one created by mistake. Add a **Delete** button on each dashboard row, as a small POST form, and this route:

```python
@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    db.session.delete(t)  # hard delete: the row is gone for good
    db.session.commit()
    flash(f"Ticket #{ticket_id} was deleted.", "warning")
    return redirect(url_for("staff_dashboard"))
```

A hard delete cannot be undone, so ask first. Give the form a `data-confirm` attribute, such as `<form method="post" action="..." data-confirm="Delete ticket 14? This cannot be undone.">`, and add this to `static/js/main.js`:

```javascript
document.querySelectorAll("form[data-confirm]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (!confirm(form.dataset.confirm)) event.preventDefault();
  });
});
```

Every route that changes data in this part is a **POST**. A GET link can be followed by a browser prefetch, a link preview or a search engine, and would serve or delete a ticket by accident.

### 9d. A second migration: switching a service off

Your setting will change after launch: a service stops for the semester, or a new one starts. You will add a column to a table that already has data, which is exactly what migrations are for.

1. In `models.py`, add `true` to the `sqlalchemy` import, and add this column to `Service`:

   ```python
   active: Mapped[bool] = mapped_column(default=True, server_default=true())
   ```

   The `server_default` matters: the table already has rows, and PostgreSQL needs a value to put in them for a NOT NULL column.

2. Generate, **review**, and apply the migration:

   ```
   flask --app app db migrate -m "add services.active"
   flask --app app db upgrade
   ```

   Open the new script and check that it only adds one column. Then run `flask --app app db downgrade` and `flask --app app db upgrade` once, to see that the change can be undone and redone. In psql, `SELECT * FROM services;` shows `active` as `t` for every existing service.

3. Add a **Manage services** page for staff at `/staff/services`, with:
   - a list of all services, showing their name, average minutes, whether they are active, and how many tickets each has (`{{ s.tickets|length }}`)
   - **Create:** a form that adds a service
   - **Update:** a form for each service that changes its name, average minutes, and an **Active** checkbox
   - **Delete:** a button that deletes a service, which must be refused if the service has tickets

   The create and delete routes, which show how to handle the database saying no:

   ```python
   @app.post("/staff/services")
   def service_create():
       name = request.form.get("name", "").strip()
       minutes = request.form.get("avg_minutes", type=int)
       if not name or len(name) > 60 or not minutes or minutes <= 0:
           flash("Enter a name (up to 60 characters) and minutes greater than 0.", "danger")
           return redirect(url_for("services_list"))
       db.session.add(Service(name=name, avg_minutes=minutes))
       try:
           db.session.commit()
           flash(f"Service “{name}” added.", "success")
       except IntegrityError:
           db.session.rollback()
           flash(f"A service named “{name}” already exists.", "danger")
       return redirect(url_for("services_list"))


   @app.post("/staff/services/<int:service_id>/delete")
   def service_delete(service_id):
       s = db.get_or_404(Service, service_id)
       if s.tickets:
           flash(f"“{s.name}” has tickets, so it cannot be deleted. Turn it off instead.", "danger")
           return redirect(url_for("services_list"))
       db.session.delete(s)
       db.session.commit()
       flash(f"Service “{s.name}” deleted.", "warning")
       return redirect(url_for("services_list"))
   ```

   Write the `services_list` (GET) and `service_edit` (POST) routes yourself, following the same pattern. In the edit route, a checkbox that is not ticked is not sent at all, so use `s.active = request.form.get("active") == "on"`, and catch `IntegrityError` for a duplicate name.

4. Make the join form show **only active services**. Add a second helper, and use it instead of `all_services()` in `join_form()` and `join()`. In `join()`, also treat a service that is not active the same as one that does not exist (`if service is None or not service.active:`). The staff dashboard and Manage services keep using `all_services()`.

   ```python
   def active_services():
       stmt = db.select(Service).filter_by(active=True).order_by(Service.name)
       return db.session.scalars(stmt).all()
   ```

Staff login comes in Week 11. For now the staff pages are open. Create a GitHub issue titled `Protect staff routes (Week 11)` so you do not forget, and say so in your README.

**Make it yours:** if your ERD has a table specific to your setting (counters, barbers, priority categories, staff assignments), give it at least create and read in the app. Full CRUD for it is a plus.

**Checkpoint 9**

- [x] Call next, Serve and No-show change the status in the database, and calling sets `called_at`.
- [x] Leaving the queue sets the status to `left`, and the row is still in `tickets`.
- [x] A mistaken ticket can be hard-deleted from the dashboard, after a confirmation.
- [x] The second migration is committed, and `downgrade` then `upgrade` both work.
- [x] Manage services can create, update, switch off and delete a service; deleting a service with tickets is refused with a clear message; a switched-off service no longer appears on the join form.
- [x] Every route that changes data is a POST.
- [x] Committed.

---

## Part 10: Validation in three layers

**Goal:** show that bad data is stopped even when someone skips your form.

The same rule lives in three places. **The browser is for users** (fast feedback), **Flask is for security** (the real gatekeeper), and **the database is for integrity** (the last line of defense against any bug).

### 10a. Browser

Make your form attributes match your columns: `required` on every NOT NULL field, `type="email"` for email, and `maxlength` equal to the column length (`maxlength="80"` for a `String(80)` name). These help honest users. Anyone can skip them.

### 10b. Flask: skip the browser on purpose

With your app running, send a bad request **without the form**, using curl in a second terminal (on Windows PowerShell, type `curl.exe`, not `curl`):

```
curl -i -X POST http://127.0.0.1:5000/join -d "name=" -d "email=not-an-email" -d "service_id=999"
```

You should see `HTTP/1.1 400 BAD REQUEST`, and `SELECT count(*) FROM tickets;` in psql should not change. Try at least two more bad requests of your own, such as a name that is 200 characters long, or a service that is switched off.

### 10c. Database: skip Flask on purpose

In psql, try to insert bad data directly. Change the ids and values to fit your tables. **Every one of these must fail** with an `ERROR`:

```sql
-- A ticket for a service that does not exist (foreign key)
INSERT INTO tickets (user_id, service_id) VALUES (1, 999);

-- A status that is not allowed (CHECK). Use a ticket id that exists.
UPDATE tickets SET status = 'lost' WHERE id = 1;

-- A second account with an email that is already used (UNIQUE)
INSERT INTO users (name, email) VALUES ('Copy', 'ana@school.edu');

-- An impossible value (CHECK)
INSERT INTO services (name, avg_minutes) VALUES ('Test', 0);

-- Deleting a service that still has tickets (ON DELETE RESTRICT)
DELETE FROM services WHERE id = 1;
```

Then insert one **good** row and see the defaults the database fills in:

```sql
INSERT INTO tickets (user_id, service_id) VALUES (1, 1) RETURNING id, status, created_at;
```

### 10d. No SQL in f-strings

Building SQL by gluing user input into a string lets the input become code (SQL injection). With `' OR '1'='1` as an email, `f"SELECT * FROM users WHERE email = '{email}'"` returns every user. SQLAlchemy always sends values separately from the SQL. Check that your code never builds SQL by hand:

```
git grep -nE "f[\"'].*(SELECT|INSERT|UPDATE|DELETE)" -- "*.py"
```

This should print nothing.

### Record it

In `docs/week4/validation.md`, make one row for each rule you tested:

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| Email must be valid | Flask | curl with `email=not-an-email` | 400, nothing saved |
| Service must exist | Database | `INSERT ... service_id 999` in psql | `ERROR: violates foreign key constraint "tickets_service_id_fkey"` |

Include at least **three Flask rows** and **one row for every constraint type** in your schema (FOREIGN KEY, UNIQUE, CHECK, NOT NULL, RESTRICT), with the exact error message PostgreSQL gave.

**Checkpoint 10**

- [x] Form attributes match the column lengths and NOT NULL rules.
- [x] curl requests that skip the form return 400 and save nothing.
- [x] Every bad insert in psql fails, one for each constraint type in your schema.
- [x] The `git grep` check prints nothing.
- [x] `docs/week4/validation.md` has the results table.
- [x] Committed.

---

## Part 11: Prove it persists, report and submission

### 11a. The restart test

This is the test from the start of the activity, and it checks your data requirements such as NFR-01. Do it in order, and take a screenshot at each step marked 📷:

1. Create at least **five tickets** across at least two services. Call one, serve one, and let one person leave.
2. 📷 The staff dashboard, and the result of `SELECT id, status, service_id, created_at FROM tickets ORDER BY id;` in psql.
3. Stop Flask with Ctrl+C. Run `docker compose down`. Run `docker compose ps` and see that nothing is running.
4. Run `docker compose up -d`, wait until `docker compose ps` says **healthy**, then start Flask again.
5. 📷 The same dashboard and the same SQL query. Every ticket, status and time must be exactly as before.

Write the steps and put the screenshots in `docs/week4/persistence.md`.

### 11b. Rebuild from scratch

Your migrations should be able to rebuild the whole database on any computer, including your instructor's. Test it. **This deletes all your data**, so do it only after 11a:

```
docker compose down -v
docker compose up -d
flask --app app db upgrade
flask --app app seed
```

The app must open, show your services on the join form, and let you join. If it fails, a table or column is missing from your migrations (or you used `db.create_all()` somewhere). Fix it with a **new** migration and try again. Write the result in `persistence.md`.

Afterwards, `down -v` is no longer a habit: use plain `docker compose down` every day.

### 11c. Write your report in your repository

Write a short report in Markdown at `docs/week4/report.md` on your `feature/week4-database` branch, using the sections below. Put your screenshots in `docs/week4/screenshots/` and show them in the report with relative links, such as `![Dashboard after restart](screenshots/after-restart.png)`, so they display on GitHub.

Report sections, using `##` headings:

1. **Title details:** your app's name, setting, full name, student ID, section, date, and the **link to your pull request**
2. **Requirements:** how many functional and non-functional requirements you wrote, your MVP list, what the person from your setting said and what you changed, with a link to `docs/requirements.md`
3. **ERD:** the ERD image, the relationship sentences, and a link to `docs/week4/schema.md`
4. **Schema:** the output of `\d` for each table, in a code block
5. **Design decisions:** three decisions you made and why, each tied to your requirements or personas (for example *"I put `is_priority` on `tickets`, not `users`, because the registrar told me a student may use the priority lane on one visit and not the next."*)
6. **Self-review:** the main problems you found in your schema and what you changed (from `schema-review.md`)
7. **Migrations:** each migration in `migrations/versions/`, with one sentence on what it does
8. **CRUD:** one screenshot for each of create, read, update, soft delete and hard delete, each with the route that does it and the requirement ID it meets
9. **Validation:** a summary of `validation.md`, including the one PostgreSQL error you found most useful
10. **Persistence:** the before-and-after restart screenshots, and the result of the rebuild from scratch. Say whether NFR-01 (no ticket lost on restart) or your own equivalent passed.
11. **Reflection:** what was hardest this week, which requirement you found hardest to write in a testable way, and one report your staff persona would want from this data (for example *"how many people left before being served, per service, per day"*). You will write that query in Week 5.
12. **Declaration:** any AI tools or outside sources you used and what for. Write "None" if you used none.

If you used the local PostgreSQL fallback instead of Docker, say so in the title details.

Commit it: `git commit -m "Add Week 4 report (#<issue>)"`. Then open your branch on GitHub and check that every heading, table, code block and screenshot displays correctly.

### 11d. Open and merge your pull request, then submit the link

1. Push your branch: `git push -u origin feature/week4-database`
2. Open a pull request into `main`.
   - **Title:** `Week 4: PostgreSQL persistence for <YourApp>`
   - **Description:** `Closes #<issue>`, the requirement IDs covered, the ERD image, and the before-and-after restart screenshots.
3. Review your own diff on GitHub. Make sure there is **no `.env`**, no `.venv/` folder and no `__pycache__/`, and that `migrations/` **is** there.
4. **Merge** the pull request into `main`, then tag it:

   ```
   git switch main
   git pull origin main
   git tag week4
   git push origin week4
   ```

5. **Submit on MOLE.** In the **Week 4 assignment on MOLE**, submit the link to your report at the `week4` tag:

   ```
   https://github.com/<your-username>/<your-repo>/blob/week4/docs/week4/report.md
   ```

   Linking to the tag means your instructor sees exactly the version you submitted, even if you keep working on `main` afterward. Your repository must be **public**. Open the link in a private (incognito) browser window first: if it shows a 404 there, your repository is still private.

**Checkpoint 11 (submission)**

- [ ] `docs/week4/persistence.md` shows the restart test and the rebuild from scratch.
- [ ] Every requirement marked *This week* in `docs/requirements.md` works, and its status is updated to *Built (Week 4)*.
- [ ] `docs/week4/report.md` is in your repository and displays correctly on GitHub.
- [ ] Your pull request is **merged** into `main` and tagged `week4`.
- [ ] Your repository is public, and the report link opens in a private browser window.
- [ ] The link to your report at the `week4` tag is submitted to the **Week 4 assignment on MOLE** before the due date.

---

## Five mistakes to avoid this week

| Mistake | What happens | Fix |
| --- | --- | --- |
| Forgetting `db.session.commit()` | The page looks fine, but the data is gone after a reload | Commit after every change |
| SQL in f-strings | SQL injection: user input becomes code | Use ORM queries or bound parameters |
| Committing `.env` | Your password is published on GitHub | `.gitignore` plus `.env.example`; change a leaked password |
| `docker compose down -v` by habit | The volume is deleted with all your data | Use `docker compose down` |
| Editing an old migration | Databases on different computers drift apart | Write a new migration |

## What your repository should look like

```
your-repo/
├── app.py
├── models.py
├── compose.yaml
├── .env.example              # committed
├── .env                      # NOT committed (in .gitignore)
├── requirements.txt
├── README.md                 # your app's name, setting, how to run it (now with Docker)
├── .gitignore
├── migrations/
│   ├── env.py, alembic.ini, script.py.mako
│   └── versions/
│       ├── …_initial_tables.py
│       └── …_add_services_active.py
├── templates/
│   ├── base.html, index.html, join.html, ticket.html, staff.html
│   └── services.html
├── static/
│   ├── css/style.css
│   └── js/main.js
└── docs/
    ├── requirements.md       # living document, updated every week
    ├── week3/ …
    └── week4/
        ├── schema.md
        ├── erd.png
        ├── schema-review.md
        ├── validation.md
        ├── persistence.md
        ├── screenshots/
        └── report.md
```

Update your `README.md` so anyone can run your app from a fresh clone: copy `.env.example` to `.env`, `docker compose up -d`, `pip install -r requirements.txt`, `flask --app app db upgrade`, `flask --app app seed`, `flask --app app run --debug`.

## Rubric (100 points)

Each criterion is scored at one of four levels: **Exemplary** (100% of the points), **Proficient** (80%), **Developing** (60%), or **Beginning** (30% or less).

| Criterion | CLO | Points | Exemplary | Developing |
| --- | --- | --- | --- | --- |
| Requirements | 1 | 10 | At least 10 testable functional requirements (3 or more ★) and 4 measurable non-functional ones, each with an ID and priority; data requirements clearly marked; MVP and out-of-scope written; checked with a real person and changed in response | Vague or untestable; missing IDs, priorities or the data column; not checked with anyone |
| Schema design and ERD | 1 | 10 | At least three related tables traced to the requirements marked *Stores data*; every column typed and constrained with a reason; relationships labelled and read aloud; delete rules chosen; normalized to 3NF; no stored results | Tables not linked to requirements; missing keys or constraints; repeated data or a stored position |
| Schema self-review | 1 | 5 | Three or more entries in the required format, each tied to a review question; ERD updated | Vague or missing; no changes made or explained |
| Docker and configuration | 2 | 10 | `compose.yaml` with pinned image, named volume and healthcheck; password only in `.env`; `.env` ignored and `.env.example` committed | Database runs but password committed, image unpinned, or no `.env.example` |
| Models and relationships | 2 | 15 | Models match the ERD exactly, with typed columns, named constraints and `relationship()` on both sides; setting-specific fields placed correctly | Models missing tables or constraints, or do not match the ERD |
| Migrations and seed data | 2 | 10 | Both migrations committed and reviewed; downgrade and upgrade work; rebuild from scratch succeeds; seed is safe to run twice | Missing migration scripts, `create_all()` used, or rebuild fails |
| CRUD for your setting | 2 | 15 | Join, My place, dashboard, staff actions, soft delete, hard delete and Manage services all work against PostgreSQL with POST for changes; setting-specific table used; clearly built for your own setting | Only part of CRUD works, data still in Python lists, or GET routes change data |
| Validation in three layers | 2 | 10 | Browser, Flask and database layers all shown with curl and psql evidence; `IntegrityError` handled with rollback; no SQL in f-strings | Only one layer, or no evidence |
| Persistence proof | 2 | 5 | Before-and-after restart screenshots match exactly; rebuild from scratch documented | Restart test missing or data lost |
| GitHub workflow and report | 2 | 10 | Public repository; issue, branch, regular commits, merged PR with ERD and screenshots, `week4` tag; report complete in the repository and its link submitted | Single commit, unmerged PR, missing report, a private repository, or a broken link |
| **Total** | | **100** | | |

**Proficient** work is complete with minor gaps. **Beginning** work is missing, not working, or not your own.

## Spot-check demonstration

In a demonstration you may be asked to:

- run your app, join the queue, and do one staff action
- restart Docker and Flask and show that your data is still there
- explain one table in your ERD, one constraint, or one route in your code, and why you wrote it that way
- show where a requirement from `docs/requirements.md` is met in your app

**If your app will not run on the day** because of a technical problem (Docker will not start, no internet, a broken laptop) but you can explain your work, walk your instructor through your report, screenshots and code instead. You may also be given 24 hours to send a 2 to 3 minute screen recording of the app running. A technical problem alone does not lower your score, apart from the *Persistence proof* criterion if you cannot show it at all.

**If you cannot explain your own work**, such as what a table in your ERD is for, what a constraint prevents, or what a route does, each rubric criterion you could not explain is scored at **Beginning (30% or less)**, because the rubric treats work that is not your own as Beginning. You keep the points for the parts you can explain.

Prepare by making sure you can explain every table, constraint and route in your submission in your own words.

## Academic integrity

This is **individual work**. You may discuss ideas with classmates, but your requirements, ERD, schema, code, tests and report must be your own. The example requirements in this activity show the format; write your own for your setting. A schema or models copied from ClinicQ without changing them for your setting, or copied from a classmate, will be scored as Beginning. The code snippets in this activity are a starting point you are expected to adapt. Declare any AI tool or outside source you used in your report.

## Checklist before you submit

- [x] `docs/requirements.md` has my requirements with IDs, priorities and the *Stores data?* column, checked with one person from my setting.
- [x] `docs/week4/schema.md` and my ERD show at least three related tables for my own setting, with every key and constraint.
- [x] `schema-review.md` has my self-review, and my ERD is updated.
- [x] `docker compose up -d` starts PostgreSQL 17, and my password is only in `.env`, which Git ignores.
- [x] `models.py` matches my ERD, and both migrations are committed.
- [x] No `TICKETS` or `SERVICES` list is left; every screen reads and writes PostgreSQL.
- [x] Create, read, update, soft delete and hard delete all work, and every change is a POST.
- [x] `validation.md` shows bad data stopped by Flask (curl) and by the database (psql).
- [x] `persistence.md` shows my data surviving a restart, and the database rebuilding from my migrations.
- [x] My pull request is merged into `main` and tagged `week4`.
- [x] `docs/week4/report.md` is in my repository with my PR link at the top, and I submitted its `week4` link on MOLE.
- [x] I can explain every table, constraint and route in my submission, in case I am asked for a spot-check demonstration.