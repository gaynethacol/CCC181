# LicenseQ — Week 3 Report

## 1. Title details

| Detail | Information |
|---|---|
| Application | LicenseQ |
| Setting | Driver’s licensing queues at LTO Tubod, Iligan City |
| Student | Gayneth A. Acol |
| Student ID | 2024-1992 |
| Section | CS3A |
| Report date | October 26, 2026 |
| GitHub issue | [Issue #1](https://github.com/gaynethacol/CCC181Activity/issues/1) |
| Pull request | Pending — add the actual pull request URL after creating it |

LicenseQ is a student prototype with separate queues for application and testing, and printed-card collection. It is not connected to official LTO systems.

## 2. Personas

### Emoy — Applicant

Emoy is a 22-year-old student applying for a new driver’s license. He has a smartphone and mobile data, prefers Bisaya, and waits outside the office where chairs are available.

- Interview summary: He finds the process inconvenient and time-consuming.
- Exact interview quote: Pending confirmation.
- Top tasks: Join the appropriate queue, check his ticket number and position, and follow his queue stage.

### Alex — Front-desk employee

Alex is a fictional name for the 32-year-old employee described in the research. The employee checks documents, calls applicants, returns their documents, and explains which desk to visit next. The employee uses a computer and reports being comfortable using web applications.

- Interview summary: Absent applicants are moved to the end of the queue.
- Exact interview quote: Pending confirmation.
- Top tasks: View the waiting lists, call applicants, record outcomes, and move applicants between queue stages.

Full profiles: [Personas](personas.md).

## 3. Screens

### Join — Phone

Emoy enters his name and contact number and chooses a queue on a phone. Covers FR-01.

![Join on a phone](screenshots/join-phone.png)

### Join — Laptop

Emoy completes the same ticket-registration task using a laptop. Covers FR-01.

![Join on a laptop](screenshots/join-laptop.png)

### My place — Phone

Emoy checks his ticket number, queue, status, and position on a small screen. Covers FR-02.

![My place on a phone](screenshots/my-place-phone.png)

### My place — Laptop

Emoy views the same queue information on a laptop, with automatic status updates. Covers FR-02.

![My place on a laptop](screenshots/my-place-laptop.png)

### Staff — Phone

Alex filters queues and accesses ticket actions using a horizontally scrollable table. Covers FR-03, FR-04, and FR-05.

![Staff on a phone](screenshots/staff-phone.png)

### Staff — Laptop

Alex views the ordered waiting list, calls applicants, records outcomes, and transfers eligible applicants to card collection. Covers FR-03, FR-04, and FR-05.

![Staff on a laptop](screenshots/staff-laptop.png)

## 4. Design decisions

1. **Prominent ticket information:** My place displays the ticket number and position prominently because applicants need to recognize their place quickly while waiting.

2. **Separate queue stages:** Application and Testing and Printed-Card Collection are labeled separately to reflect the two-stage process described in the research.

3. **Visible staff actions:** Call next appears above the waiting list because calling applicants is a frequent staff task. Transfer and move-to-end actions require confirmation to reduce accidental queue changes.

## 5. Self-review

The wireframe review identified unclear card-collection eligibility wording, insufficient emphasis on ticket status, and uncertainty about staff actions.

The implementation includes guidance about card collection, status badges with text, and confirmation before requeuing or transferring applicants. My place also updates automatically and provides a manual Refresh status option.

The applicant eligibility checkbox was removed during development. The form retains guidance, while staff confirm eligibility when transferring a ticket.

Review notes: [Self-review](feedback.md).

## 6. Accessibility

Chrome Lighthouse Accessibility testing produced the following final scores:

| Screen | Final score |
|---|---|
| Join | 100 |
| My place | 100 |
| Staff | 100 |

The initial Staff score was 96 because the Filter button had insufficient color contrast. Changing outline-primary buttons to navy text and borders improved the final score to 100.

Keyboard testing confirmed that the skip link appears, focus is visible, and the main applicant and staff tasks can be completed without a mouse. Phone-width checks were performed at 375 px.

CSS minimum dimensions of 44 × 44 px were added to buttons, the menu toggle, and flash-message close buttons. Final rendered-size verification should be recorded in the accessibility checklist.

These Lighthouse scores describe automated checks and do not establish complete accessibility.

Detailed results: [Accessibility check](accessibility.md).

## 7. Usability test and improvement

Emoy provided feedback on the applicant experience and completed the staff task without assistance. Completion times were not recorded.

| Task | Recorded result | Feedback |
|---|---|---|
| Join Application and Testing | Reported no difficulty; confirm completion in the test notes | Found the interface easy to understand and navigate. |
| Identify ticket number and people ahead | Completion needs confirmation in the test notes | Asked how long the wait would be when one person was ahead. |
| Call the next applicant and mark them served | Completed without help | No separate staff-task comment was recorded. |

Emoy appreciated being able to check the number of people ahead without remaining seated inside the building. However, queue position does not guarantee a waiting time or prevent a missed turn. Applicants should remain nearby because the prototype does not send notifications.

### Implemented improvement

The Staff Filter button’s contrast was improved after the accessibility check.

**Before:** Staff Lighthouse Accessibility score of 96.

![Staff before the contrast fix](screenshots/staff-before.png)

**After:** Staff Lighthouse Accessibility score of 100.

![Staff after the contrast fix](screenshots/staff-after.png)

Detailed notes: [Usability test](usability-test.md).

## 8. Reflection

A major challenge during development was keeping Flask routes, Jinja templates, and JavaScript consistent. Errors occurred when a template referred to a route that had not yet been added or when the old placeholder template was still being displayed.

The current Python list loses its tickets when the server restarts. In Week 4, PostgreSQL should preserve ticket records and queue order. The interface should continue to distinguish ticket number from queue position, and it should provide clear feedback when data cannot be loaded or updated.

The participant’s waiting-time question also suggests a future improvement. Estimated waiting times should be considered only after sufficient service-duration data is available.

## 9. Declaration

I used ChatGPT to help draft and revise documentation, generate a wireframe reference image, explain Flask and Git errors, and develop Flask, Jinja, Bootstrap, and JavaScript code. ChatGPT also helped interpret accessibility findings and suggested fixes.

An earlier simulated walkthrough was used as practice material, not as evidence of participant behavior. The participant feedback recorded in this report comes from the feedback supplied during the actual testing discussion.

I adapted the instructor’s CCC181 Week 2 starter and Week 3 activity examples:

- https://github.com/jjmmontemayor/ccc181-1s-2026/tree/main/lecture/demo/my-app

Bootstrap 5.3.3 is loaded through jsDelivr.