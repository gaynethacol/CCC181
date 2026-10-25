# LicenseQ Wireframe Self-Review

## 1. Join — Phone
Persona: Emoy | Requirement: FR-01

1. **Clear within five seconds?** Likely yes. The heading, labeled fields, and Join queue button show what to do.
2. **Status visible?** Not applicable before ticket creation. Submission should lead directly to My place.
3. **Familiar wording?** Most labels are straightforward, but “eligible applicants” needs explanation. Confirm whether Emoy understands the English wording.
4. **Frequent staff action reachable?** Not applicable. The applicant’s Join queue button is directly below the fields.
5. **Important information first?** Yes. The heading and required fields appear first, but brief instructions are missing.
6. **Persona rules followed or broken?** Follows the smartphone-layout rule with stacked fields. Partly breaks the familiar-wording rule because eligibility is unclear.

**Works well:** A short, vertically stacked form suits Emoy’s smartphone.

**Problem:** The eligibility note does not explain when to select card collection. This affects error prevention.

**Change:** Add: “For card collection, select this only after staff confirm you are ready.”

## 2. Join — Laptop
Persona: Emoy | Requirement: FR-01

1. **Clear within five seconds?** Likely yes. The form and adjacent instructions explain the main action.
2. **Status visible?** Not applicable before ticket creation. Submission should open My place.
3. **Familiar wording?** The instructions are simple, but the card-collection eligibility note needs clarification.
4. **Frequent staff action reachable?** Not applicable. Join queue is clearly placed below the inputs.
5. **Does the phone equivalent prioritize correctly?** Yes, but it should include the same essential instructions.
6. **Persona rules followed or broken?** Follows the rule for a short, understandable process. Partly breaks familiar wording through the unexplained eligibility term.

**Works well:** Instructions beside the form reduce the need to remember the steps.

**Problem:** The laptop provides guidance that the phone does not. This affects consistency.

**Change:** Keep the side-by-side layout and use the same essential instructions and eligibility explanation on both devices.

## 3. My place — Phone
Persona: Emoy | Requirement: FR-02

1. **Clear within five seconds?** Likely yes. Ticket number and position are immediately noticeable.
2. **Status visible?** Yes, but it is less prominent than the ticket number and position.
3. **Familiar wording?** “2 people ahead” is clear. A Called status should include the actual desk destination.
4. **Frequent staff action reachable?** Not applicable. Refresh status is visible below the ticket details.
5. **Important information first?** Yes. Ticket number and position appear first, but status should join them.
6. **Persona rules followed or broken?** Follows the smartphone and prominent-ticket rules. Partly breaks quick status recognition because status is separated from the main panel.

**Works well:** Large ticket and position text help Emoy check his place quickly.

**Problem:** Emoy could overlook a change to Called. This affects visibility of system status.

**Change:** Put status inside the main ticket panel and add a Called example with a clear destination. Show when information was last updated.

## 4. My place — Laptop
Persona: Emoy | Requirement: FR-02

1. **Clear within five seconds?** Likely yes. The large ticket panel clearly communicates queue position.
2. **Status visible?** Yes, in the right panel, but it is visually separated from the ticket number.
3. **Familiar wording?** Position and Waiting are understandable. Confirm the office’s preferred wording for the destination desk.
4. **Frequent staff action reachable?** Not applicable. Refresh status is easy to locate in the details panel.
5. **Does the phone equivalent prioritize correctly?** Yes. Both prioritize ticket number and position, but status needs more emphasis.
6. **Persona rules followed or broken?** Follows the prominent-ticket rule. Partly breaks easy status recognition by separating status from the main information.

**Works well:** The two-column layout makes good use of laptop space.

**Problem:** The screen gives no indication of how recent the displayed information is. This affects visibility of system status.

**Change:** Add a last-updated label and move status beside the ticket number. Keep the two-column layout for supporting details.

## 5. Staff dashboard — Phone
Persona: Alex | Requirements: FR-03, FR-04, FR-05

1. **Clear within five seconds?** Likely yes. The queue selector and Call next button clearly indicate the main task.
2. **Status visible?** Waiting-list statuses are shown, but the current ticket’s status is missing.
3. **Familiar wording?** Call next is clear. “No-show / Move to end” should state the action more directly.
4. **Frequent staff action reachable?** Yes. Call next is near the top and spans most of the available width.
5. **Important information first?** Yes. The selected queue, main action, and current ticket appear before the waiting list.
6. **Persona rules followed or broken?** Follows easy-to-find actions and clear queue-stage rules. Partly breaks explicit requeue behavior because the action lacks confirmation.

**Works well:** Stacked controls keep staff actions accessible on a narrow screen.

**Problem:** The combined no-show and requeue label may cause uncertainty about what happens after tapping it. This affects error prevention.

**Change:** Rename it “Absent — move to end” and confirm the affected ticket before applying the action. Display the current ticket’s status.

## 6. Staff dashboard — Laptop
Persona: Alex | Requirements: FR-03, FR-04, FR-05

1. **Clear within five seconds?** Likely yes. The waiting-list table and action panel clearly separate information from controls.
2. **Status visible?** Waiting-list statuses are visible, but the current ticket needs an explicit status.
3. **Familiar wording?** Most labels match the described tasks. Use the same clearer requeue wording as the phone.
4. **Frequent staff action reachable?** Yes. Call next is prominently placed at the top of the action panel.
5. **Does the phone equivalent prioritize correctly?** Yes. It retains queue selection and current-ticket actions before the waiting list.
6. **Persona rules followed or broken?** Follows the rules for visible actions and distinct queue stages. Partly breaks error prevention because ticket-changing actions lack explicit confirmation.

**Works well:** Alex can view the waiting list and current-ticket controls together.

**Problem:** Calling another applicant or transferring the current ticket without resolving its state could create confusion. This affects error prevention.

**Change:** Show the current status, disable Call next until the current applicant is resolved, and confirm eligibility before transfer. Use the same requeue confirmation as the phone.