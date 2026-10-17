# Impact ratings and summaries: second editorial pass (17 Oct 2026)

Scope: every tracked 26C (148) and 26B (134) change in `data/updates.json`, checked against its Oracle What's New feature page (description, Action to Enable / steps, Business Benefit, Oracle's scale of impact, opt-in status, and Oracle's Current Opt-In Expirations list).

Rules applied:

- **High**: users must change how they work; large-scale UI or process change; an opt-in ending, or a former opt-in now standard, that affects users; or touches payments, postings, integrations or security.
- **Medium**: visible but contained, or automatic but noticeable.
- **Low**: minor, cosmetic, reporting-only, or needs setup that nobody gets by default.
- Wording: "now standard", never "mandatory".

Overrides live in `data/editorial.json` (keyed by Oracle URL) and are applied by `scripts/build.py` after the automatic first pass, so they survive rebuilds. This file is not published on the site (it isn't copied into `dist/`).

## Totals

- **26C**: 63 ratings changed (high → low: 1, high → medium: 7, medium → high: 1, medium → low: 54); 50 summaries rewritten. Before: high 23, low 29, medium 96. After: high 16, low 84, medium 48.
- **26B**: 60 ratings changed (high → low: 7, high → medium: 19, medium → low: 34); 56 summaries rewritten. Before: high 40, low 10, medium 84. After: high 14, low 51, medium 69.

Items reviewed with no change: 99 (rating and summary already matched Oracle's page and the rules).

## 26C changes

### 26C-f49280@fins26c · Invoice Import with Supplier Bank Account Details Using Collaboration Messaging Framework
- Family / product: Financials · Financials · Payables Invoice Processing
- Rating: high (unchanged)
- Old summary: Import B2B XML invoices in Fusion Payables with supplier Remit-to Bank Account Number and Supplier IBAN using the Collaboration Messaging. The Collaboration Messaging inbound payload containing the supplier external bank account information, are interfaced to Fusion Payables.
- New summary: B2B XML invoices imported into Payables through Collaboration Messaging can now carry the supplier's remit-to bank account number and IBAN, and the invoice installment is paid to that account. If the bank details are left out, Payables falls back to the supplier's primary bank account.
- Reason: Summary was Oracle's raw wording with grammar errors; rewritten. High kept: touches supplier payments and an inbound integration.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f49280.htm

### 26C-f47388@fins26c · Accrued Expense Migration for Exempt Payments
- Family / product: Financials · Financials · Asset Acquisition, Maintenance, and Lease
- Rating: **medium → low**
- Reason: Only applies when importing midlife leases that have exempt payments; nothing changes in existing lease flows.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f47388.htm

### 26C-f47293@fins26c · Budget Entry Creation from Revenue for Control Budget
- Family / product: Financials · Financials · Planning and Budgeting
- Rating: **medium → low**
- Reason: Adds an optional Control Budget parameter to one process; nothing changes unless you use it.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f47293.htm

### 26C-f47385@fins26c · Calculation Calendar for Secondary Representation
- Family / product: Financials · Financials · Asset Acquisition, Maintenance, and Lease
- Rating: **medium → low**
- Reason: Oracle's steps require settings in Manage Lease Accounting Configuration (primary and secondary standards and ledgers) before it does anything.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f47385.htm

### 26C-f47291@fins26c · Carried Interest Payout Processing
- Family / product: Financials · Financials · Joint Venture Settlement
- Rating: **medium → low**
- Reason: Needs configuration in Joint Venture Management setup before anyone can use it.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f47291.htm

### 26C-f51045@fins26c · Carrier Information in fiscal documents created from Receivables transactions
- Family / product: Financials · Financials · Local Compliance & Reporting
- Rating: **medium → low**
- Reason: Brazil only, and only when a carrier is selected on a goods fiscal document; an optional new field.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f51045.htm

### 26C-f50544@fins26c · Cash Processing Agent for Receipt Processing and Cash Application
- Family / product: Financials · Financials · Cash Processing Agent
- Rating: medium (unchanged)
- Old summary: The Cash Processing Agent improves cash processing exception handling and increases cash application matching accuracy. It combines AI-assisted cash processing automation with guided insights to help users identify and resolve exceptions more efficiently.
- New summary: An AI agent that flags receipt and cash application exceptions and suggests matches, building on Document IO's automated reading of bank files and emailed remittances. It's on by default, but users need the agent's security access before they can use it.
- Reason: Summary didn't say users need security access first (Oracle's steps). Medium kept: touches cash application.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f50544.htm

### 26C-f47279@fins26c · Consumption Allowance Revenue Recognition
- Family / product: Financials · Financials · Revenue Management
- Rating: medium (unchanged)
- Old summary: Use enhanced revenue recognition support for allowance-based usage rating models in Oracle Subscription Management. You can now manage revenue recognition for subscriptions where customers purchase a defined quantity-based allowance, consume against that allowance during a balance period, purchase top-ups, roll over unused allowance, and incur overage when usage exceeds the available allowance- all this in accordance…
- New summary: Revenue Management now handles allowance-based usage plans from Subscription Management (base allowance, top-ups, rollover and overage) and recognizes revenue for each part under ASC 606 and IFRS 15.
- Reason: Summary was cut off mid-sentence.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f47279.htm

### 26C-f47386@fins26c · Lease Migration Balances by Representation
- Family / product: Financials · Financials · Asset Acquisition, Maintenance, and Lease
- Rating: **medium → low**
- Reason: Only applies when importing midlife expense leases (migration); no change to existing leases.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f47386.htm

### 26C-f49371@fins26c · Service Excellence Continuing Investments
- Family / product: Financials · Financials · Performance and Stability
- Rating: medium (unchanged)
- Old summary: Our ongoing investment in service excellence has a focus on overall usability, resiliency, performance, and security. This work is based on monitoring performance trends, reviewing common use patterns, analyzing service requests, and participating in many discussions with customers.
- New summary: A bundle of small usability, resiliency, performance and security fixes across Financials, for example a new Subledger Accounting source (Prepayment Line Type Code) for prepayment lines. Check Oracle's page for the full list.
- Reason: Summary was Oracle boilerplate that said nothing about what changed.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f49371.htm

### 26C-f49529@risk26c · New Dashboard for Reviewing Intra-Role Violations
- Family / product: Financials · Risk Management (Classic) · Transactional Business Intelligence for Risk Management
- Rating: low (unchanged)
- Old summary: This dashboard enables users to review intra-role access violations. For the selected access algorithm(s), the Intra-Role Access Violations Dashboard includes:
- New summary: A new dashboard for reviewing intra-role access violations: counts of affected roles and users, with drill-down to entitlements, incident paths and violations by algorithm.
- Reason: Summary ended in a colon (cut off before Oracle's list).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/risk26c/26C-risk-wn-f49529.htm

### 26C-f43609@fins26c · Attributes for Asset Addition Using ERP Integration REST API
- Family / product: Financials · Financials · Integration & Extensibility
- Rating: low (unchanged)
- Old summary: Procure to Pay - Asset Acquisition, Maintenance, and Lease: The “Transaction-addAsset” service of the ERP Integration REST API supports the following additional attributes in 26C, which can now be added during asset addition:
- New summary: The addAsset service of the ERP Integration REST API now accepts impairment reserve and year-to-date impairment values when you add assets.
- Reason: Summary ended in a colon and named a column header instead of the change.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f43609.htm

### 26C-f49403@fins26c · Budget Adjustment Assistant
- Family / product: Financials · Financials · Budgetary Control
- Rating: low (unchanged)
- Old summary: The Budget Adjustment Assistant helps budget office users create budget entries using natural language for control budgets sourced from Enterprise Performance Management (EPM) .
- New summary: An AI assistant that helps budget office users create budget entries in plain language for control budgets sourced from EPM, fix errors before submitting, and check budgetary control balances. Users need the Budget Adjustment Assistant role.
- Reason: Clarified that a role is needed (Oracle: Setup Required).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f49403.htm

### 26C-f50616@fins26c · Cash Processing Agent for Cash Positioning and Improved Liquidity
- Family / product: Financials · Financials · Cash Processing Agent
- Rating: low (unchanged)
- Old summary: Cash Processing Agent The Cash Processing Agent for Cash Positioning and Improved Liquidity helps cash managers review daily liquidity through an insights-driven conversational experience.
- New summary: An AI agent that gives cash managers a conversational view of daily liquidity: cash position, bank balances, intraday movements and accounts short of cash. Users need security access set up first.
- Reason: Summary started with a stray heading ('Cash Processing Agent The ...').
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/fins26c/26C-fin-wn-f50616.htm

### 26C-f46532@hure-26c · Display Page Properties Conditionally in Connections
- Family / product: HCM · Human Resources · Workforce Directory Management
- Rating: **high → medium**
- Old summary: You can control the Connections experience with the Configure Page Properties feature. You can now apply these settings with conditional rules based on:
- New summary: Admins can now apply Connections page properties, such as hiding the Feedback card, conditionally: by the viewer's role, whether they're viewing their own profile, or the profile's business unit, department, country, legal employer or location.
- Reason: Nothing changes until an admin sets up conditional rules, so not a large change for users. Summary ended in a colon.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/hure-26c/26C-hr-wn-f46532.htm

### 26C-f50016@hure-26c · Redwood Enabled by Default for Employment Pages in Update 26D
- Family / product: HCM · Human Resources · Employment
- Rating: high (unchanged)
- Old summary: Enhance the user experience by letting users directly access the following Redwood-enabled HCM pages where the Redwood profile option is turned on by default in 26D.
- New summary: From 26D, the Redwood versions of the employment pages (Add Assignment, Add Contingent Worker, Add Nonworker, Add Pending Worker and more) are switched on by default through their profile options. Nothing changes in 26C, so plan your testing for 26D.
- Reason: Summary said 'enhance the user experience' without saying what happens or when; made clear it's a 26D change.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/hure-26c/26C-hr-wn-f50016.htm

### 26C-f50060@hure-26c · Redwood Enabled by Default for Employment Pages in Update 27A
- Family / product: HCM · Human Resources · Employment
- Rating: high (unchanged)
- Old summary: Enhance the user experience by letting users directly access the following Redwood-enabled Employment pages where the Redwood profile option is turned on by default in 27A.
- New summary: From 27A, the Redwood Resign from Employment, Terminate Employment and Mass Assignment Change pages are switched on by default. Nothing changes in 26C.
- Reason: Summary didn't name the pages; made clear it's a 27A change.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/hure-26c/26C-hr-wn-f50060.htm

### 26C-f47440@hure-26c · Redwood Enabled by Default for Person Pages in Update 26D
- Family / product: HCM · Human Resources · Person
- Rating: high (unchanged)
- Old summary: Effective from release 26D, the Redwood person pages will be enabled by default. This update was initially planned for release 26C, but it's being moved to release 26D.
- New summary: The Redwood person pages (Personal Details, Contact Info, Identification Info, Family and Emergency Contacts and more) become the default in 26D, not 26C as Oracle first planned. You can switch back to the older pages by setting their profile options to No.
- Reason: Reworded for clarity; added the pages and how to switch back.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/hure-26c/26C-hr-wn-f47440.htm

### 26C-f46375@payr-26c · Local Tax Jurisdiction Sync on Tax Withholding Card
- Family / product: HCM · Payroll · Payroll for the United States
- Rating: high (unchanged)
- Old summary: We have enhanced the sync of local tax jurisdictions to the employee’s Tax Withholding card to provide more consistent, controlled, and auditable behavior. When you create or update a valid address (latitude/longitude present), the system automatically synchronizes any affected local tax jurisdictions from the Tax Jurisdiction card to the following regional components on the tax card.
- New summary: When a valid address is created or updated, the affected local tax jurisdictions now sync automatically to the employee's Tax Withholding card: Ohio and Kentucky school districts and Pennsylvania PSD and school districts (Indiana gets component creation only).
- Reason: Summary ended with 'the following regional components' and no list.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/payr-26c/26C-payroll-wn-f46375.htm

### 26C-f49372@payr-26c · Redwood Experience for Payroll Setup Pages
- Family / product: HCM · Payroll · Global Payroll
- Rating: **high → medium**
- Old summary: The following Payroll setup pages are now available in the Redwood user experience: Oracle Search for HCM is now integrated within these setup pages.
- New summary: The Element Classifications, Consolidation Group and Payment Methods Preferences setup pages are now Redwood pages, with Oracle Search for HCM built in. They're on by default, and any personalizations of the old pages have to be redone.
- Reason: Setup pages used by payroll admins only, so contained. Summary was garbled ('...user experience: Oracle Search...'); added Oracle's note that personalizations must be redone.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/payr-26c/26C-payroll-wn-f49372.htm

### 26C-f49835@payr-26c · Tax Calculation Statement Page
- Family / product: HCM · Payroll · Payroll for Canada
- Rating: **high → medium**
- Reason: A new read-only tab on Person Results for Canadian payroll; visible but contained, no process change.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/payr-26c/26C-payroll-wn-f49835.htm

### 26C-f50592@tila-26c · Compensatory Time Interface Enhancements
- Family / product: HCM · Time and Labor · Time and Labor
- Rating: high (unchanged)
- Old summary: Two new enhancements to the compensatory time integration are being introduced in this release. Entry-Level Approval Support for Payroll Users
- New summary: If you use the Entry Level Approval timecard task, compensatory time earned now goes to Absence Management as each time entry is approved, so the balance is usable straight away, not after the whole timecard is approved. Compensatory time also now works for customers using only Projects with a third-party payroll.
- Reason: Summary was cut off after a heading. High kept: automatic change to when absence balances update.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/tila-26c/26C-time-labor-wn-f50592.htm

### 26C-f49549@amg-26c · Additional Extensibility for Redwood Add Absence
- Family / product: HCM · Absence Management · Absence Management
- Rating: **medium → low**
- Reason: Needs extension work in Visual Builder Studio; nothing changes by default.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/amg-26c/26C-absence-mgmt-wn-f49549.htm

### 26C-f49554@amg-26c · Compensatory Time Interface Enhancements
- Family / product: HCM · Absence Management · Absence Management
- Rating: **medium → high**
- Old summary: Two new enhancements to the compensatory time integration are being introduced in this release. With this enhancement, when customers use the Timecard Approval ELA task, compensatory time earned entries are now sent to Absence Management as soon as each individual time entry is approved.
- New summary: If you use the Entry Level Approval timecard task, compensatory time earned now goes to Absence Management as each time entry is approved, so the balance is usable straight away, not after the whole timecard is approved. Compensatory time also now works for customers using only Projects with a third-party payroll.
- Reason: Same Oracle feature as the Time and Labor entry (rated high); aligned the rating and summary. Automatic change to when compensatory balances update.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/amg-26c/26C-absence-mgmt-wn-f49554.htm

### 26C-f49551@amg-26c · Display Unpaid Break when Absence is Entered on the Timecard
- Family / product: HCM · Absence Management · Absence Management
- Rating: medium (unchanged)
- Old summary: Previously, we introduced a feature in 26B to display unpaid break on the absence Redwood pages when the break is automatically deducted from the absence duration.
- New summary: Absences entered on the timecard now also show the unpaid break deducted from the absence duration, in a read-only field on the Redwood absence pages (26B did this for absences entered in Absence Management).
- Reason: Summary only described the 26B feature, not what's new.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/amg-26c/26C-absence-mgmt-wn-f49551.htm

### 26C-f49555@amg-26c · Invalid Dates are Disabled in the Date Picker
- Family / product: HCM · Absence Management · Absence Management
- Rating: **medium → low**
- Reason: Minor UI aid: invalid dates are greyed out in the date picker.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/amg-26c/26C-absence-mgmt-wn-f49555.htm

### 26C-f49553@amg-26c · Optional Reason for Discretionary Disbursements
- Family / product: HCM · Absence Management · Absence Management
- Rating: **medium → low**
- Old summary: You can now configure absence plans to mandate reason selection when disbursing balances. You can define your list of acceptable reasons using the new ORA_ANC_DISBURSEMENT_REASONS lookup code.
- New summary: You can now set up absence plans so users must pick a reason, from the new ORA_ANC_DISBURSEMENT_REASONS lookup, when they enter or upload discretionary disbursements. Nothing changes until you attach reasons to a plan.
- Reason: Only applies after you define reasons and attach them to a plan. Summary didn't make clear it's optional.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/amg-26c/26C-absence-mgmt-wn-f49553.htm

### 26C-f49552@amg-26c · Prevent Withdrawal of Previously Approved Absences
- Family / product: HCM · Absence Management · Absence Management
- Rating: medium (unchanged)
- Old summary: Previously, if an employee edited and resubmitted an already approved absence, the status changed to Awaiting Approval status and the employee could withdraw the absence without the manager's approval.
- New summary: Employees can no longer withdraw an approved absence that they've edited and resubmitted while the change is awaiting approval. The manager has to approve the change first, and withdrawing it after that needs approval too.
- Reason: Summary only described the old behavior, not the change.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/amg-26c/26C-absence-mgmt-wn-f49552.htm

### 26C-f49550@amg-26c · Use VB Studio to Restrict Access to Past and Future Assignments
- Family / product: HCM · Absence Management · Absence Management
- Rating: **medium → low**
- Reason: Needs two new page properties set in Visual Builder Studio; nothing changes by default.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/amg-26c/26C-absence-mgmt-wn-f49550.htm

### 26C-f49902@benf-26c · Configure Rules for Benefits Redwood Page Properties
- Family / product: HCM · Benefits · Benefits
- Rating: **medium → low**
- Reason: Admin capability in Visual Builder Studio; nothing changes until rules are configured.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/benf-26c/26C-benefits-wn-f49902.htm

### 26C-f49782@benf-26c · Display Benefits Document Type Names in Certification Panel Drawers
- Family / product: HCM · Benefits · Benefits
- Rating: **medium → low**
- Reason: Minor label change in Redwood Benefits, and only with the Redwood Benefits profile options on.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/benf-26c/26C-benefits-wn-f49782.htm

### 26C-f49784@benf-26c · Enhanced Benefits Analyst Agent for Flex Credits and Benefits Representatives
- Family / product: HCM · Benefits · Benefits
- Rating: **medium → low**
- Reason: Extends an AI agent that has to be set up, plus the Redwood Benefits profile options; nobody gets it by default.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/benf-26c/26C-benefits-wn-f49784.htm

### 26C-f49786@benf-26c · Preview Certification Attachments in the Benefits Summary
- Family / product: HCM · Benefits · Benefits
- Rating: **medium → low**
- Reason: Minor UI convenience (inline preview of attachments).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/benf-26c/26C-benefits-wn-f49786.htm

### 26C-f49787@benf-26c · Simulate a Life Event for Benefits Administrators
- Family / product: HCM · Benefits · Benefits
- Rating: medium (unchanged)
- Old summary: Benefits administrators can now simulate a life event for a person from the Benefits Summary page. The simulation allows administrators to: The simulation is read-only.
- New summary: Benefits administrators can now simulate a life event for a person from the Benefits Summary page and see the estimated eligibility and rates it would produce. The simulation is read-only and saves nothing.
- Reason: Summary was garbled ('allows administrators to: The simulation is read-only').
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26c/benf-26c/26C-benefits-wn-f49787.htm

### 26C-f47313@gtm26c · Try the New Redwood Experience
- Family / product: Logistics (OTM/GTM/WMS) · Global Trade Management · Redwood UI
- Rating: high (unchanged)
- Old summary: Redwood is the new user interface for Oracle Transportation and Global Trade Management. The 26C "Try the New Redwood Experience" extends the Redwood Experience by adding an additional set of UIs that have been migrated to the modern look and unified user interface provided by Redwood.
- New summary: More Transportation and Global Trade Management screens are now available in the Redwood UI, along with the Product Map navigation view and Redwood Help and Export. Where both exist the legacy screens remain, but Oracle strongly encourages moving to Redwood.
- Reason: Clarified what's new and that legacy screens remain. High kept (Oracle: larger scale UI change).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/gtm26c/26C-gtm-wn-f47313.htm

### 26C-f47313@otm26c · Try the New Redwood Experience
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · Redwood UI
- Rating: high (unchanged)
- Old summary: Redwood is the new user interface for Oracle Transportation and Global Trade Management. The 26C "Try the New Redwood Experience" extends the Redwood Experience by adding an additional set of UIs that have been migrated to the modern look and unified user interface provided by Redwood.
- New summary: More Transportation and Global Trade Management screens are now available in the Redwood UI, along with the Product Map navigation view and Redwood Help and Export. Where both exist the legacy screens remain, but Oracle strongly encourages moving to Redwood.
- Reason: Clarified what's new and that legacy screens remain. High kept (Oracle: larger scale UI change).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/otm26c/26C-otm-wn-f47313.htm

### 26C-f49755@gtm26c · AI Agent Studio - Seeded Business Objects
- Family / product: Logistics (OTM/GTM/WMS) · Global Trade Management · AI Infrastructure
- Rating: **medium → low**
- Old summary: This feature provides you with a set of thirty pre-seeded OTM/GTM business objects that are available within the AI Agent Studio to simplify the development of your AI Agents.
- New summary: Thirty ready-made OTM and GTM business objects are now available in AI Agent Studio, so you don't have to map them yourself when building your own AI agents.
- Reason: Only matters to teams building their own AI agents; no change for users. Summary simplified.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/gtm26c/26C-gtm-wn-f49755.htm

### 26C-f49634@gtm26c · Copy Additional Data from Inventory to Exit Declaration Line
- Family / product: Logistics (OTM/GTM/WMS) · Global Trade Management · Trade Incentive Programs
- Rating: **medium → low**
- Old summary: This feature enables you to copy dates and zone status information from your inventory to an exit declaration. When moving goods out of a Free Trade Zone (FTZ), you must create an exit declaration.
- New summary: When you move goods out of a Free Trade Zone, the exit declaration line can now copy dates (such as the entry date) and zone status from inventory, based on a data configuration you define.
- Reason: Needs a data configuration before anything is copied. Summary made clearer.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/gtm26c/26C-gtm-wn-f49634.htm

### 26C-f49353@gtm26c · Enhancement to Restricted Party Screening Workbench
- Family / product: Logistics (OTM/GTM/WMS) · Global Trade Management · Restricted Party Screening
- Rating: medium (unchanged)
- Old summary: This feature introduces enhancements to the Restricted Party Screening Workbench. Business Benefit: This enhancement improves the usability and efficiency of the Restricted Party Screening Workbench by:
- New summary: In the Restricted Party Screening Workbench, Passed and Failed now show in green and red, and new buttons let you mark a party as Trusted, Requires Screening or Prohibited.
- Reason: Summary was cut off at 'Business Benefit:'.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/gtm26c/26C-gtm-wn-f49353.htm

### 26C-f49597@gtm26c · Enhancements to License Management
- Family / product: Logistics (OTM/GTM/WMS) · Global Trade Management · Trade Compliance
- Rating: medium (unchanged)
- Old summary: This feature enhances license management to better support scenarios that use both license reservation and license assignment. With these enhancements, you can: License management enables you to reserve license quantities and values upon receipt of a sales order to help ensure compliance.
- New summary: License management now copes when a shipment exceeds the reserved license amount: a new Allow Supplement from Balance flag lets the assignment draw the extra from the license balance, and a new Adjust License action updates the reserved balance.
- Reason: Summary was garbled (sentences out of order, dangling 'you can:').
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/gtm26c/26C-gtm-wn-f49597.htm

### 26C-f46555@gtm26c · Entry Exit Configuration on Trade Incentive Programs
- Family / product: Logistics (OTM/GTM/WMS) · Global Trade Management · Trade Incentive Programs
- Rating: medium (unchanged)
- Old summary: A new Entry-Exit Configuration section is now available for Trade Incentive Programs. This enhancement provides greater flexibility when configuring trade incentive programs, including: Within the Entry-Exit Configuration section, you can define the following:
- New summary: Trade Incentive Programs get a new Entry-Exit Configuration section that replaces the Applicable Profile. It supports both customs and physical inventory tracking and sets the sequence, entry-exit profile and movement type for each program.
- Reason: Summary ended in a colon twice.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/gtm26c/26C-gtm-wn-f46555.htm

### 26C-f49885@gtm26c · Redwood Theme For Enhanced Workbench
- Family / product: Logistics (OTM/GTM/WMS) · Global Trade Management · Enhanced Workbench Improvements
- Rating: **medium → low**
- Old summary: This feature incorporates several of the Redwood style elements into the Enhanced Workbench. The enhancements provided include the following: Enhanced Workbench - Redwood Theme Improvements
- New summary: The Enhanced Workbench picks up Redwood styling: a Redwood strip across the top of layouts and Redwood colors on the side navigation bar.
- Reason: Cosmetic. Summary was cut off after a screenshot caption.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/gtm26c/26C-gtm-wn-f49885.htm

### 26C-f49602@gtm26c · Transaction Type/Declaration Type Available on Line UIs
- Family / product: Logistics (OTM/GTM/WMS) · Global Trade Management · Trade Compliance
- Rating: **medium → low**
- Old summary: The Type ID is now available in the Trade Transaction Line and Declaration Line user interfaces. Business Benefit: This enhancement improves visibility and access to transaction type and declaration type information directly within key workflow pages.
- New summary: The transaction type and declaration type are now shown, and searchable, on Trade Transaction Line and Declaration Line pages.
- Reason: Minor: one extra field on existing pages. Summary contained a stray 'Business Benefit:' label.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/gtm26c/26C-gtm-wn-f49602.htm

### 26C-f49755@otm26c · AI Agent Studio - Seeded Business Objects
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · AI Infrastructure
- Rating: **medium → low**
- Old summary: This feature provides you with a set of thirty pre-seeded OTM/GTM business objects that are available within the AI Agent Studio to simplify the development of your AI Agents.
- New summary: Thirty ready-made OTM and GTM business objects are now available in AI Agent Studio, so you don't have to map them yourself when building your own AI agents.
- Reason: Only matters to teams building their own AI agents; no change for users. Summary simplified.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/otm26c/26C-otm-wn-f49755.htm

### 26C-f46332@otm26c · Copy Parameter Override
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · Logistics Network Modeling
- Rating: **medium → low**
- Reason: Minor convenience (a new copy action).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/otm26c/26C-otm-wn-f46332.htm

### 26C-f49885@otm26c · Redwood Theme For Enhanced Workbench
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · Enhanced Workbench Improvements
- Rating: **medium → low**
- Old summary: This feature incorporates several of the Redwood style elements into the Enhanced Workbench. The enhancements provided include the following: Enhanced Workbench - Redwood Theme Improvements
- New summary: The Enhanced Workbench picks up Redwood styling: a Redwood strip across the top of layouts and Redwood colors on the side navigation bar.
- Reason: Cosmetic. Summary was cut off after a screenshot caption.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/otm26c/26C-otm-wn-f49885.htm

### 26C-f50053@wms26c · Enhance Queries for Wave Research Advisor AI Agent
- Family / product: Logistics (OTM/GTM/WMS) · Warehouse Management · Outbound Logistics
- Rating: **medium → low**
- Reason: Only for customers who have set up the Wave Research Advisor agent (26A); nobody gets it by default.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/wms26c/26C-wms-wn-f50053.htm

### 26C-f50402@wms26c · Honor Expiry Date Range Rules for Cross Dock Pick And Allocate
- Family / product: Logistics (OTM/GTM/WMS) · Warehouse Management · Inventory Operations
- Rating: **medium → low**
- Reason: New mobile screen parameter; if it's left blank, Pick and Allocate works as before.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/wms26c/26C-wms-wn-f50402.htm

### 26C-f50401@wms26c · Honor Expiry Date Range Rules for Direct Allocation
- Family / product: Logistics (OTM/GTM/WMS) · Warehouse Management · Inventory Operations
- Rating: **medium → low**
- Reason: New mobile screen parameter; if it's left blank, Direct Allocation works as before.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/wms26c/26C-wms-wn-f50401.htm

### 26C-f50161@wms26c · Honor Expiry Date Range, Order Prioritization Rules for Distribute LPN
- Family / product: Logistics (OTM/GTM/WMS) · Warehouse Management · Inventory Operations
- Rating: **medium → low**
- Old summary: Warehouses use flowthrough to move received inventory directly to outbound orders instead of storing it first. When several orders can receive the same inventory, users need a consistent way to decide which inventory should flow through and which order should receive it.
- New summary: Distribute LPN can now use Crossdock Flowthrough Rules to decide which received inventory flows straight to which outbound order, based on inventory details, expiry date range, order criteria and priority.
- Reason: Needs flowthrough rules configured. Summary described the problem, not the change.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/wms26c/26C-wms-wn-f50161.htm

### 26C-f50178@wms26c · UPS Standard Integration Supports Shipping to Canada
- Family / product: Logistics (OTM/GTM/WMS) · Warehouse Management · Outbound Logistics
- Rating: medium (unchanged)
- Old summary: UPS Standard integration now supports international shipping to Canada by sending invoice line total information. You don't need to do anything to enable this feature.
- New summary: The UPS Standard integration now sends an invoice line total (item unit cost times quantity), so shipments to Canada can be manifested. Item unit cost must be above zero, or manifesting may fail.
- Reason: Summary repeated Oracle's 'You don't need to do anything' line and missed the unit-cost caveat.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/wms26c/26C-wms-wn-f50178.htm

### 26C-f50162@wms26c · View Employee Timeline Metrics
- Family / product: Logistics (OTM/GTM/WMS) · Warehouse Management · Warehouse Workforce Management
- Rating: **medium → low**
- Old summary: Warehouse managers need a simple way to review how employees spend time during the day. They need visibility into facility time, work area activity, and break time so they can understand labor usage, identify gaps, and support daily workforce decisions.
- New summary: A new Employee Timeline Metrics tab in the WFM Employee Dashboard shows each employee's day in one place: facility clock-in and clock-out, work area activity and breaks.
- Reason: Reporting-only view. Summary described the need, not the feature.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26c/wms26c/26C-wms-wn-f50162.htm

### 26C-f42886@proc26c · AI Agent: Negotiation Surrogate Response Assistant
- Family / product: Procurement · Procurement · Sourcing
- Rating: **high → low**
- Reason: An AI agent template that has to be deployed, with a monitored mailbox and Redwood Sourcing on; nobody gets it by default. (Oracle rates it larger scale.)
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/proc26c/26C-procurement-wn-f42886.htm

### 26C-f47247@proc26c · Create Transfer Orders with Header Level Descriptive Flexfields
- Family / product: Procurement · Procurement · Supply Chain Orchestration
- Rating: **medium → low**
- Reason: Optional new fields in a REST API and FBDI template; existing integrations keep working.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/proc26c/26C-procurement-wn-f47247.htm

### 26C-f46385@proc26c · Redwood: Communicate Purchase Agreements to Multiple Email Recipients
- Family / product: Procurement · Procurement · Purchasing
- Rating: **medium → low**
- Reason: Minor: extra email recipients when communicating agreements.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/proc26c/26C-procurement-wn-f46385.htm

### 26C-f44482@proc26c · Redwood: Review B2B Account Number on Purchasing Documents
- Family / product: Procurement · Procurement · Purchasing
- Rating: **medium → low**
- Reason: Minor: one extra field in the supplier information drawer on Redwood purchasing pages.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/proc26c/26C-procurement-wn-f44482.htm

### 26C-f49334@proc26c · Redwood: Use Extensibility Capabilities to Default Document Styles When Creating Purchasing Documents
- Family / product: Procurement · Procurement · Purchasing
- Rating: **medium → low**
- Reason: Needs Visual Builder Studio extension work; nothing changes by default.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/proc26c/26C-procurement-wn-f49334.htm

### 26C-f46352@proc26c · Redwood: View Additional Information About Location and Supplier
- Family / product: Procurement · Procurement · Purchasing
- Rating: **medium → low**
- Reason: Minor: extra detail drawers on Redwood purchase order and agreement pages.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/proc26c/26C-procurement-wn-f46352.htm

### 26C-f49435@proc26c · Selected External Purchase Prices Bug Fixes in This Update
- Family / product: Procurement · Procurement · External Purchase Prices
- Rating: **medium → low**
- Old summary: This update includes some bug fixes that can change the way Oracle External Purchase Prices works. This isn't a full list of all the bug fixes in this update.
- New summary: External Purchase Prices FBDI templates now work on Mac as well as Windows. Oracle lists this among the 26C bug fixes that change behavior.
- Reason: Minor fix. Summary was boilerplate that didn't say what changed.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/proc26c/26C-procurement-wn-f49435.htm

### 26C-f47268@proc26c · Selected Purchasing Bug Fixes in This Update
- Family / product: Procurement · Procurement · Purchasing
- Rating: medium (unchanged)
- Old summary: This update includes some bug fixes that can change the way Oracle Purchasing works. This isn't a full list of all the bug fixes in this update.
- New summary: Oracle's list of 26C Purchasing fixes that change behavior. The main one: with profile option ORA_PO_CO_BUDGET_DATE_FOR_LIQ set to Y, funds on change orders are now liquidated on the budget date, the change order date or the current date, depending on dates and fulfillment. Others include global DFFs on Approved Supplier List documents and back-arrow navigation on Redwood pages.
- Reason: Summary was boilerplate. Medium kept: one fix changes encumbrance liquidation dates.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/proc26c/26C-procurement-wn-f47268.htm

### 26C-f49711@proc26c · Selected Sourcing Bug Fixes in This Update
- Family / product: Procurement · Procurement · Sourcing
- Rating: medium (unchanged)
- Old summary: This update includes a bug fix that can change the way Oracle Sourcing works. This isn't a full list of all the bug fixes in this update.
- New summary: Fix: in Redwood, a negotiation created from a template now uses the latest version of its negotiation style, so style changes made after the template was created now apply.
- Reason: Summary was boilerplate that didn't say what changed.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/proc26c/26C-procurement-wn-f49711.htm

### 26C-f43314@proc26c · View Additional Information About Preparers, Requesters, Buyers, and Approvers
- Family / product: Procurement · Procurement · Purchasing
- Rating: **medium → low**
- Reason: Minor: extra person details behind name links on requisitions and POs.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/proc26c/26C-procurement-wn-f43314.htm

### 26C-f43313@ssproc26c · Access Cart Details Directly During Requisition Creation
- Family / product: Procurement · Self Service Procurement · Self Service Procurement
- Rating: **medium → low**
- Reason: Minor navigation aid (cart item count and link while creating requests).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/ssproc26c/26C-ssproc-wn-f43313.htm

### 26C-f47247@ssproc26c · Create Transfer Orders with Header Level Descriptive Flexfields
- Family / product: Procurement · Self Service Procurement · Supply Chain Orchestration
- Rating: **medium → low**
- Reason: Optional new fields in a REST API and FBDI template; existing integrations keep working.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/ssproc26c/26C-ssproc-wn-f47247.htm

### 26C-f46356@ssproc26c · Create a Noncatalog Request Without Copying Supplier Details From a Previous Request
- Family / product: Procurement · Self Service Procurement · Self Service Procurement
- Rating: **medium → low**
- Old summary: This enhancement improves the confirmation message you receive after creating a noncatalog or smart form request. You can select Create another request with the same supplier to create a new request with the same supplier information that was entered.
- New summary: After you submit a noncatalog or smart form request, the confirmation message now offers Create another request (starting fresh) alongside Create another request with the same supplier. The View cart link moves to the navigation bar at the bottom of the page.
- Reason: Minor change to a confirmation message. Summary didn't match the feature title (it described only the existing option).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/ssproc26c/26C-ssproc-wn-f46356.htm

### 26C-f49452@ssproc26c · Identify Attachments and Notes on My Requisitions
- Family / product: Procurement · Self Service Procurement · Self Service Procurement
- Rating: **medium → low**
- Old summary: In update 26B, we introduced the Identify Attachments and Notes on Requisition Lines feature, which displays an icon next to requisition lines with notes or attachments in the shopping cart and on the Requisition Line Details page.
- New summary: The note and attachment icons that 26B added to requisition lines now also appear on the My Requisitions page.
- Reason: Minor icon. Summary only described the 26B feature.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/ssproc26c/26C-ssproc-wn-f49452.htm

### 26C-f43317@ssproc26c · Launch Quote to Purchase Requisition Assistant from Menu
- Family / product: Procurement · Self Service Procurement · Self Service Procurement
- Rating: **medium → low**
- Old summary: In update 25D, we introduced the AI Agent: Quote to Purchase Requisition Assistant feature, which parses emails containing supplier quotations and automatically converts them into purchase requisitions.
- New summary: The Quote to Purchase Requisition Assistant, which turns emailed supplier quotes into requisitions, can now be started from the Self Service Procurement home page menu, without setting up an email account. You still need to create and publish an instance of the agent in AI Agent Studio.
- Reason: Needs the agent set up in AI Agent Studio. Summary only described the 25D feature.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/ssproc26c/26C-ssproc-wn-f43317.htm

### 26C-f43315@ssproc26c · Manage Public Shopping Lists
- Family / product: Procurement · Self Service Procurement · Self Service Procurement
- Rating: **medium → low**
- Reason: Off by default: needs the Redwood Catalog Setup Pages Enabled profile option, which is set to No.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/ssproc26c/26C-ssproc-wn-f43315.htm

### 26C-f46387@ssproc26c · Manage Shopping Catalog Category Hierarchies
- Family / product: Procurement · Self Service Procurement · Self Service Procurement
- Rating: **medium → low**
- Reason: Off by default: needs the Redwood Catalog Setup Pages Enabled profile option, which is set to No.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/ssproc26c/26C-ssproc-wn-f46387.htm

### 26C-f43763@ssproc26c · Search for Deliver-to Locations Using Additional Attributes in Requisitions
- Family / product: Procurement · Self Service Procurement · Self Service Procurement
- Rating: **medium → low**
- Old summary: Search for deliver-to locations using additional attributes in the Self Service Procurement application. With ‘More search options’ on location LOVs, you can filter your search by these attributes: The enhanced deliver-to location search, previously available in the Preferences drawer, is now available on these pages:
- New summary: The enhanced deliver-to location search (by name, code, address, city, postal code or country) now works on the requisition line and summary edit pages, not just in Preferences. It's off by default and switched on with a Visual Builder Studio constant.
- Reason: Off by default (Visual Builder Studio constant). Summary was garbled (two dangling colons).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/ssproc26c/26C-ssproc-wn-f43763.htm

### 26C-f46538@ssproc26c · Selected Self Service Procurement Bug Fixes in This Update
- Family / product: Procurement · Self Service Procurement · Self Service Procurement
- Rating: **medium → low**
- Old summary: Easier Access to Charge Account Combination Details With this update, you can more easily review charge account combination details in both edit and read-only modes.
- New summary: Fix: charge account combination details are easier to review in requisitions, from the charge account actions menu in edit mode or the account link in read-only mode.
- Reason: Minor fix. Summary began with a heading.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/ssproc26c/26C-ssproc-wn-f46538.htm

### 26C-f46353@ssproc26c · Sort Shopping Search Results and Shopping Lists by Item Number and Supplier Item
- Family / product: Procurement · Self Service Procurement · Self Service Procurement
- Rating: **medium → low**
- Reason: Minor: column sorting; sorting by supplier item needs an extensibility constant.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/ssproc26c/26C-ssproc-wn-f46353.htm

### 26C-f43318@ssproc26c · View Additional Information About Deliver-to Locations
- Family / product: Procurement · Self Service Procurement · Self Service Procurement
- Rating: **medium → low**
- Reason: Minor: extra location details behind a link.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/ssproc26c/26C-ssproc-wn-f43318.htm

### 26C-f49352@ppm26c · Labor Commitment Reporting in OTBI
- Family / product: Project Management · Project Management · Cost Management and Control
- Rating: **medium → low**
- Reason: Reporting-only: new attributes in existing OTBI subject areas.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/ppm26c/26C-ppm-wn-f49352.htm

### 26C-f49302@ppm26c · Milestone Approval History
- Family / product: Project Management · Project Management · Planning, Scheduling, and Forecasting
- Rating: **medium → low**
- Reason: Minor: a read-only approval history for milestones.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/ppm26c/26C-ppm-wn-f49302.htm

### 26C-f49384@ppm26c · Optional Ship-To Account and Site Through Configurable Contract Line Validations
- Family / product: Project Management · Project Management · Billing and Revenue Management
- Rating: low (unchanged)
- Old summary: Specifying ship-to details on contract lines may be unnecessary when billing for projects or professional services, or when ship-to information is not used as a sales tax determinant.
- New summary: Two new contract line validations let privileged users make the ship-to account and ship-to site optional on project contract lines, by changing them to Warning or turning them off. By default they're still required.
- Reason: Summary described the reason, not the change.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/ppm26c/26C-ppm-wn-f49384.htm

### 26C-f49249@ppm26c · Project Contract Bill Transactions Assistant
- Family / product: Project Management · Project Management · Project Financial Control Agents
- Rating: low (unchanged)
- Old summary: Helps users find, review, and summarize bill transactions through a guided conversational experience, enabling faster billing review and decision-making. Use the Project Contract Bill Transactions Assistant to:
- New summary: An AI assistant that finds, reviews and summarizes project bill transactions by project, contract, status or date range. Users need the assistant's role in AI Agent Studio.
- Reason: Summary ended in a colon.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26c/ppm26c/26C-ppm-wn-f49249.htm

### 26C-f46398@maint26c · Clock In and Clock Out of Work Order Operations in My Maintenance Work
- Family / product: Supply Chain & Manufacturing · Maintenance · Maintenance
- Rating: high (unchanged)
- Old summary: In organizations enabled for advanced scheduling, maintenance technicians can now clock in and clock out for an operation to track execution time accurately. When the first technician clocks in to an assigned and qualified operation, the operation is automatically started and the actual start date is updated.
- New summary: In organizations using advanced scheduling, maintenance technicians can now clock in and out of work order operations in My Maintenance Work. The first clock-in starts the operation automatically, and it's marked complete once every assigned technician has finished.
- Reason: Reworded. High kept: automatically changes how operations start and complete for technicians.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/maint26c/26C-maintenance-wn-f46398.htm

### 26C-f46402@maint26c · Redwood: Create and Manage Follow Up Work Orders in My Maintenance Work
- Family / product: Supply Chain & Manufacturing · Maintenance · Maintenance
- Rating: **high → medium**
- Reason: New optional action for technicians, behind a new privilege; visible but contained.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/maint26c/26C-maintenance-wn-f46402.htm

### 26C-f46397@maint26c · Redwood: Edit Work Orders from My Maintenance Work
- Family / product: Supply Chain & Manufacturing · Maintenance · Maintenance
- Rating: **high → medium**
- Reason: New optional action for technicians, behind existing work order privileges; visible but contained.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/maint26c/26C-maintenance-wn-f46397.htm

### 26C-f44509@mfg26c · Redwood: Use a Separate Operation to Track Rework in a Standard or Nonstandard Discrete Manufacturing Work Order
- Family / product: Supply Chain & Manufacturing · Manufacturing · Discrete Manufacturing
- Rating: high (unchanged)
- Old summary: In the previous release, you could track rework activities and costs for materials and resources in the original work order that produces a product. For significant or complex rework, a dedicated process may be required for operational visibility and detailed tracking of the physical quantity being reworked, but without the additional steps of completing into inventory to rework in another work order.
- New summary: Discrete manufacturing work orders can now include a separate rework operation. Supervisors move rejected quantities to it and track rework progress and costs in the same work order, without completing into inventory and opening a new work order. Redwood pages only.
- Reason: Summary only described the previous release. High kept: changes work order execution and costing for rework.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/mfg26c/26C-mfg-wn-f44509.htm

### 26C-f44524@mfg26c · Use Kanban Planning to Manage Just-in-Time Material Replenishment
- Family / product: Supply Chain & Manufacturing · Manufacturing · Flow Manufacturing
- Rating: **high → medium**
- Old summary: Manufacturing and inventory teams need an accurate, repeatable way to size Kanban replenishment, so point-of-use materials stay available without driving excess inventory.
- New summary: New Kanban plans calculate the right number of Kanban cards or bin size for each pull sequence from an external forecast and pull sequence attributes (average daily demand, lead time, safety stock), and can then update the pull sequences.
- Reason: New planning capability you choose to use; no change to existing Kanban until you run plans and apply them. Summary described the need, not the feature.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/mfg26c/26C-mfg-wn-f44524.htm

### 26C-f46394@maint26c · Manage Organizations for Global Work Definitions Using File-Based Data Import
- Family / product: Supply Chain & Manufacturing · Maintenance · Maintenance
- Rating: **high → medium**
- Reason: Opt-in that becomes standard in 26D, but Oracle's expiration list shows it won't be switched on automatically, and it only affects FBDI loads of global work definitions.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/maint26c/26C-maintenance-wn-f46394.htm

### 26C-f47247@demand26c · Create Transfer Orders with Header Level Descriptive Flexfields
- Family / product: Supply Chain & Manufacturing · Demand Management · Supply Chain Orchestration
- Rating: **medium → low**
- Reason: Optional new fields in a REST API and FBDI template; existing integrations keep working.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/demand26c/26C-demand-wn-f47247.htm

### 26C-f45795@demand26c · Redwood: Calculate Planning Percentages for Product Families
- Family / product: Supply Chain & Manufacturing · Demand Management · Demand Management
- Rating: medium (unchanged)
- Old summary: In manufacturing and distribution environments with many items that have minor differences, it’s easier to plan at an aggregate level, such as a product family, and have automated mechanisms to disaggregate the forecast to items.
- New summary: Demand Management can now forecast at product-family level: it calculates planning percentages from history and splits family forecasts down to items, and Supply Planning can consume the forecast at item or family level. You switch it on per plan.
- Reason: Summary described the need, not the feature.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/demand26c/26C-demand-wn-f45795.htm

### 26C-f45812@demand26c · Redwood: Compare a Plan to its Archived Versions Using a New User Experience
- Family / product: Supply Chain & Manufacturing · Demand Management · Demand Management
- Rating: **medium → low**
- Reason: Minor: Redwood version of an existing comparison view.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/demand26c/26C-demand-wn-f45812.htm

### 26C-f45813@demand26c · Redwood: Compare a Plan to its Archived Versions Using a New User Experience
- Family / product: Supply Chain & Manufacturing · Demand Management · Replenishment Planning
- Rating: **medium → low**
- Reason: Minor: Redwood version of an existing comparison view.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/demand26c/26C-demand-wn-f45813.htm

### 26C-f46374@demand26c · Redwood: Create Link to AI Agents Using a New User Experience
- Family / product: Supply Chain & Manufacturing · Demand Management · Demand Management
- Rating: **medium → low**
- Reason: Needs a published AI agent configured to take the data context; nothing changes by default.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/demand26c/26C-demand-wn-f46374.htm

### 26C-f46376@demand26c · Redwood: Create Link to AI Agents Using a New User Experience
- Family / product: Supply Chain & Manufacturing · Demand Management · Replenishment Planning
- Rating: **medium → low**
- Reason: Needs a published AI agent configured to take the data context; nothing changes by default.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/demand26c/26C-demand-wn-f46376.htm

### 26C-f45842@demand26c · Redwood: Deep Links to Planning Pages and Visualizations with Context
- Family / product: Supply Chain & Manufacturing · Demand Management · Replenishment Planning
- Rating: **medium → low**
- Reason: Minor navigation aid (deep links).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/demand26c/26C-demand-wn-f45842.htm

### 26C-f45847@demand26c · Redwood: Enable Wildcard Search
- Family / product: Supply Chain & Manufacturing · Demand Management · Demand Management
- Rating: **medium → low**
- Reason: Minor search improvement.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/demand26c/26C-demand-wn-f45847.htm

### 26C-f45849@demand26c · Redwood: Enable Wildcard Search
- Family / product: Supply Chain & Manufacturing · Demand Management · Replenishment Planning
- Rating: **medium → low**
- Reason: Minor search improvement.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/demand26c/26C-demand-wn-f45849.htm

### 26C-f45793@demand26c · Redwood: Set Up Waterfall and Trend Analyses and Plan Comparisons Using a New User Experience
- Family / product: Supply Chain & Manufacturing · Demand Management · Demand Management
- Rating: medium (unchanged)
- Old summary: In previous updates, using the classic interface, you could configure tables and graphs to easily visualize trends and comparisons across plans and plan versions.
- New summary: Waterfall analyses, trend analyses and plan comparisons, previously set up in the classic interface, can now be configured on the Comparison tab of Redwood planning tables and graphs.
- Reason: Summary only described the previous behavior.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/demand26c/26C-demand-wn-f45793.htm

### 26C-f45797@demand26c · Redwood: Set Up Waterfall and Trend Analyses and Plan Comparisons Using a New User Experience
- Family / product: Supply Chain & Manufacturing · Demand Management · Replenishment Planning
- Rating: medium (unchanged)
- Old summary: In previous updates, using the classic interface, you could configure tables and graphs to easily visualize trends and comparisons across plans and plan versions.
- New summary: Waterfall analyses, trend analyses and plan comparisons, previously set up in the classic interface, can now be configured on the Comparison tab of Redwood planning tables and graphs.
- Reason: Summary only described the previous behavior.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/demand26c/26C-demand-wn-f45797.htm

## 26B changes

### 26B-f43384@fins26b · Landed Cost Line Classification of Payables Invoices from File-Based Data Import
- Family / product: Financials · Financials · Payables Invoice Processing
- Rating: **high → medium**
- Old summary: Designate invoice lines in the Payables Invoice Import Spreadsheet to link landed cost charge references, helping Payables users easily mark them as landed costs during bulk processing.
- New summary: The Payables Invoice Import spreadsheet gets a Landed Cost Enabled flag per invoice line. Lines set to Y go to Landed Cost Management for variance calculation and allocation. The column is hidden and blank by default, so existing imports are unchanged.
- Reason: Optional, hidden column; existing imports don't change. Medium rather than low because it touches an import template.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43384.htm

### 26B-f43498@fins26b · Payroll Encumbrance and Liquidation
- Family / product: Financials · Financials · Planning and Budgeting
- Rating: **high → low**
- Reason: Needs encumbrance accounting enabled and configured for the payroll ledger, plus the Calculate Payroll Encumbrances flow; nobody gets it by default. (Oracle rates it larger scale.)
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43498.htm

### 26B-f43676@fins26b · Account Alias for Joint Venture Accounts
- Family / product: Financials · Financials · Joint Venture Settlement
- Rating: **medium → low**
- Old summary: Use account aliases when specifying accounts in the following Joint Venture Management applications: Instead of entering the actual account segment values that make up an account, users can select from a list of account aliases when specifying an account.
- New summary: Joint Venture Management pages (partner contributions, source transactions, JV definitions, ownership assignment rules and overhead methods) now let you pick an account alias instead of typing every account segment.
- Reason: Minor data-entry aid. Summary ended with 'the following ... applications:' and no list.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43676.htm

### 26B-f43286@fins26b · Accounting for Multiple Partner Contributions in Stakeholder Billing
- Family / product: Financials · Financials · Joint Venture Settlement
- Rating: medium (unchanged)
- Old summary: Generate separate accounting entries when billing stakeholders, if the bill includes distributions funded by partner contributions with different accounts. A Receivables invoice from Joint Venture Management showing separate partner contribution lines – Invoice Lines section.
- New summary: When a stakeholder bill includes distributions funded by partner contributions with different accounts, Joint Venture Management now creates a separate accounting entry and invoice line for each partner contribution.
- Reason: Summary included a screenshot caption.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43286.htm

### 26B-f43307@fins26b · Automated Revenue Recognition for Sales Invoices with Prepayment Applications
- Family / product: Financials · Financials · Receivables Invoice Processing
- Rating: medium (unchanged)
- Old summary: Generate revenue schedules on the standard sales invoice lines of sales invoices that also contain prepayment application lines. Assign invoicing rules and revenue scheduling rules to the standard lines to automate revenue recognition.
- New summary: Sales invoices that include prepayment application lines can now have revenue schedules on their standard lines, using invoicing and revenue scheduling rules. The prepayment application lines themselves now default to the Immediate revenue scheduling rule.
- Reason: Added Oracle's note that prepayment lines now default to Immediate (an automatic change).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43307.htm

### 26B-f43446@fins26b · Deep Links for Budget Entries and Budgetary Control Balances
- Family / product: Financials · Financials · Planning and Budgeting
- Rating: **medium → low**
- Reason: Minor navigation aid (deep links from reports and dashboards).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43446.htm

### 26B-f43423@fins26b · Lease Payables Processing for Approved Payments
- Family / product: Financials · Financials · Asset Acquisition, Maintenance, and Lease
- Rating: **medium → low**
- Reason: Optional new parameter on the Expense Lease Payments process; existing scheduling unchanged.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43423.htm

### 26B-f43422@fins26b · Lease Transactions and Balances Report Improvements
- Family / product: Financials · Financials · Asset Acquisition, Maintenance, and Lease
- Rating: **medium → low**
- Reason: Reporting-only.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43422.htm

### 26B-f43159@fins26b · Receivables Invoice Installment Creation Using a REST API
- Family / product: Financials · Financials · Receivables Invoice Processing
- Rating: **medium → low**
- Reason: Optional new REST action; nothing changes for users.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43159.htm

### 26B-f43455@fins26b · Service Excellence Continuing Investments
- Family / product: Financials · Financials · Performance and Stability
- Rating: medium (unchanged)
- Old summary: Our ongoing investment in service excellence has a focus on overall usability, resiliency, performance, and security. This work is based on monitoring performance trends, reviewing common use patterns, analyzing service requests, and participating in many discussions with customers.
- New summary: A bundle of small usability, resiliency, performance and security fixes across Financials, for example an optional control that stops users deleting global intercompany invoices from the Payables Correct Import Errors spreadsheet. Check Oracle's page for the full list.
- Reason: Summary was Oracle boilerplate that said nothing about what changed.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43455.htm

### 26B-f43735@fins26b · Supplier and Customer Default Trading Partner TAS Update
- Family / product: Financials · Financials · U.S. Federal Treasury Reporting and Interfaces
- Rating: **medium → low**
- Reason: U.S. Federal Financials only, and runs through a process you schedule.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43735.htm

### 26B-f43734@fins26b · System for Award Management Import for Customers
- Family / product: Financials · Financials · U.S. Federal Treasury Reporting and Interfaces
- Rating: **medium → low**
- Old summary: Use imported System for Award Management (SAM) trading partner data to automatically create customer records. This process involves: Previously, federal agencies could only manage SAM supplier data.
- New summary: U.S. federal agencies can now create customer records from imported System for Award Management (SAM) data, not just supplier records.
- Reason: U.S. Federal Financials only. Summary was garbled ('This process involves: Previously...').
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43734.htm

### 26B-f43681@risk26b · New Advanced Access Requests Subject Area
- Family / product: Financials · Risk Management · Transactional Business Intelligence for Risk Management
- Rating: **medium → low**
- Reason: Reporting-only: a new OTBI subject area.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/risk26b/26B-risk-wn-f43681.htm

### 26B-f43543@fins26b · Japanese Corporate Tax Schedule 16 Reports Compliance
- Family / product: Financials · Financials · Legislative Updates
- Rating: low (unchanged)
- Old summary: Comply with the National Tax Agency's updated templates for the Japanese Corporate Tax Schedule 16 reports. The following enhancements have been implemented in the Schedule 16 reports for Japan:
- New summary: The Japanese Corporate Tax Schedule 16 reports follow the National Tax Agency's updated templates: they can show global descriptive flexfields from Add Asset and Adjust Asset, use the revised era name and include asset category descriptions.
- Reason: Summary ended in a colon.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43543.htm

### 26B-f44411@fins26b · Cash Processing from Bank Statements and Remittance Advices
- Family / product: Financials · Financials · Cash Processing Agent
- Rating: low (unchanged)
- Old summary: Bank Statement and Remittance Advices Processing enhancements extend Oracle’s broader investment toward Cash Processing Agent–driven capabilities, advancing a more automated and connected approach to cash processing within Receivables and Cash Management workflows.
- New summary: Receipts can now be created automatically from bank statement lines, and remittance advices in several formats are read and matched to receipts in one flow. In 26B it's for early adopters only, enabled through a service request.
- Reason: Summary was vague; added that it's early-adopter only via a service request.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f44411.htm

### 26B-f43398@hure-26b · Ability to Enable Guided Journeys for Individual Sections in Activity Centers
- Family / product: HCM · Human Resources · Workforce Directory Management
- Rating: **high → low**
- Old summary: The Guided Journey experience in the My Activity Center, Team Activity Center, and the Person Activity Center has been enhanced in the following ways: The streamlined Guided Journey experience greatly enhances the ability to convey the purpose and specifics of the different sections of the activity centers.
- New summary: In My, Team and Person Activity Centers, the communications and guided journey banners are combined into one, and guided journeys can now be set up for individual sections (in Visual Builder Studio).
- Reason: Needs guided journey page properties configured in Visual Builder Studio. Summary was garbled ('enhanced in the following ways:' with no list).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/hure-26b/26B-hr-wn-f43398.htm

### 26B-f44367@hure-26b · Approval Enforcement for Connections Photo Changes
- Family / product: HCM · Human Resources · Workforce Directory Management
- Rating: **high → medium**
- Old summary: Photo changes (upload, edit, and delete) initiated from the waterfall view in Connections are subject to the same Change Photo approval rule that already applies to Personal Details.
- New summary: If you've set up a Change Photo approval rule, photo uploads, edits and deletes made from Connections now go through the same approval as Personal Details: the new photo shows as pending until it's approved.
- Reason: Only changes anything if a Change Photo approval rule is configured. Summary reworded.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/hure-26b/26B-hr-wn-f44367.htm

### 26B-f43666@hure-26b · Enhanced AI-Generated Comments for Redwood Employment Processes
- Family / product: HCM · Human Resources · Employment
- Rating: **high → medium**
- Old summary: Assignment Notes in Redwood Employment processes now offer enhanced controls that lets users customize the AI generated content to better suit their needs. Tone control, Length control, and Rewrite options in Generate button
- New summary: AI-generated assignment notes in Redwood employment processes get tone (Engaging or Formal), length (Summarize or Expand) and Rewrite controls.
- Reason: Visible to HR users but contained to one optional AI field. Summary trailed off into a caption.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/hure-26b/26B-hr-wn-f43666.htm

### 26B-f43664@hure-26b · Enhanced Guided Journey Parameters for Redwood Employment Processes
- Family / product: HCM · Human Resources · Employment
- Rating: **high → low**
- Reason: Only matters if you configure guided journey tasks that use the new parameters.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/hure-26b/26B-hr-wn-f43664.htm

### 26B-f43513@hure-26b · New Redwood Process to Change Worker Type
- Family / product: HCM · Human Resources · Employment
- Rating: high (unchanged)
- Old summary: You can now use the Redwood Change Worker Type process to seamlessly convert workers from one type to another using a single guided flow. This eliminates the need to terminate an existing work relationship and create a new one, reducing duplicate data entry and maintaining continuity of worker information.
- New summary: A new Redwood Change Worker Type process converts a worker from one type to another (for example contingent worker to employee) in a single guided flow, instead of terminating the work relationship and creating a new one.
- Reason: Reworded. High kept: changes how HR handles worker type conversions.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/hure-26b/26B-hr-wn-f43513.htm

### 26B-f43339@hure-26b · Redwood Experience for Actions Reasons Page
- Family / product: HCM · Human Resources · Employment
- Rating: **high → medium**
- Old summary: Enrich the user experience with the Actions Reasons page developed using the Redwood tool set. The page is built from the ground up using Visual Builder Studio (VBS) to give you a unique experience of Oracle applications.
- New summary: The Action Reasons setup page moves to Redwood: create and edit action reasons, translate text with the Translation Editor, and control the page with new Visual Builder Studio properties.
- Reason: Setup page for HR admins only, so contained. Summary was marketing text that didn't say what changed.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/hure-26b/26B-hr-wn-f43339.htm

### 26B-f43340@hure-26b · Redwood Experience for Assignment Statuses Page
- Family / product: HCM · Human Resources · Employment
- Rating: **high → medium**
- Old summary: Enrich the user experience with the Assignment Statuses page developed using the Redwood tool set. The page is built from the ground up using Visual Builder Studio (VBS) to give you a unique experience of Oracle applications.
- New summary: The Assignment Statuses setup page moves to Redwood: create assignment statuses and translate text with the Translation Editor.
- Reason: Setup page for HR admins only, so contained. Summary was marketing text that didn't say what changed.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/hure-26b/26B-hr-wn-f43340.htm

### 26B-f43338@hure-26b · Redwood Experience for Configure Actions Page
- Family / product: HCM · Human Resources · Employment
- Rating: **high → medium**
- Old summary: Enrich the user experience with the Configure Actions page developed using the Redwood tool set. The page is built from the ground up using Visual Builder Studio (VBS) to give you a unique experience of Oracle applications.
- New summary: The Configure Actions setup page moves to Redwood: create actions, link existing reasons, translate text with the Translation Editor, and use new Visual Builder Studio page properties.
- Reason: Setup page for HR admins only, so contained. Summary was marketing text that didn't say what changed.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/hure-26b/26B-hr-wn-f43338.htm

### 26B-f43341@hure-26b · Redwood Experience for Configure Seniority Dates Page
- Family / product: HCM · Human Resources · Employment
- Rating: **high → medium**
- Old summary: Enrich the user experience with the Configure Seniority Dates page developed using the Redwood tool set. The page is built from the ground up using Visual Builder Studio (VBS) to give you a unique experience of Oracle applications.
- New summary: The Configure Seniority Dates setup page moves to Redwood: create and edit seniority date rules, with new Visual Builder Studio properties to hide the Add and Delete buttons.
- Reason: Setup page for HR admins only, so contained. Summary was marketing text that didn't say what changed.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/hure-26b/26B-hr-wn-f43341.htm

### 26B-f43396@hure-26b · Update Checkin Page is Displayed From Talent View in Team Activity Center
- Family / product: HCM · Human Resources · Workforce Directory Management
- Rating: **high → low**
- Old summary: In the 'Talent' view on Team Activity Center, Last checkin date opens the Update Checkin page
- New summary: In the Talent view of Team Activity Center, the last check-in date now opens that check-in for updating, and if there's no check-in you can create one.
- Reason: Minor navigation change. Summary reworded.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/hure-26b/26B-hr-wn-f43396.htm

### 26B-f43906@payr-26b · Monthly DSN
- Family / product: HCM · Payroll · Payroll for France
- Rating: high (unchanged)
- Old summary: French legal employers have the obligation of reporting each month payroll information for all their employees. For information on the setup and configuration, see:
- New summary: French payroll can now produce the monthly DSN (Déclaration Sociale Nominative), the payroll report French employers must file every month. Setup is described in Oracle's France payroll technical brief (KB183664).
- Reason: Summary was cut off at 'see:'. High kept: statutory payroll reporting.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/payr-26b/26B-payroll-wn-f43906.htm

### 26B-f43498@payr-26b · Payroll Encumbrance and Liquidation
- Family / product: HCM · Payroll · Global Payroll
- Rating: **high → low**
- Reason: Needs encumbrance accounting enabled and configured for the payroll ledger, plus the Calculate Payroll Encumbrances flow; nobody gets it by default. (Oracle rates it larger scale.)
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/payr-26b/26B-payroll-wn-f43498.htm

### 26B-f43648@payr-26b · Redwood Experience: Personal Payment Method Enhancements
- Family / product: HCM · Payroll · Global Payroll
- Rating: high (unchanged)
- Old summary: You can now manage employee payment methods with more flexibility, while keeping payroll data consistent. Reorder payment methods across different start dates You can change the order of an employee’s payment methods when they have multiple payment methods with different start dates (for example, one starting 1 January and another starting 1 June).
- New summary: Employees and admins can now reorder personal payment methods that have different start dates, and employees can see payment methods that start in the future.
- Reason: Summary ran a heading into the text. High kept: touches how employees are paid.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/payr-26b/26B-payroll-wn-f43648.htm

### 26B-f43509@payr-26b · Statutory Neonatal Care Leave & Pay
- Family / product: HCM · Payroll · Payroll for the United Kingdom
- Rating: high (unchanged)
- Old summary: You can now create absences for neonatal care leave and if they qualify and make statutory payments – subject to eligibility based on average weekly earnings (AWE) as per legislation laid down in April 2025.
- New summary: UK payroll now supports Statutory Neonatal Care leave and pay (legislation from April 2025): a new Neonatal Care absence type, accrual of up to 12 weeks' leave, and statutory payments for employees who qualify on average weekly earnings.
- Reason: Summary grammar was garbled.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/payr-26b/26B-payroll-wn-f43509.htm

### 26B-f46411@payr-26b · Tax Groups
- Family / product: HCM · Payroll · Payroll for the United States
- Rating: high (unchanged)
- Old summary: With the introduction of tax groups, we have made it easier for you to track state and federal limit taxes across multiple tax reporting units (TRUs) under a parent PSU.
- New summary: A new tax group level between the payroll statutory unit and its tax reporting units tracks state and federal limit taxes, so balances don't need transferring when an employee moves between TRUs that share wage and tax limits.
- Reason: Reworded and spelled out the acronyms.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/payr-26b/26B-payroll-wn-f46411.htm

### 26B-f43768@wohs-26b · New Metrics in Incidents Real Time Subject Area
- Family / product: HCM · Workforce Health and Safety · Transactional Business Intelligence for Health and Safety
- Rating: **high → low**
- Reason: Reporting-only: new metrics in an OTBI subject area. (Oracle rates it larger scale.)
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/wohs-26b/26B-workforce-health-wn-f43768.htm

### 26B-f43865@amg-26b · Change history turned off for creation record
- Family / product: HCM · Absence Management · Absence Management
- Rating: **medium → low**
- Old summary: Previously, when a record was created, the Absence Categories and Absence Reasons Redwood setup pages displayed the change details listing every field that was populated.
- New summary: On the Redwood Absence Categories and Absence Reasons setup pages, Change Details now appears only for updated records, not newly created ones.
- Reason: Minor. Summary only described the old behavior.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/amg-26b/26B-absence-mgmt-wn-f43865.htm

### 26B-f43855@amg-26b · Default Workday Definitions from Work Patterns
- Family / product: HCM · Absence Management · Absence Management
- Rating: **medium → low**
- Reason: Optional: the primary assignment is still checked first, so nothing changes unless you put workday definitions on work patterns.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/amg-26b/26B-absence-mgmt-wn-f43855.htm

### 26B-f43857@amg-26b · Event Processing for Front-loaded Accrual Plans
- Family / product: HCM · Absence Management · Absence Management
- Rating: **medium → low**
- Reason: Only applies if you associate HCM events with a front-loaded accrual plan.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/amg-26b/26B-absence-mgmt-wn-f43857.htm

### 26B-f43859@amg-26b · New Return Variable for the Entitlement Formula
- Family / product: HCM · Absence Management · Absence Management
- Rating: **medium → low**
- Reason: Minor fast formula option.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/amg-26b/26B-absence-mgmt-wn-f43859.htm

### 26B-f43856@amg-26b · New Unpaid Break Display Field
- Family / product: HCM · Absence Management · Absence Management
- Rating: medium (unchanged)
- Old summary: The Redwood pages for absence entry and calendar now display unpaid break information when a worker’s absence is entered. Let’s assume a worker’s 12 hour shift starts from 7AM to 7PM, and it includes a 30 minute unpaid break.
- New summary: Redwood absence entry and calendar pages now show the unpaid break deducted from an absence. For example, a full 12-hour shift with a 30-minute unpaid break counts as 11.5 hours, and the break is shown.
- Reason: Reworded.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/amg-26b/26B-absence-mgmt-wn-f43856.htm

### 26B-f42727@comp-26b · HDL Support for Salary Basis Calculation Type Simple Component and Other Miscellaneous
- Family / product: HCM · Compensation · Compensation
- Rating: **medium → low**
- Old summary: 1. Load and manage salary basis records that use the Simple Component calculation type using HCM Data Loader.
- New summary: Salary basis records with the Simple Component calculation type can now be loaded with HCM Data Loader, and simple components work on Redwood offer pages and in Line Manager Change Salary and Salary History.
- Reason: Optional additions; nothing changes for existing salary bases. Summary started with '1.' and was cut off.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/comp-26b/26B-compensation-wn-f42727.htm

### 26B-f42379@comp-26b · Hide or Show Component Columns in Salary Section of Recruiting pages
- Family / product: HCM · Compensation · Compensation
- Rating: **medium → low**
- Reason: Configured through business rules; nothing changes by default.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/comp-26b/26B-compensation-wn-f42379.htm

### 26B-f43878@hcom-26b · Business Object Enhancements
- Family / product: HCM · HCM Common · HCM Data Loader
- Rating: medium (unchanged)
- Old summary: Extend your data loading capabilities with these enhanced business objects: This business object has introduced a new component in the hierarchy:
- New summary: HCM Data Loader business objects gain new components and attributes, for example simple components on Salary Basis and an unpaid break duration on Absence Entry. Check Oracle's list against your HDL files.
- Reason: Summary ended in two colons with no content.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/hcom-26b/26B-hcm-common-wn-f43878.htm

### 26B-f42915@gtm26b · AES Filing Enhancements
- Family / product: Logistics (OTM/GTM/WMS) · Global Trade Management · Customs Management
- Rating: medium (unchanged)
- Old summary: This feature enhances the AES Filing capability to address recent regulatory updates affecting the X12.601 Customs and Border Protection (CBP) - Export Shipment Information specification.
- New summary: AES filing follows the latest CBP export shipment (X12.601) changes: the SPP license exception for Syria (code C78, for EAR99 items) is added to GTM's default AES code mapping.
- Reason: Added the actual change.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/gtm26b/26B-gtm-wn-f42915.htm

### 26B-f43365@otm26b · Bulk Secondary Charge Shipments Creation Action
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · Secondary Charge Shipments
- Rating: **medium → low**
- Reason: New optional Process Management action; the existing UI action is unchanged.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/otm26b/26B-otm-wn-f43365.htm

### 26B-f43360@otm26b · Documents for Shipment Ship Unit
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · Document Management
- Rating: **medium → low**
- Old summary: This feature extends the objects that support document functionality to include the Shipment Ship Units (SSU). In addition to the UI Documents actions, this feature also provides related document Agent Actions to automate your Shipment Ship Unit document processes..
- New summary: Shipment Ship Units now support documents: add, upload, link, copy, generate and view documents, plus matching agent actions to automate document handling (for example packing lists and labels).
- Reason: New optional actions. Summary had a double full stop.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/otm26b/26B-otm-wn-f43360.htm

### 26B-f43866@otm26b · LNM - Updates on SCP - OTM/LNM Integration
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · Logistics Network Modeling
- Rating: medium (unchanged)
- Old summary: Following enhancements have been delivered as part of 26B on SCP - OTM Integration: User can terminate the plan and then rerun the same plan.
- New summary: Changes to the Supply Chain Planning to OTM integration in Logistics Network Modeling: a new property caps the orders pulled per plan (default 10,000, with an error above it), only one SCP plan can be pulled at a time, and a running pull can be terminated and rerun.
- Reason: Summary was garbled. Medium kept: the new 10,000-order cap can cause errors on large plans.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/otm26b/26B-otm-wn-f43866.htm

### 26B-f43557@otm26b · Merge Shipments - Reuse Action
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · Planning Actions
- Rating: **medium → low**
- Reason: New optional planning action for one multi-leg scenario.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/otm26b/26B-otm-wn-f43557.htm

### 26B-f43828@otm26b · Mobile - Custom Sort-By Fields for Date and Number
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · Mobile
- Rating: **medium → low**
- Reason: Needs mobile layout configuration.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/otm26b/26B-otm-wn-f43828.htm

### 26B-f43829@otm26b · Mobile - Planner Flow Dock Appointment Scheduling
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · Mobile
- Rating: **medium → low**
- Reason: Hidden by default; needs mobile layout changes to switch on.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/otm26b/26B-otm-wn-f43829.htm

### 26B-f43713@otm26b · Override Calendar Action
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · Calendars
- Rating: **medium → low**
- Reason: Minor convenience (multi-select calendar override action).
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/otm26b/26B-otm-wn-f43713.htm

### 26B-f43832@otm26b · TOI Extension – Invoice, Location Attributes, Local Dates
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · Transportation Intelligence
- Rating: **medium → low**
- Reason: Reporting-only: new fields in an OTBI subject area.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/otm26b/26B-otm-wn-f43832.htm

### 26B-f44038@otm26b · Task Height Parameter for Gantts
- Family / product: Logistics (OTM/GTM/WMS) · Transportation Management · Enhanced Workbench Gantt
- Rating: **medium → low**
- Reason: Minor display setting.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/otm26b/26B-otm-wn-f44038.htm

### 26B-f44028@wms26b · Additional Support for Purge Script Handling
- Family / product: Logistics (OTM/GTM/WMS) · Warehouse Management · WMS Common
- Rating: medium (unchanged)
- Old summary: The purge process helps improve performance by optimizing data retention and increasing storage efficiency. It enables you to remove older, no-longer-needed records in a controlled and predictable way.
- New summary: The WMS purge script now also deletes older history records, for example shipped serial number history after 3 years and pallet history after 6 months. Check any reports or integrations that rely on that history.
- Reason: Summary described purging in general, not what's new. Medium kept: automatic data deletion.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/wms26b/26B-wms-wn-f44028.htm

### 26B-f45826@wms26b · Cancel Carton Action to Support Cancelling Packed OBLPNs in Bulk
- Family / product: Logistics (OTM/GTM/WMS) · Warehouse Management · Inventory Operations
- Rating: medium (unchanged)
- Old summary: Today, WMS allows you to multi-select a OBLPN (Outbound Created status) and cancel in bulk from OBLPN UI. Also, users could also cancel a packed OBLPN from the Redwood mobile through a one scan, slowing the outbound process.
- New summary: The Cancel Cartons action on the OBLPN screen can now cancel picked and packed OBLPNs in bulk, not just those in Outbound Created status.
- Reason: Summary described the old behavior.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/wms26b/26B-wms-wn-f45826.htm

### 26B-f46283@wms26b · Display LPN Type Attachment in Inbound and Outbound Transaction
- Family / product: Logistics (OTM/GTM/WMS) · Warehouse Management · WMS Common
- Rating: **medium → low**
- Old summary: Today, Warehouses require users to move across multiple screens to confirm whether an IBLPN/OBLPN has attachments tied to its LPN type, which slows processing and adds unnecessary effort.
- New summary: A new LPN Type Attachments column on the Item Inventory by LPN screen shows how many attachments an LPN's type has, with a link to view them. It's hidden until you add it in grid settings.
- Reason: Hidden by default. Summary described the problem, not the feature.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/wms26b/26B-wms-wn-f46283.htm

### 26B-f44434@wms26b · Expand Audit OBLPN to Handle Mixed UOMs
- Family / product: Logistics (OTM/GTM/WMS) · Warehouse Management · Outbound Logistics
- Rating: medium (unchanged)
- Old summary: In warehouse outbound operations, OBLPNs can be created using combine or repack OBLPNs to improve space utilization and reduce freight cost. As a result, a single OBLPN can include allocations in different units of measure (UOM), such as cases, packs, and units.
- New summary: The mobile Outbound Audit transaction can now audit OBLPNs that hold allocations in mixed units of measure (cases, packs and units). Before, those OBLPNs couldn't be audited.
- Reason: Summary was background only.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/wms26b/26B-wms-wn-f44434.htm

### 26B-f44435@wms26b · Generate Cycle Count Info on Rejection of MHE Triggered Counts
- Family / product: Logistics (OTM/GTM/WMS) · Warehouse Management · Inventory Operations
- Rating: medium (unchanged)
- Old summary: Rejecting cycle count adjustments creates new cycle count tasks either for the entire location or for specific items, depending on configuration. For MHE-driven cycle counts (counts passed via the Cycle Count List API), the originating MHE must be notified when a recount is needed.
- New summary: When you reject a cycle count that came from automated material handling equipment (MHE) through the Cycle Count List API, the recount task is now sent back to that MHE so it can do the recount.
- Reason: Summary was background only.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/wms26b/26B-wms-wn-f44435.htm

### 26B-f44430@wms26b · Improvements to Alternate Location Determination During Picking
- Family / product: Logistics (OTM/GTM/WMS) · Warehouse Management · Outbound Logistics
- Rating: medium (unchanged)
- Old summary: In busy warehouse environments, the system-directed pick location may not be an ideal location to pick at the moment of execution due to operational constraints.
- New summary: The Ctrl-F Alternate Location option during picking now lists all eligible locations with available inventory, and keeps the allocation when no eligible alternate is available.
- Reason: Summary described the problem, not the change.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/logistics/26b/wms26b/26B-wms-wn-f44430.htm

### 26B-f43892@proc26b · Redwood: Add Ad Hoc Approvers on Purchasing Documents at Additional Positions
- Family / product: Procurement · Procurement · Purchasing
- Rating: medium (unchanged)
- Old summary: Add ad hoc approvers on purchase orders and purchase agreements at additional positions.With this update, you can now add and manage ad hoc approvers at additional positions in the default approval hierarchy when submitting purchase orders or purchase agreements for approval in the Redwood user application.
- New summary: In Redwood Purchasing, you can now add ad hoc approvers at more points in the approval hierarchy when submitting POs and agreements: at the start of the task, or the start or end of a stage.
- Reason: Summary ran two sentences together ('positions.With').
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/proc26b/26B-procurement-wn-f43892.htm

### 26B-f42903@proc26b · Redwood: Duplicate a Purchase Order or Its Lines When Editing the Purchase Order
- Family / product: Procurement · Procurement · Purchasing
- Rating: **medium → low**
- Old summary: Duplicate a purchase order or its lines when editing the purchase order using a Redwood page. These screen captures illustrate the feature.
- New summary: In Redwood Purchasing, you can duplicate a purchase order or its lines while editing it, and duplicate change order lines, including all their schedules and distributions.
- Reason: Minor convenience. Summary referred to screenshots.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/proc26b/26B-procurement-wn-f42903.htm

### 26B-f42782@proc26b · Redwood: Navigate to Source Agreements from a Purchase Order
- Family / product: Procurement · Procurement · Purchasing
- Rating: **medium → low**
- Reason: Minor: the source agreement becomes a link.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/proc26b/26B-procurement-wn-f42782.htm

### 26B-f42957@proc26b · Redwood: Search When Editing Purchase Orders
- Family / product: Procurement · Procurement · Purchasing
- Rating: **medium → low**
- Reason: Minor: search within large POs while editing.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/proc26b/26B-procurement-wn-f42957.htm

### 26B-f42859@proc26b · Redwood: Support Business Rules for Business Classifications in Supplier Registration
- Family / product: Procurement · Procurement · Supplier Model
- Rating: **medium → low**
- Old summary: Supplier registration can have unique requirements based on factors like country and industry. If the information requested in the registration flow isn't tailored using these types of factors, it can be confusing and result in higher support costs with lower registration success rates.
- New summary: Visual Builder Studio business rules now cover the Business Classifications page of supplier registration, so you can make fields required, read-only or hidden by criteria such as country or industry.
- Reason: Needs business rules configured. Summary described the need, not the feature.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/proc26b/26B-procurement-wn-f42859.htm

### 26B-f42962@proc26b · Redwood: Use Additional Capabilities in Negotiations
- Family / product: Procurement · Procurement · Sourcing
- Rating: medium (unchanged)
- Old summary: Additional capabilities are now available in Oracle Sourcing Redwood UIs: You can now set and view minimum decrement value for each line in an auction. This ensures bids are lowered by at least by specified amount or percentage for each line when suppliers revise responses.
- New summary: More Sourcing features in the Redwood pages: export and import requirements by spreadsheet for draft negotiations, view requirement details from scoring and analysis pages, response revision settings, and a minimum decrement per line in auctions.
- Reason: Summary's sentences were out of order.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/proc26b/26B-procurement-wn-f42962.htm

### 26B-f42902@proc26b · Redwood: Use Extensibility Capabilities
- Family / product: Procurement · Procurement · Purchasing
- Rating: **medium → low**
- Old summary: Use the extensibility capabilities supported in the Redwood Purchasing application. With this update, you can use extensibility capabilities for these functionalities: Default purchase order and purchase agreement attributes using business rules
- New summary: Redwood Purchasing extensibility now covers defaulting PO and agreement attributes with business rules, personalizing attachments and default attachment categories, project DFFs on distributions, and the View PDF action.
- Reason: Needs Visual Builder Studio work. Summary was cut off.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/proc26b/26B-procurement-wn-f42902.htm

### 26B-f42836@proc26b · Redwood: View Budget Details with Funds Check Results
- Family / product: Procurement · Procurement · Purchasing
- Rating: **medium → low**
- Reason: Minor: an extra Budget view in funds check results.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/proc26b/26B-procurement-wn-f42836.htm

### 26B-f43469@proc26b · Selected Procurement Contracts and Enterprise Contracts Bug Fixes in This Update
- Family / product: Procurement · Procurement · Procurement Contracts
- Rating: medium (unchanged)
- Old summary: This update includes some bug fixes that can change the way Oracle Procurement Contracts and Enterprise Contracts works. This isn't a full list of all the bug fixes in this update.
- New summary: Oracle's list of 26B Procurement Contracts and Enterprise Contracts fixes that change behavior. For example, purchasing documents for large contracts can now be created with a scheduled process instead of only in real time.
- Reason: Summary was boilerplate that didn't say what changed.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/proc26b/26B-procurement-wn-f43469.htm

### 26B-f43144@proc26b · Selected Purchasing Bug Fixes in This Update
- Family / product: Procurement · Procurement · Purchasing
- Rating: medium (unchanged)
- Old summary: This update includes some bug fixes that can change the way Oracle Purchasing works. This isn't a full list of all the bug fixes in this update.
- New summary: Oracle's list of 26B Purchasing fixes that change behavior, for example document history is now shown for withdrawn and rejected POs on Redwood pages, and the expiring, overutilized and underutilized agreement filters no longer return draft agreements.
- Reason: Summary was boilerplate that didn't say what changed.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/proc26b/26B-procurement-wn-f43144.htm

### 26B-f43178@proc26b · Use Supply Chain Orchestration to Support Contract Manufacturing for Process Manufacturing In Your Plan-to-Produce Flows
- Family / product: Procurement · Procurement · Supply Chain Orchestration
- Rating: **medium → low**
- Reason: Only applies if you set up contract manufacturing for process manufacturing; no change to existing flows.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/proc26b/26B-procurement-wn-f43178.htm

### 26B-f43231@ppm26b · Labor Commitment Integration from Third-Party Payroll Sources
- Family / product: Project Management · Project Management · Cost Management and Control
- Rating: **high → medium**
- Old summary: Automatically create and distribute labor commitment costs to projects by importing payroll encumbrance data from external payroll systems. This solution uses the existing labor distribution flow, ensuring ongoing budget consumption and applying budgetary controls to reserve funds for anticipated payroll expenses.
- New summary: Labor commitments can now be imported from a third-party payroll's encumbrance data and distributed to projects through the existing labor distribution flow, reserving budget for expected payroll costs and liquidating it as actuals post. Pay elements and labor schedules must be set up first.
- Reason: Nothing happens until you set up pay elements and labor schedules and import data. Medium rather than low because it feeds project costs and budgetary control.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/ppm26b/26B-ppm-wn-f43231.htm

### 26B-f43229@ppm26b · Labor Costing by Project Role
- Family / product: Project Management · Project Management · Cost Management and Control
- Rating: **high → medium**
- Reason: Applies only once you define project role cost rate schedules and assign them to business units and cost organizations. Medium because it then changes labor costing.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/ppm26b/26B-ppm-wn-f43229.htm

### 26B-f43309@ppm26b · Action History for Bill Transactions
- Family / product: Project Management · Project Management · Billing and Revenue Management
- Rating: **medium → low**
- Reason: Minor: a read-only audit trail of bill transaction actions.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/ppm26b/26B-ppm-wn-f43309.htm

### 26B-f43593@inv26b · Calculate the Costs of Standard Costed Configured Items On Demand
- Family / product: Supply Chain & Manufacturing · Inventory Management · Cost Management
- Rating: **high → medium**
- Reason: Optional: applies when you run a configured-item cost scenario with rollup scope All Items. Medium because it changes published standard costs.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/inv26b/26B-inventory-wn-f43593.htm

### 26B-f43062@inv26b · Redwood: Perform Lot Split, Merge, or Translate Transactions Using a Redwood Page
- Family / product: Supply Chain & Manufacturing · Inventory Management · Inventory Management
- Rating: **high → medium**
- Old summary: When managing goods under lot control, various situations may require you to split, merge, or otherwise adjust the lot assignments for certain items. For instance, if a weather incident damages your warehouse and only part of a lot is affected, the compromised portion might still be suitable for some manufacturing uses but not others.
- New summary: Lot split, merge and translate transactions can now be done on a Redwood page, for example splitting off the damaged part of a lot under a new lot number, or merging several lots into one.
- Reason: New Redwood page for one transaction type; contained. Summary was background only.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/inv26b/26B-inventory-wn-f43062.htm

### 26B-f43065@inv26b · Redwood: Review and Select Lot and Serial Numbers from an ASN or Transfer Order during Receipt
- Family / product: Supply Chain & Manufacturing · Inventory Management · Receiving
- Rating: high (unchanged)
- Old summary: When you receive lot or serial control goods with lot or serial numbers mentioned in an Advance Shipment Notice (ASN) or transfer order, it's important to review and select specific lot or serial numbers, instead of automatically accepting all the numbers provided.
- New summary: When you receive lot- or serial-controlled goods against an ASN or transfer order, you can now review and pick the specific lot and serial numbers you're receiving, instead of accepting every number on the document.
- Reason: Summary described the need. High kept: changes the receiving flow.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/inv26b/26B-inventory-wn-f43065.htm

### 26B-f43071@inv26b · Redwood: Use the All Organizations Option When Selecting an Organization
- Family / product: Supply Chain & Manufacturing · Inventory Management · Inventory Management
- Rating: **high → medium**
- Old summary: Certain roles within your organization, such as supply chain operations managers or regional managers, often require access to data across multiple inventory organizations to effectively oversee and coordinate activities at various locations.
- New summary: Many Inventory Management pages now offer an All organizations option in the organization chooser, so managers can see data across every organization they have access to.
- Reason: Visible convenience, no process change. Summary was background only.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/inv26b/26B-inventory-wn-f43071.htm

### 26B-f43586@inv26b · Track Costs for Parallel Work Order Operations Using Precedence Constraints
- Family / product: Supply Chain & Manufacturing · Inventory Management · Cost Management
- Rating: **high → low**
- Reason: Needs its parent opt-in feature (Operation Yield for process manufacturing work definitions) enabled first.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/inv26b/26B-inventory-wn-f43586.htm

### 26B-f43291@order26b · Redwood: Set Up Customer Pricing
- Family / product: Supply Chain & Manufacturing · Order Management · Pricing
- Rating: high (unchanged)
- Enablement: Automatically on → Opt-in, expires 26D
- Old summary: Use the new Customer Pricing page in the Pricing Administration work area to set up pricing differently according to each of your customer's unique requirements.
- New summary: A new Redwood Customer Pricing page in Pricing Administration lets you set prices and pricing rules for a customer, account or group of customers, with effective dates. It's an opt-in in 26B and, per Oracle's opt-in expiration list, becomes standard (switched on) in 26D.
- Reason: Added the opt-in status from Oracle's page and expiration list. High kept: pricing, and becomes standard in 26D.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/order26b/26B-order-mgmt-wn-f43291.htm

### 26B-f43397@plm26b · Selected Product Management Bug Fixes In This Update
- Family / product: Supply Chain & Manufacturing · Product Lifecycle Management · Product Management
- Rating: high (unchanged)
- Old summary: This update includes some bug fixes that can change the way Oracle Fusion Cloud Product Lifecycle Management works. This isn't a full list of all the bug fixes in this update.
- New summary: Oracle's list of 26B Product Lifecycle Management fixes that change behavior. For example, item revision attachments created or updated by import or REST now honor the needs-approval rule and create a change order.
- Reason: Summary was boilerplate. High kept: changes how imports and REST updates behave.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/plm26b/26B-plm-wn-f43397.htm

### 26B-f42994@sop26b · Redwood: Manage Levels and Attributes Using a New User Experience
- Family / product: Supply Chain & Manufacturing · Sales and Operations Planning · Demand Management
- Rating: **high → medium**
- Old summary: You can use the Levels and Attributes page to view and configure levels and attributes for dimension hierarchies. On this page, you can: Using this page, you can also search for records by dimension, hierarchy, and level.
- New summary: A Redwood Levels and Attributes page for planning dimension hierarchies: rename levels for tables and graphs, choose which member identifier to show, add or delete item and organization attributes, and search by dimension, hierarchy and level.
- Reason: Configuration page for planning admins; contained. Summary was garbled ('you can: Using this page').
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/sop26b/26B-sales-ops-wn-f42994.htm

### 26B-f42989@sop26b · Redwood: Manage Measures Using the Expression Builder and Measure Context
- Family / product: Supply Chain & Manufacturing · Sales and Operations Planning · Demand Management
- Rating: **high → medium**
- Reason: Enhancement to an existing Redwood configuration page for planning admins; contained.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/sop26b/26B-sales-ops-wn-f42989.htm

### 26B-f42994@scp26b · Redwood: Manage Levels and Attributes Using a New User Experience
- Family / product: Supply Chain & Manufacturing · Supply Planning · Supply Planning
- Rating: **high → medium**
- Old summary: You can use the Levels and Attributes page to view and configure levels and attributes for dimension hierarchies. On this page, you can: Using this page, you can also search for records by dimension, hierarchy, and level.
- New summary: A Redwood Levels and Attributes page for planning dimension hierarchies: rename levels for tables and graphs, choose which member identifier to show, add or delete item and organization attributes, and search by dimension, hierarchy and level.
- Reason: Configuration page for planning admins; contained. Summary was garbled ('you can: Using this page').
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/scp26b/26B-sc-planning-wn-f42994.htm

### 26B-f42989@scp26b · Redwood: Manage Measures Using the Expression Builder and Measure Context
- Family / product: Supply Chain & Manufacturing · Supply Planning · Supply Planning
- Rating: **high → medium**
- Reason: Enhancement to an existing Redwood configuration page for planning admins; contained.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/scp26b/26B-sc-planning-wn-f42989.htm

### 26B-f42994@demand26b · Redwood: Manage Levels and Attributes Using a New User Experience
- Family / product: Supply Chain & Manufacturing · demand26b · Demand Management
- Rating: **high → medium**
- Old summary: You can use the Levels and Attributes page to view and configure levels and attributes for dimension hierarchies. On this page, you can: Using this page, you can also search for records by dimension, hierarchy, and level.
- New summary: A Redwood Levels and Attributes page for planning dimension hierarchies: rename levels for tables and graphs, choose which member identifier to show, add or delete item and organization attributes, and search by dimension, hierarchy and level.
- Reason: Configuration page for planning admins; contained. Summary was garbled ('you can: Using this page').
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/demand26b/26B-demand-wn-f42994.htm

### 26B-f42989@demand26b · Redwood: Manage Measures Using the Expression Builder and Measure Context
- Family / product: Supply Chain & Manufacturing · demand26b · Demand Management
- Rating: **high → medium**
- Reason: Enhancement to an existing Redwood configuration page for planning admins; contained.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/demand26b/26B-demand-wn-f42989.htm

### 26B-f42980@demand26b · Redwood: Simulate Demand Using Additional Details
- Family / product: Supply Chain & Manufacturing · demand26b · Demand Management
- Rating: **high → medium**
- Reason: New tabs in an existing simulation drawer; visible but contained.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/demand26b/26B-demand-wn-f42980.htm

### 26B-f43079@mfg26b · Redwood: Execute Work Order Operations with Enhanced Options
- Family / product: Supply Chain & Manufacturing · Manufacturing · Manufacturing
- Rating: high (unchanged)
- Old summary: Execute work order operations using the Redwood UI with additional options and workflows, such as inspecting rejected quantities, viewing Transactional Item Attributes for work orders, and accessing sales order attachments within the UI.
- New summary: More options when executing work order operations on Redwood pages: inspect rejected quantities, see transactional item attributes, and upload attachments during execution. An opt-in in 26B that becomes standard in 26C.
- Reason: Added the opt-in status.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/mfg26b/26B-mfg-wn-f43079.htm

### 26B-f43095@mfg26b · Redwood: Pause and Resume Operations During Production Execution Without Workstations
- Family / product: Supply Chain & Manufacturing · Manufacturing · Manufacturing
- Rating: high (unchanged)
- Old summary: Flexibility in production execution is increasingly vital for modern manufacturing environments, especially those that operate without predetermined workstations.
- New summary: Operators can now start, pause (with a reason) and resume work order operations in flows without workstations, and run and stop times are tracked accurately. An opt-in in 26B that becomes standard in 26C.
- Reason: Summary described the need, not the feature.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/mfg26b/26B-mfg-wn-f43095.htm

### 26B-f43599@inv26b · Derive Receivables and Payables Accounts for External Trade Events Using Transaction Account Definition
- Family / product: Supply Chain & Manufacturing · Inventory Management · Supply Chain Financial Orchestration
- Rating: **medium → low**
- Old summary: Earlier, when you uploaded and processed intercompany transactions from Oracle subscriptions or external sources into Financial Orchestration to generate receivables and Payables invoices, you were required to set up the control accounts of receivables and Payables in Advanced Global Intercompany System (OAGIS) using the new external trade as a business flow in the financial agreement.
- New summary: Receivables and Payables accounts for external trade events in Supply Chain Financial Orchestration can now be derived with a Transaction Account Definition, not only from the control accounts on the financial agreement.
- Reason: Optional extra setup choice. Summary described the old setup.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/inv26b/26B-inventory-wn-f43599.htm

### 26B-f43594@inv26b · Enable Accurate Capture and Fiscal Processing for Prepayments Under the New Tax Regime
- Family / product: Supply Chain & Manufacturing · Inventory Management · Fiscal Document Capture
- Rating: medium (unchanged)
- Old summary: You can now record, tax, and track supplier prepayments against purchase orders before goods are received in Brazil’s standard procure-to-pay fiscal flows. With the new Prepayment fiscal flow for source document type Purchase Order , the system automatically associates and applies prepayments to final invoices, ensuring:
- New summary: In Brazil, a new Prepayment fiscal flow for purchase orders lets you record, tax and track supplier prepayments before goods arrive, and applies them to the final invoice.
- Reason: Summary ended in a colon.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/inv26b/26B-inventory-wn-f43594.htm

### 26B-f43598@inv26b · Generate Intercompany Events for Oracle Transportation Management Interface for Customer Drop Shipments
- Family / product: Supply Chain & Manufacturing · Inventory Management · Supply Chain Financial Orchestration
- Rating: **medium → low**
- Old summary: Financial Orchestration Transfer Prices REST resource is used by applications like Oracle Global Trade Management to print import or export documentation based on who owns the goods at the time of customs clearance.
- New summary: Supply Chain Financial Orchestration now publishes a Transfer Pricing business event for shipment-driven flows, including customer drop shipments, that other systems such as OTM and GTM can subscribe to.
- Reason: Optional: only matters if you subscribe to the event. Summary described the existing REST resource.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/inv26b/26B-inventory-wn-f43598.htm

### 26B-f49705@inv26b · Redwood: Export All Search Results on the Completed Transactions Page
- Family / product: Supply Chain & Manufacturing · Inventory Management · Inventory Management
- Rating: **medium → low**
- Old summary: The Completed Transactions page serves as a critical auditing and investigative tool, providing visibility into historical inventory activity used to research and reconcile on-hand inventory discrepancies.
- New summary: The Completed Transactions page has a new Export All button that downloads every search result, not just the rows on screen.
- Reason: Minor. Summary was background only.
- Oracle: https://docs.oracle.com/en/cloud/saas/readiness/scm/26b/inv26b/26B-inventory-wn-f49705.htm

