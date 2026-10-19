# 26D impact ratings: editorial review (19 Oct 2026)

Scope: all 37 tracked 26D changes the automatic first pass rated high (Oracle "Larger scale"), plus a quick scan of the 62 rated medium. Each was checked against its Oracle 26D What's New feature page, fetched fresh on 19 Oct 2026 (description, Steps to enable and configure, Tips and considerations, Access requirements), and for Risk Management (Redwood) Oracle's Introduction page in that book.

Rules: the same as the 26C/26B pass (review/2026-10-17-ratings-review.md). High: users must change how they work; large-scale UI or process change; an opt-in ending, or a former opt-in now standard, that affects users; or touches payments, postings, integrations or security. Medium: visible but contained, or automatic but noticeable. Low: minor, cosmetic, reporting-only, or needs setup that nobody gets by default. Precedents from the 26C pass were followed (payroll setup pages and read-only payroll tabs medium; AI agents that must be set up low; statutory pay changes and automatic absence changes high).

Overrides are in data/editorial.json (keyed by Oracle URL) and applied by scripts/build.py after the automatic pass, so the weekly refresh keeps them. Only ratings changed; no summaries or enablement labels were edited.

## Totals

- Ratings changed: 40 (high → low: 19, high → medium: 13, medium → low: 8). Promoted: 0.
- Before: high 37, medium 62, low 37. After: high 5, medium 67, low 64.
- High kept: 5.

## Items

### Payables Period Close Workspace (Financials)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: None
- Reason: A new agentic workspace for the Payables close; users need its Manage or View Payables Period Close Workspace privilege, and the existing close steps don't change. Visible but contained, as with the 26C Cash Processing Agent.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/erp/26d/fins26d/26D-fin-wn-f51249.htm

### Define reusable Algorithm Filters (Risk Management (Redwood))
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Risk Management (Redwood) needs a service request to Oracle to get set up (Oracle's introduction), and access comes through the Risk Management roles and record stakeholders; nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/erp/26d/rrsk26d/26D-rrsk-wn-f51114.htm

### Define reusable User-Defined Access Paths (Risk Management (Redwood))
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Risk Management (Redwood) needs a service request to Oracle to get set up (Oracle's introduction), and access comes through the Risk Management roles and record stakeholders; nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/erp/26d/rrsk26d/26D-rrsk-wn-f51115.htm

### Generate Risk and Security Snapshot Reports (Risk Management (Redwood))
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Risk Management (Redwood) needs a service request to Oracle to get set up (Oracle's introduction), and access comes through the Risk Management roles and record stakeholders; nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/erp/26d/rrsk26d/26D-rrsk-wn-f51130.htm

### Internal Control record management (Risk Management (Redwood))
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Risk Management (Redwood) needs a service request to Oracle to get set up (Oracle's introduction), and access comes through the Risk Management roles and record stakeholders; nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/erp/26d/rrsk26d/26D-rrsk-wn-f51038.htm

### Manage access entitlements for access algorithms (Risk Management (Redwood))
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Risk Management (Redwood) needs a service request to Oracle to get set up (Oracle's introduction), and access comes through the Risk Management roles and record stakeholders; nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/erp/26d/rrsk26d/26D-rrsk-wn-f51112.htm

### Monitor and schedule Risk Management jobs (Risk Management (Redwood))
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Risk Management (Redwood) needs a service request to Oracle to get set up (Oracle's introduction), and access comes through the Risk Management roles and record stakeholders; nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/erp/26d/rrsk26d/26D-rrsk-wn-f51119.htm

### My Access Certification Task management (Risk Management (Redwood))
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Risk Management (Redwood) needs a service request to Oracle to get set up (Oracle's introduction), and access comes through the Risk Management roles and record stakeholders; nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/erp/26d/rrsk26d/26D-rrsk-wn-f51072.htm

### My Internal Control Certification Tasks management (Risk Management (Redwood))
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Risk Management (Redwood) needs a service request to Oracle to get set up (Oracle's introduction), and access comes through the Risk Management roles and record stakeholders; nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/erp/26d/rrsk26d/26D-rrsk-wn-f51132.htm

### Reference Data management (Risk Management (Redwood))
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Risk Management (Redwood) needs a service request to Oracle to get set up (Oracle's introduction), and access comes through the Risk Management roles and record stakeholders; nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/erp/26d/rrsk26d/26D-rrsk-wn-f51070.htm

### Enhancements to Assignment Change Assistant with AI Assistance (Human Resources)
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Extends the 26C Assignment Change Assistant AI agent, which needs AI Agent Studio, permission groups and security set up (and an Oracle Support check of the environment); nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/hure-26d/26D-hr-wn-f50993.htm

### Protect Correct Termination Changes for Multi-Row EFF (Human Resources)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Automatic, but contained to one flow: when correcting a termination date, the extensible flexfields section becomes read-only.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/hure-26d/26D-hr-wn-f51748.htm

### Redwood Enabled by Default for Employment Pages in Update 26D (Human Resources)
- Rating: high (unchanged)
- Oracle: Larger scale · Action to Enable: None
- Reason: High kept: Oracle switches 20 Redwood employment pages on by default in 26D with no action needed; users see new pages unless the profile options are set to No.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/hure-26d/26D-hr-wn-f50016.htm

### Redwood Enabled by Default for Employment Pages in Update 27A (Human Resources)
- Rating: high (unchanged)
- Oracle: Larger scale · Action to Enable: None
- Reason: High kept: Oracle announces that Resign, Terminate and Mass Assignment Change switch to Redwood by default in 27A (same rating as the 26C notice).
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/hure-26d/26D-hr-wn-f50060.htm

### Agentic Course Designer (Learning and Development)
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: None
- Reason: Needs the Learning Connect SKU licensed and the instructional designer privilege; nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/lear-26d/26D-learning-wn-f51886.htm

### Agentic Course Player (Learning and Development)
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: None
- Reason: Only used for agentic courses, which have to be built first with Agentic Course Designer (Learning Connect SKU); nothing changes for existing courses. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/lear-26d/26D-learning-wn-f51885.htm

### Upgraded My Learning Assistant (Learning and Development)
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: The assistant has to be deployed through a guided journey (or the 25D version replaced with the new template); nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/lear-26d/26D-learning-wn-f50703.htm

### Enhanced Statutory Parental Bereavement Leave and Pay for Northern Ireland Employees (Payroll)
- Rating: high (unchanged)
- Oracle: Larger scale · Action to Enable: None
- Reason: High kept: automatic statutory pay change for Northern Ireland employees (eligibility for miscarriage-related absences, day-one eligibility, separate balances); touches how employees are paid.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/payr-26d/26D-payroll-wn-f51224.htm

### Redwood Experience for Balance Adjustment (Payroll)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: None
- Reason: New Redwood page for one payroll admin task (Adjust Individual Balances), on by default; visible but contained.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/payr-26d/26D-payroll-wn-f50910.htm

### Redwood Experience for Organization Calculation Cards (Payroll)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Redwood versions of the organization calculation card setup tasks, used by payroll implementers only; contained.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/payr-26d/26D-payroll-wn-f50612.htm

### Redwood Experience for Payroll Setup Pages (Payroll)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: None
- Reason: Six Redwood payroll setup pages on by default, used by payroll admins only, so contained (as for the 26C payroll setup pages). Oracle notes custom job roles need updating for the new Organization Payment Method page.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/payr-26d/26D-payroll-wn-f50913.htm

### Tax Calculation Statement Page: Federal Income Tax (Payroll)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: None
- Reason: A new read-only Tax Calculation Statement tab on Person Results for payrolls run after 26D; visible but contained, no process change (as for the 26C Canadian tab).
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/payr-26d/26D-payroll-wn-f51363.htm

### Tax Calculation Statement Page: Social Security (Payroll)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: None
- Reason: A new read-only Tax Calculation Statement tab on Person Results for payrolls run after 26D; visible but contained, no process change (as for the 26C Canadian tab).
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/payr-26d/26D-payroll-wn-f51361.htm

### Use Published Schedules to Determine UK Statutory Sick Pay Qualifying Days (Payroll)
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Needs Schedule Hierarchy Starting Point set to Published Schedule on each absence type; Oracle says customers that don't use Workforce Management published schedules see no change.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/payr-26d/26D-payroll-wn-f51226.htm

### Enhancements for Absence Integration on Redwood Time Cards (Time and Labor)
- Rating: high (unchanged)
- Oracle: Larger scale · Action to Enable: None
- Reason: High kept: automatic change to how absences on Redwood time cards are removed, withdrawn and approved; saving is blocked until the time card is resubmitted.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/tila-26d/26D-time-labor-wn-f50905.htm

### Redwood Experience for Workday Definitions (Time and Labor)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Redwood version of one setup task (Workday Definitions), on by default for Time and Labor admins; contained.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/tila-26d/26D-time-labor-wn-f50903.htm

### Open Shift Conflict Handling (Workforce Scheduling)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: None
- Reason: Automatic but contained: workers claiming part of an open shift see the claimable range, and fully blocked shifts are hidden.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26d/wosc-26d/26D-workforce-scheduling-wn-f51267.htm

### Handle date changes in contract lines as inline updates in purchase agreements (Procurement)
- Rating: high (unchanged)
- Oracle: Larger scale · Action to Enable: None
- Reason: High kept: automatic change to the Import Purchase Agreements from External Purchase Prices process; date changes now update the existing agreement line instead of end-dating it and adding a new one, which affects integrations relying on line references.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/proc26d/26D-procurement-wn-f50520.htm

### Manage negotiation templates (Procurement)
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Oracle says you must enable the Redwood Sourcing and Redwood Negotiation Templates profile options to access it; off until set up.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/proc26d/26D-procurement-wn-f42877.htm

### Simulate award scenarios in the Sourcing Command Center (Procurement)
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Needs the Sourcing Command Center profile option, permission groups and an Enterprise Sourcing Award Policy added in AI Agent Studio; nobody gets it by default. (Oracle rates it larger scale.)
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/proc26d/26D-procurement-wn-f51463.htm

### Introduce and plan for new business (Demand Management)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: A new optional Introductions page for demand plans; nothing changes in plan runs until you create introductions.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/demand26d/26D-demand-wn-f50198.htm

### Associate a technician to multiple labor resources (Maintenance)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: None
- Reason: Automatic, but only changes scheduling and assignment once you model a technician against more than one labor resource.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/maint26d/26D-maintenance-wn-f46400.htm

### Capture quality events for returns and field service debrief (Maintenance)
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: Potential Setup
- Reason: Needs inspection plans of type Asset defined in Quality Management, plus inspection privileges; nothing shows until then.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/maint26d/26D-maintenance-wn-f50143.htm

### Get substitution recommendations for high-risk, unreleased batches using the Batch Conformance Guide (Manufacturing)
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: None
- Reason: Process manufacturing only, and needs the 26C Batch Process Manufacturing Workspace and Redwood Batches profile options enabled; nobody gets it by default.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/mfg26d/26D-mfg-wn-f50431.htm

### Quality Assurance Workspace (Manufacturing)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: None
- Reason: A new agentic workspace for quality teams, available with existing inspection privileges; existing processes don't change. Visible but contained.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/mfg26d/26D-mfg-wn-f50528.htm

### Quality Assurance Workspace (Product Lifecycle Management)
- Rating: **high → medium**
- Oracle: Larger scale · Action to Enable: None
- Reason: A new agentic workspace for quality teams, available with existing inspection privileges; existing processes don't change. Visible but contained.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/plm26d/26D-plm-wn-f50528.htm

### Manage configurations programmatically with Redwood Configurator (Product Lifecycle Management)
- Rating: **high → low**
- Oracle: Larger scale · Action to Enable: None
- Reason: A REST service for developers and integrators; Oracle says it's designed for configurator modelers and system integrators, so nothing changes for users.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/plm26d/26D-plm-wn-f50870.htm

### Manage catalog administration tasks using a new user experience (Self Service Procurement)
- Rating: **medium → low**
- Oracle: Small scale · Action to Enable: Potential Setup
- Reason: Off by default: needs the Redwood Catalog Setup Pages Enabled profile option, which Oracle delivers set to No.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/ssproc26d/26D-ssproc-wn-f47406.htm

### Manage catalogs (Self Service Procurement)
- Rating: **medium → low**
- Oracle: Small scale · Action to Enable: Potential Setup
- Reason: Off by default: needs the Redwood Catalog Setup Pages Enabled profile option, which Oracle delivers set to No.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/ssproc26d/26D-ssproc-wn-f47412.htm

### Display line type when viewing requisition lines (Self Service Procurement)
- Rating: **medium → low**
- Oracle: Small scale · Action to Enable: Potential Setup
- Reason: Minor: the Line Type column is hidden by default and needs a Visual Builder Studio change for the Lines view.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/ssproc26d/26D-ssproc-wn-f47408.htm

### Search and filter requisition lines, purchase orders, and purchase agreements using descriptive flexfields (Procurement)
- Rating: **medium → low**
- Oracle: Small scale · Action to Enable: Potential Setup
- Reason: Needs flexfield segments added to the search indexes and the index jobs run; nothing changes until then.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/proc26d/26D-procurement-wn-f49560.htm

### Create intake requests for procurement contracts (Procurement)
- Rating: **medium → low**
- Oracle: Small scale · Action to Enable: Potential Setup
- Reason: Needs the Intake Requests opt-in enabled and Procurement Contracts implemented; nobody gets it by default.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/proc26d/26D-procurement-wn-f50314.htm

### Create intake requests for procurement contracts (Self Service Procurement)
- Rating: **medium → low**
- Oracle: Small scale · Action to Enable: Potential Setup
- Reason: Needs the Intake Requests opt-in enabled and Procurement Contracts implemented; nobody gets it by default.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/ssproc26d/26D-ssproc-wn-f50314.htm

### Additional criteria for label template selection rules (Warehouse Management)
- Rating: **medium → low**
- Oracle: Small scale · Action to Enable: Potential Setup
- Reason: Only adds optional criteria to label template selection rules; nothing changes until you add them.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26d/wms26d/26D-wms-wn-f51829.htm

### Receive the Risk Cloud Daily Digest (Risk Management (Redwood))
- Rating: **medium → low**
- Oracle: Small scale · Action to Enable: None
- Reason: Risk Management (Redwood) needs a service request to Oracle to get set up (Oracle's introduction), and access comes through the Risk Management roles and record stakeholders; nobody gets it by default.
- Source: https://docs.oracle.com/en/cloud/saas/readiness/erp/26d/rrsk26d/26D-rrsk-wn-f51122.htm
