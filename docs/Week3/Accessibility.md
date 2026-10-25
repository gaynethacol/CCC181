# LicenseQ Accessibility Check

## 1. Lighthouse

Tested using Chrome Lighthouse with Mobile and Accessibility selected.

| Screen | Final score | Screenshot |
|---|---|---|
| Join | 100 | [Join report](accessibility/join-lighthouse.png) |
| My place | 100 | [My place report](accessibility/my-place-lighthouse.png) |
| Staff | 100 | [Staff report](accessibility/staff-lighthouse.png) |

### Fixes made

- Changed outline-primary buttons to navy text and borders to address the Staff filter button’s contrast issue.
- Added a minimum size of 44 × 44 px to buttons and the navigation toggle.
- Set the flash-message close button to 44 × 44 px.

Lighthouse scores cover automated checks; keyboard and manual checks are recorded separately below.

## 2. Keyboard-only test

- ✅ Skip to main content appears on the first Tab.
- ✅ Keyboard focus is visible.
- ✅ Applicants can join the queue using only the keyboard.
- ✅ My place controls are reachable and usable.
- ✅ Staff can filter a queue, call an applicant, and mark them as served using only the keyboard.
- No keyboard failures were reported.

## 3. Manual checklist

✅ = passed through manual testing or code inspection.
N/A = the screen has no applicable input or status.

| Check | Join | My place | Staff |
|---|---|---|---|
| Every input has a visible label | ✅ | N/A | ✅ |
| Error messages say what to do, in text | ✅ | ✅ Action feedback | ✅ Action feedback |
| Status is shown in words, not only color | N/A | ✅ | ✅ |
| Text and buttons are readable at 375 px with no sideways page scroll | ✅ | ✅ | ✅ Table scrolls inside its box |
| Buttons are at least about 44 × 44 px on a phone | Pending final size check | Pending final size check | Pending final size check |
| Page has one h1 and headings in order | ✅ | ✅ | ✅ |
| HTML language is set to English | ✅ | ✅ | ✅ |

### Remaining verification

Check the rendered button sizes after the CSS changes and confirm that the larger controls still fit at 375 px. Replace the pending entries with ✅ once verified.