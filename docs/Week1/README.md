# Proposed Application: [Application Name]

| | |
|---|---|
| **Student name** | [Acol, Gayneth] |
| **Section** | [CS3A] |
| **GitHub username** | [gaynethacol] |
| **Date submitted** | [YYYY-MM-DD] |

---

## 1. Problem Statement

Applicants at a driver’s licensing office need a clear way to know their turn and track their progress through the application and printed-card collection queues. Without clear queue information, they may be unsure where to wait or when they will be called. Staff also need an organized way to manage both queues and direct applicants to the correct stage.

### 1.1 Background

This problem occurs at the Land Transportation Office (LTO) in Tubod, Iligan City, where applicants wait during the driver’s licensing process. Based on the process I encountered, applicants queue for application activities, including forms, the driving test, and ID photo capture, and later queue to collect their printed plastic cards. Applicants need clear information about their turn and which queue to follow. I became aware of this problem through my experience with the licensing process at this office.

### 1.2 Evidence from research

| Method | Who / where | Key finding |
|---|---|---|
| Interview | My brother, referred to as “Emoy” | Described the licensing process as inconvenient and time-consuming. |
| Interview | Front-desk employee | Not yet conducted. Staff procedures and challenges still need confirmation. |
| Observation | Personal visit to LTO Tubod, Iligan City, approximately six months ago | Observed a crowded waiting area with insufficient seating. Some applicants left because they were tired of waiting. Estimated waiting time was approximately 4–5 hours. |
| Personal experience | Queue process at LTO Tubod | After submitting documents, applicants waited for their names to be called. Instructions about the next step were given when documents were returned, followed by another wait. Names were called twice before absent applicants were skipped. |
| Document review | Not conducted | No forms, written queue instructions, or queue policies were reviewed. |1

### 1.3 Point-of-view (POV) statement

**Driver’s license applicants at LTO Tubod, Iligan City** need **clear information about their turn and the next queue stage** because **long waits and reliance on name calls make it difficult to know their progress and avoid missing their turn**.

### 1.4 "How might we…?" question

How might we help driver’s license applicants at LTO Tubod, Iligan City, understand their queue progress and next steps so they are less likely to miss their turn?

### 1.5 Self-check

- [x] Names a real user group
- [x] States a need, not a feature
- [x] Rests on an insight from research
- [x] Is narrow enough to act on and open enough to allow different ideas

---

## 2. Target-User Profile

### 2.1 Primary persona

Based on an interview with my brother, using the pseudonym “Emoy.”

| | |
|---|---|
| **Name, age** | Emoy, 22 |
| **Role / background** | Student applying for a new driver’s license at LTO Tubod, Iligan City. |
| **Goals** | Complete the licensing process and collect his printed license card. |
| **Frustrations / pain points** | Finds the process inconvenient and time-consuming. |
| **Context of use** | Has a smartphone and mobile data. Waits outside the office, where chairs are available. |
| **Accessibility considerations** | Prefers Bisaya. No difficulty reading small text or using apps was reported. |
| **Current workaround** | Stays outside the office and listens for his name to be called. |

### 2.2 User groups and stakeholders

| Group | Who | Relationship to the app |
|---|---|---|
| Primary users | Driver’s license applicants at LTO Tubod, Iligan City | Join the queue and check their ticket number, status, and position during application processing and printed-card collection. |
| Secondary users | Front-desk employees | Manage both waiting lists, call applicants, mark completed transactions, and record no-shows. |
| Stakeholders | Office supervisor or designated administrator, subject to confirmation | Oversee queue procedures, approve system use, and coordinate maintenance. |

### 2.3 Organizational needs

- Maintain organized queues for application processing and printed-card collection, with clear procedures for calling applicants and handling missed turns.
- Reduce uncertainty and repeated inquiries by allowing applicants to check their queue status.
- Support queue fairness by recording entry order and staff actions. Any authorized changes to the order should include a recorded reason to help address concerns about unauthorized queue insertion.
- Limit applicant information collected by the queue app to name and contact number. Computer-based examinations, biometrics, and ID photo capture remain outside the app’s scope. Public queue views should display ticket numbers rather than personal details.
- Keep costs manageable by designing the system for existing office computers. Internet availability and permission to use office equipment still need confirmation.
- Balance applicants’ need for clear updates with staff’s need to keep the line moving. Display queue position and status without promising an exact waiting time, and establish a clear procedure for applicants who miss their turn.

## 3. Proposed Application
LicenseQ

### 3.1 Concept

LicenseQ is a proposed queue management system for LTO Tubod, Iligan City, covering application processing and printed-card collection. Applicants provide their name and contact number to receive a ticket and check their queue stage, status, and position. Front-desk employees use a dashboard to call applicants, mark them as served or absent, and move eligible applicants to the card-collection queue. The system records queue order and staff actions to support transparency and help address concerns about unauthorized queue insertion. It manages waiting lists; examinations, forms, biometrics, photo capture, and license printing remain part of the office’s existing procedures.

### 3.2 Value proposition

For driver’s license applicants at LTO Tubod, Iligan City who need to know their turn and follow the licensing queues, LicenseQ is a queue management system that shows their ticket number, queue position, and status. Unlike relying only on staff calling names, it lets applicants check their place in both the application and printed-card collection queues while helping staff maintain an organized waiting list.

### 3.3 Value Proposition Canvas

| User side | Product side |
|---|---|
| **Jobs: Complete application processing and collect the printed license card while following the correct queue.** [ ] | **Features: Separate queues for application processing and card collection, digital tickets, and a staff dashboard.** [ ] |
| **Pains: Long waits, uncertainty about turns, missed name calls, and concerns about unauthorized queue insertion.** [ ] | **Pain relievers: Visible queue position and status, recorded queue order, and staff controls for calls and no-shows.** [ ] |
| **Gains: Clearer information about turns, less uncertainty, and greater confidence in queue fairness.** [ ] | **Gain creators: A personal ticket page and an ordered waiting list with recorded reasons for authorized queue changes.** [ ] |
### 3.4 Existing applications (from your application analysis)

| Existing app | What it does well | Where it falls short | How your app differs |
|---|---|---|---|
| LicenseQ Week 2 starter | Demonstrates Flask pages, ticket display, and a reusable page layout. | It is a classroom starter and does not provide the two-stage licensing workflow needed for this project. | LicenseQ will support application and printed-card collection queues, applicant queue-position tracking, and staff controls for calling, serving, and marking no-shows. |

### 3.5 Technology choice

**Options considered:** A responsive Flask web application, a native mobile application, and an AI-assisted queue application.

**Weighted decision matrix** (scores 1–5, higher is better):

These scores are preliminary estimates based on the project’s requirements, current learning stage, and semester timeline. Each total applies the weights shown in the headings.

| Option | Solves the problem ×3 | Team skills ×2 | Cost ×2 | Privacy ×2 | Time to MVP ×1 | Total /50 |
|---|---|---|---|---|---|---|
| Responsive Flask web application | 5 | 4 | 5 | 4 | 5 | 46 |
| Native mobile application | 5 | 2 | 3 | 4 | 2 | 35 |
| AI-assisted queue application | 3 | 1 | 2 | 2 | 1 | 19 |

**Chosen technology and rationale:** LicenseQ will begin as a responsive web application using Flask, Jinja, and Bootstrap. Applicants and staff can access it through a browser on a phone or computer without installing an application. This approach builds on the Week 2 starter and supports ticket creation, queue-position tracking, and staff queue management. Tickets will initially use a Python list, followed by PostgreSQL in Week 4 and a REST API in Week 6 to support the Flutter application from Week 8. No emerging technology is needed because the core problem requires clear queue information and organized staff controls.

---

## 4. Preliminary Requirements

### 4.1 Functional requirements (user stories)

| ID | User story | Priority (MoSCoW) |
|---|---|---|
| FR-01 | As an applicant, I want to join the appropriate queue using my name and contact number so that I receive a ticket. | Must |
| FR-02 | As an applicant, I want to view my ticket number, queue stage, status, and position so that I know my place in line. | Must |
| FR-03 | As a front-desk employee, I want to view each queue separately and in order so that I can manage applicants correctly. | Must |
| FR-04 | As a front-desk employee, I want to call applicants and mark them as served or no-show so that the waiting list stays updated. | Must |
| FR-05 | As a front-desk employee, I want to move eligible applicants to the printed-card collection queue so that they can proceed to the next stage. | Must |
| FR-06 | As an office supervisor, I want a record of queue changes and reasons for changes in order so that I can review concerns about unfair queue handling. | Should |
| FR-07 | As an applicant, I want an estimated waiting time so that I can plan my time. | Could |
| FR-08 | As an applicant, I want an SMS notification when my turn is approaching so that I am less likely to miss it. | Won't (this time) |

### 4.2 Non-functional requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Performance | With up to 100 active tickets in a local test, ticket creation and queue-page requests must complete within 2 seconds in at least 95% of requests. |
| NFR-02 | Usability | In a test with five first-time users, at least four must join the queue and locate their ticket status within 2 minutes without assistance. |
| NFR-03 | Security / privacy | Public queue lists must display ticket numbers without names or contact numbers. All staff queue-management actions must reject requests from users who are not authenticated as staff. |
| NFR-04 | Compatibility | The join form, ticket page, and staff dashboard must work without horizontal page scrolling at viewport widths of 360 px and 1366 px in Chrome and Edge. |

### 4.3 MoSCoW summary

- **Must have:** Queue registration and ticket creation; ticket status and position tracking; separate application and card-collection waiting lists; staff controls to call, serve, and mark no-shows; transfer of eligible applicants to the card-collection queue.
- **Should have:** A record of queue changes, including reasons for changes in order.
- **Could have:** Estimated waiting time.
- **Won't have (this time):** SMS notifications.

## 5. Minimum Viable Product (MVP)

The MVP of LicenseQ will help applicants at LTO Tubod, Iligan City, join a queue and check their ticket status and position. Front-desk employees will manage separate queues for application processing and printed-card collection, call applicants, mark them as served or no-show, and transfer eligible applicants to the card-collection queue. This is the core scope planned for completion this semester.

### 5.1 MVP features

1. **Join the queue:** Applicants enter their name and contact number to receive a ticket for the appropriate queue.
2. **My place:** Applicants view their ticket number, queue stage, status, and position.
3. **Staff dashboard:** Front-desk employees view both queues in order, call applicants, mark them as served or no-show, and transfer eligible applicants to the printed-card collection queue.
### 5.2 Out of scope

- **SMS notifications:** Excluded from the MVP to avoid messaging costs and additional integration work.
- **Estimated waiting time:** Deferred until enough service-duration data is available to produce useful estimates.
- **Examinations, biometrics, and ID photo capture:** Handled through the office’s existing procedures; LicenseQ only manages queues.
- **License printing, payments, and official LTO system integration:** Excluded because these require equipment, authorization, or access beyond this student project.

### 5.3 Constraints and assumptions

- **Constraints:** Development must be completed within one semester by a student developer with limited time and budget. The project follows the course technologies: Flask, Jinja, Bootstrap, PostgreSQL, a REST API, and later Flutter. Access to official LTO systems and permission for deployment have not been obtained, so testing will use sample data.
- **Assumptions:** Applicants have access to a smartphone and an internet connection, or can receive assistance from front-desk staff. Staff have access to an internet-connected computer and can update ticket statuses consistently. The office will confirm queue-transfer rules and procedures for missed turns before any real deployment.

### 5.4 Feasibility check (TELOS)


| Dimension | Key question | Your assessment |
|---|---|---|
| Technical | Can I build it with my skills and tools? | Feasible using the course starter and technologies, with features developed gradually through the semester. |
| Economic | Do the benefits justify the costs? | A classroom prototype can use existing equipment and free development tools. Actual hosting, maintenance costs, and benefits must be evaluated before deployment. |
| Legal | Does it comply with law and policy (e.g., RA 10173)? | Compliance has not yet been established. Testing will use sample data; real deployment requires office authorization and review of privacy practices and applicable policies. |
| Operational | Will people use it, and can it be run? | Potentially feasible if applicants and front-desk employees find it usable. Staff participation, internet availability, and procedures for missed turns and queue transfers need confirmation. |
| Schedule | Can I deliver the MVP this semester? | Feasible if development stays focused on the three core screens and required queue-management functions. |

**Verdict:** Feasible as a student prototype within one semester. Real deployment depends on office approval, user validation, available equipment and connectivity, and privacy review.

---

## Submission Checklist

- [ ] File saved as `activities/proposed-application/README.md` in my CCC181 repository
- [ ] All `[bracketed placeholders]` replaced and guidance blockquotes removed
- [ ] Sections 1–5 complete
- [ ] Images (if any) placed in `images/` and displaying correctly on GitHub