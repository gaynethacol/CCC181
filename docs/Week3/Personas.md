## Emoy, the person waiting

Quote: Hassle kaayo ug dugay kaayo ang paghulat.

| | |
|---|---|
| **Photo or sketch** | 👤 |
| **Age, role and background** | 22-year-old student applying for a new driver’s license at LTO Tubod, Iligan City. *(interview)* |
| **Goals** | Complete his license application and receive his printed license card. |
| **Frustrations** | Describes the process as inconvenient and time-consuming. *(interview)* |
| **Devices and context** | Has a smartphone and mobile data. Waits outside the office because chairs are available there. *(interview)* |
| **Tech comfort** | No difficulty using apps was reported; comfort level needs confirmation. *(interview)* |
| **Accessibility needs** | Prefers Bisaya. No difficulty reading small text was reported. *(interview)* |

### Scenario

Emoy visits LTO Tubod to apply for a new driver’s license and waits outside where chairs are available. In the proposed workflow, he opens LicenseQ on his smartphone to obtain a queue ticket and check his position and status. After completing the application stage, he checks his ticket for printed-card collection. This scenario needs confirmation against his actual visit.

### Top tasks in the app

| Task | Screen | Requirement ID |
|---|---|---|
| Join the application queue and receive a ticket | Join | FR-01 |
| Check ticket status and position | My place | FR-02 |
| Check his queue stage after staff transfer him to card collection | My place | FR-02, FR-05 |

### What this means for my interface

1. Because Emoy checks the queue on a smartphone, my interface must fit a small screen without horizontal scrolling.
2. Because he finds the process time-consuming, my interface must make his ticket status and position easy to find.
3. Because he prefers Bisaya, my interface must use clear, familiar wording and test whether Bisaya labels improve his understanding.


## Alex, the staff member

Alex is a fictional name used to protect the interviewee’s identity.

Quote pending: Kung tawagon nako unya wala sila, ibutang nako sila sa pinakaluyo sa pila.

| | |
|---|---|
| **Photo or sketch** | 👤 |
| **Age, role and background** | 32-year-old front-desk employee who checks applicants’ documents and directs them to the next desk. *(interview)* |
| **Goals** | Check documents for correctness, return them to applicants, and explain where applicants should go next. *(interview)* |
| **Frustrations** | Reports no particular difficulty managing calls. Absent applicants are moved to the end of the queue. Other pain points need confirmation. *(interview)* |
| **Devices and context** | Uses a computer at the front desk. Reports that the office internet connection is good. *(interview)* |
| **Tech comfort** | Comfortable using web applications on a computer. *(interview)* |
| **Accessibility needs** | No specific interface difficulties were reported. *(interview)* |

### Scenario

An applicant arrives and submits their documents. Alex checks whether the documents are correct while the applicant waits to be called. Alex calls the applicant, returns the documents, and explains which desk to visit next, where the applicant waits for another call. If an applicant is absent when called, Alex moves them to the end of the queue. In the proposed workflow, Alex uses LicenseQ’s staff dashboard to view the waiting list, call applicants, and update their status.

### Top tasks in the app

| Task | Screen | Requirement ID |
|---|---|---|
| View each waiting list in order | Staff dashboard | FR-03 |
| Call an applicant and mark them as served or no-show | Staff dashboard | FR-04 |
| Transfer eligible applicants to printed-card collection | Staff dashboard | FR-05 |

### What this means for my interface

1. Because Alex checks documents while managing applicants, my interface must make queue actions easy to find and complete.
2. Because Alex directs applicants between stages, my interface must clearly label each queue and the applicant’s current stage.
3. Because absent applicants go to the end of the queue, my interface must provide an explicit requeue action that preserves the order of other waiting applicants.