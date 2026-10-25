# LicenseQ Usability Walkthrough

This walkthrough simulates a participant’s reactions based on the supplied interface. No app interaction or task timing was measured.

## Participant and setup

- Participant: ChatGPT role-playing a student applying for a new license
- Device context: Laptop using Chrome
- Method: Simulated walkthrough
- Recording: None

## Task reactions

| Task | Simulated response | Potential hesitation |
|---|---|---|
| Join Application and Testing | “I enter my name and contact number, select Application and Testing, and click Get a ticket.” | Understanding which queue to select. |
| Identify ticket number and people ahead | “The large ticket number is easy to notice. The people-ahead sentence explains my position.” | Distinguishing “You’re next” from being called. |
| Call the next applicant and mark them served | “I open Staff, click Call next, and look for Serve after the ticket changes to Called.” | Distinguishing Serve from Transfer to card collection. |

## Persona-rule findings

- The prominent ticket number and position support quick recognition.
- Short explanations could make queue choices easier to understand.
- Staff actions are visible, but Serve and Transfer could use clearer descriptions.

## Implemented improvement

- **Problem:** Lighthouse flagged insufficient contrast on the Staff filter button. The initial Accessibility score was 96.
- **Fix:** Changed outline-primary buttons to navy text and borders against the cream background.
- **Result:** The final Staff Accessibility score was 100.

### Before

![Staff before the contrast fix](screenshots/staff-before.png)

### After

![Staff after the contrast fix](screenshots/staff-after.png)