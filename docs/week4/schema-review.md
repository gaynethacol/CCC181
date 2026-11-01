# LicenseQ Schema Review

## 1. Applicant and service relationships

**Works well:** Each ticket references one applicant and one service using foreign keys. Applicant and service details are stored separately.

**Problem:** Deleting an applicant or service could leave tickets pointing to missing records, breaking referential integrity.

**Change:** Keep ON DELETE RESTRICT on both foreign keys. Deactivate services with existing tickets instead of deleting them.

## 2. Queue order after requeuing or transferring

**Works well:** created_at preserves the original joining time.

**Problem:** Ordering only by created_at would put transferred or requeued applicants ahead of people already waiting.

**Change:** Keep queued_at as a separate timestamp. Update it when transferring or requeuing, and order by queued_at followed by id.

## 3. Shared contact numbers

**Works well:** Each applicant has a generated primary key.

**Problem:** Making contact_number unique would prevent different applicants from using a shared family contact number.

**Change:** Keep contact_number non-unique. Validate its format and identify applicants using their primary keys.

## 4. Ticket status and queue position

**Works well:** The status column distinguishes waiting, called, served, no-show, and left.

**Problem:** A stored position would become outdated whenever someone leaves, transfers, or is called.

**Change:** Calculate position from earlier waiting tickets in the same service. Do not add a position column.

## Diagram decision

The existing schema and ERD already include these decisions.
No diagram changes are needed after this review.