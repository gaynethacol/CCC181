# LicenseQ Requirements

**Setting:** Driver’s licensing queues at LTO Tubod, Iligan City.

**People who wait:** Driver’s license applicants, represented by Emoy in [Week 3 personas](Week3/personas.md).

**People who serve:** Front-desk employees, represented by Alex in [Week 3 personas](Week3/personas.md).

**Problem statement:** Driver’s license applicants need clear information about their turn and queue stage because long waits and reliance on name calls make progress uncertain. Staff need organized waiting lists that remain accurate after the server restarts.

## Functional requirements

Existing Week 3 requirement IDs are preserved. A requirement marked “Stores data: Yes” depends on information that must survive a restart, even when the displayed result is computed.

★ identifies requirements specific to the licensing setting.

| ID | Requirement | Priority | Stores data? | Status |
|---|---|---|---|---|
| FR-01 | An applicant can join a queue using their name and contact number and receive a ticket. | Must | Yes | Built (Week 3) |
| FR-02 | An applicant can view their ticket number, queue stage, status, and number of waiting applicants ahead. | Must | Yes | Built (Week 3) |
| FR-03 ★ | A front-desk employee can view separate, ordered waiting lists for application/testing and printed-card collection. | Must | Yes | Built (Week 3) |
| FR-04 | A front-desk employee can call the next waiting applicant and mark a called ticket as served or no-show. | Must | Yes | Built (Week 3) |
| FR-05 ★ | A front-desk employee can transfer a called application-stage ticket to the end of the printed-card collection queue after confirming eligibility. | Must | Yes | Built (Week 3) |
| FR-06 | An office supervisor can review recorded queue changes and reasons for changes in order. | Should | Yes | Later |
| FR-07 | An applicant can view an estimated waiting time based on recorded service durations. | Could | Yes | Later |
| FR-08 | An applicant can receive an SMS notification when their turn approaches. | Won't (this semester) | Yes | Later |
| FR-09 | An applicant can reopen an existing ticket after Flask or PostgreSQL restarts and see its saved details. | Must | Yes | This week |
| FR-10 | A staff member can create a service with a unique name and a positive average service duration. | Must | Yes | This week |
| FR-11 | A staff member can edit a service’s name and average service duration. | Must | Yes | This week |
| FR-12 | A staff member can switch a service off so applicants cannot join it, while preserving its existing tickets. | Must | Yes | This week |
| FR-13 | A staff member can delete a service only when no tickets reference it. | Must | Yes | This week |
| FR-14 | An applicant can leave a waiting queue, with the ticket retained under the status left. | Must | Yes | This week |
| FR-15 | A staff member can permanently delete a mistaken ticket after confirmation. | Must | Yes | This week |
| FR-16 ★ | A front-desk employee can move a called but absent applicant to the end of their current licensing queue after confirmation. | Must | Yes | Built (Week 3) |
| FR-17 | An applicant can see when their ticket was created, displayed in Philippine time. | Should | Yes | This week |

The persistence work applies to all existing ticket and service functions, including those marked Built (Week 3).

FR-02 uses stored ticket records to compute queue position. Position itself will not be stored.

FR-14 changes the Week 3 leave action from no-show to left so voluntary departures can be distinguished from missed calls.

## Non-functional requirements

Existing Week 1 requirement IDs are retained.

| ID | Requirement | Category | Priority |
|---|---|---|---|
| NFR-01 | With 100 active tickets during a local test, at least 95% of ticket-creation and queue-page requests complete within 2 seconds. | Performance | Should |
| NFR-02 | At least four of five first-time test users can join a queue and find their ticket status within 2 minutes without assistance. | Usability | Should |
| NFR-03 | Public queue lists do not display names or contact numbers. Staff queue-management actions require staff authentication before real deployment; authentication is deferred to Week 11. | Security/privacy | Must |
| NFR-04 | Join, My place, and Staff work at widths of 360 px and 1366 px in Chrome and Edge without sideways page scrolling; the Staff table may scroll inside its container. | Compatibility | Must |
| NFR-05 | Tickets retain their identifiers, service, status, and timestamps after Flask and PostgreSQL are stopped and restarted without deleting the database volume. | Reliability | Must |
| NFR-06 | Concurrent ticket submissions receive distinct database-generated ticket identifiers. | Data integrity | Must |
| NFR-07 | Join, My place, and Staff each score at least 90 in Chrome Lighthouse Accessibility testing. | Accessibility | Must |
| NFR-08 | No real database password or production secret is committed to Git. Configuration uses an ignored .env file and a committed .env.example with placeholders. | Security | Must |
| NFR-09 | Every status-changing or deletion action uses POST; GET requests do not modify queue records. | Data integrity | Must |

## Minimum viable product

**Functional requirements:** FR-01, FR-02, FR-03, FR-04, FR-05, FR-09, FR-10, FR-11, FR-12, FR-13, FR-14, FR-15, and FR-16.

The MVP lets applicants join and follow the two licensing queues while staff manage ticket outcomes and services. Database persistence preserves those records after restarts.

Staff authentication remains a deployment requirement scheduled for Week 11. The current classroom prototype uses fictional data.

**Week 4 scope:** Persist the existing queue functions; implement FR-09 through FR-17 except features explicitly marked Later; satisfy and test the applicable data, accessibility, compatibility, and configuration requirements.

## Out of scope this semester

- SMS notifications, because messaging costs and provider integration are outside the project scope.
- Official LTO system integration, payments, examinations, biometrics, photo capture, and license printing, because these require authorization or equipment beyond this queue-management prototype.

## Requirements validation

| Review question | Feedback |
|---|---|
| Is anything missing? | No missing functions were identified. |
| Is anything wrong or unnecessary? | No changes were suggested; the requirements looked appropriate. |
| Which functions matter most? | Joining the queue and receiving a ticket (FR-01). |

No requirements were changed after this review. The reviewer identified two priorities rather than three, both covered by FR-01.