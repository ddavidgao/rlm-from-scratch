"""
Synthetic documents for RLM retrieval testing and training data generation.

Each document is a realistic text blob (1000-5000 characters) representing
a different document type. These serve as the corpus that the RLM searches
through when generating training examples.
"""

PRODUCT_SPEC = """\
ThermoSense Pro X1 — Smart Thermostat Product Specification Sheet

Model Number: TS-PRO-X1-2024
Manufacturer: ThermoSense Technologies Inc.
Release Date: September 2024

OVERVIEW
The ThermoSense Pro X1 is a next-generation smart thermostat designed for \
residential and light commercial HVAC systems. It combines precision temperature \
control with advanced environmental monitoring to optimize comfort and energy \
efficiency. The device features a 3.5-inch full-color LCD touchscreen with \
ambient light adaptive brightness.

DIMENSIONS AND PHYSICAL SPECIFICATIONS
- Display Unit: 4.3 in (W) x 4.3 in (H) x 1.1 in (D)
- Weight: 6.2 oz (display unit), 2.1 oz (backplate)
- Display: 3.5-inch IPS LCD, 320x320 resolution, capacitive touch
- Finish: Matte white (TS-PRO-X1-W) or brushed nickel (TS-PRO-X1-N)

FEATURES
- WiFi Connectivity: 802.11 b/g/n (2.4 GHz) and 802.11 ac (5 GHz)
- Geofencing: Automatic home/away detection using smartphone GPS with \
configurable radius from 500 ft to 5 miles
- Humidity Sensor: Integrated capacitive humidity sensor, ±2% RH accuracy, \
range 0-99% RH
- Air Quality Monitor: Built-in VOC sensor and particulate matter estimator \
(PM2.5) with real-time AQI display
- Occupancy Detection: Dual passive infrared (PIR) sensors with 120° field of view
- Ambient Light Sensor: Automatic display brightness adjustment
- Learning Algorithm: Proprietary AdaptiveComfort AI learns household patterns \
within 7-14 days of installation

TEMPERATURE SPECIFICATIONS
- Operating Range: 40°F to 95°F (4.4°C to 35°C)
- Temperature Accuracy: ±0.5°F (±0.3°C)
- Setpoint Range: 45°F to 90°F (7.2°C to 32.2°C)
- Differential: Adjustable from 0.5°F to 3.0°F

POWER REQUIREMENTS
- Primary Power: 24 VAC from HVAC system (C-wire required)
- Backup Battery: Built-in rechargeable lithium-polymer, maintains settings for \
up to 4 hours during power loss
- Power Consumption: 2.5W typical, 4W maximum

COMPATIBILITY
- HVAC Systems: Supports 1-stage, 2-stage, and variable-speed heating and cooling; \
heat pump with auxiliary heat; dual-fuel systems
- Smart Home Integration: Amazon Alexa, Google Home, Apple HomeKit, Samsung SmartThings
- Protocols: Zigbee 3.0 hub built-in, Matter-ready via firmware update (Q1 2025)
- Mobile App: iOS 15+ and Android 10+ (ThermoSense Connect app)

INSTALLATION REQUIREMENTS
- Wiring: Requires C-wire (common wire). C-wire adapter kit sold separately ($29.99)
- Wall Box: Standard single-gang electrical box or direct wall mount
- Clearance: Minimum 4 inches clearance on all sides for accurate temperature reading
- Professional installation recommended; DIY installation guide included

WARRANTY AND PRICING
- Warranty: 2-year limited manufacturer warranty covering defects in materials and \
workmanship; extended 5-year warranty available for $39.99
- MSRP: $249.99
- In the Box: Display unit, backplate, mounting screws, wire labels, trim plate, \
quick start guide, screwdriver

CERTIFICATIONS
- FCC Part 15 Class B, UL 60730-1, Energy Star Certified, EPA SmartSense Partner
- Operating Temperature (Ambient): 32°F to 120°F
- Operating Humidity: 5% to 95% non-condensing

For technical support contact support@thermosense.com or call 1-888-THERMO-1. \
Full documentation available at docs.thermosense.com/pro-x1.\
"""

LEASE_AGREEMENT = """\
RESIDENTIAL LEASE AGREEMENT

Oakwood Apartments — Unit 4B
1247 Oakwood Boulevard, Portland, OR 97205

This Residential Lease Agreement ("Agreement") is entered into on February 15, \
2025, by and between:

LANDLORD: Oakwood Property Management LLC, represented by Margaret A. Sullivan, \
Property Manager, hereinafter referred to as "Landlord."

TENANT: Jonathan R. Whitfield and Emily S. Whitfield, hereinafter collectively \
referred to as "Tenant."

1. PREMISES
Landlord leases to Tenant the residential unit located at 1247 Oakwood Boulevard, \
Unit 4B, Portland, Oregon 97205, a two-bedroom, one-bathroom apartment \
approximately 875 square feet, including one assigned parking space (Space #47).

2. LEASE TERM
The lease term shall be twelve (12) months, commencing on March 1, 2025, and \
ending on February 28, 2026. Tenant must provide written notice of intent to \
vacate at least sixty (60) days prior to the lease expiration. If no notice is \
given, the lease converts to a month-to-month tenancy at a rate of $1,950 per month.

3. RENT
Monthly rent is One Thousand Eight Hundred Fifty Dollars ($1,850), due on the \
first day of each calendar month. Rent shall be paid via the Oakwood Resident \
Portal (portal.oakwoodapts.com) or by certified check delivered to the leasing \
office at 1247 Oakwood Boulevard, Suite 100.

4. SECURITY DEPOSIT
Tenant shall pay a security deposit of Two Thousand Seven Hundred Seventy-Five \
Dollars ($2,775), equal to one and one-half months' rent, upon execution of this \
Agreement. The security deposit will be held in a non-interest-bearing account at \
First Pacific Bank. The deposit, less any lawful deductions for damages beyond \
normal wear and tear, unpaid rent, or cleaning fees, will be returned within \
thirty-one (31) days of lease termination per Oregon Revised Statutes §90.300.

5. LATE PAYMENT AND FEES
Rent not received by 5:00 PM on the fifth (5th) day of the month shall incur a \
late fee of Seventy-Five Dollars ($75). An additional charge of Twenty-Five Dollars \
($25) per day applies from the 10th day until rent is received in full. Returned \
checks or failed electronic payments will incur a fee of Fifty Dollars ($50).

6. PET POLICY
Cats are permitted with a one-time non-refundable pet deposit of Three Hundred \
Dollars ($300) and monthly pet rent of Thirty-Five Dollars ($35) per cat, maximum \
two cats. Dogs are permitted provided they do not exceed twenty-five (25) pounds \
at maturity. Dogs over 25 lbs are strictly prohibited. Aggressive breeds as defined \
by the property's insurance carrier (including but not limited to Pit Bulls, \
Rottweilers, and Dobermans) are prohibited regardless of weight. A veterinary \
health certificate and proof of vaccination must be provided prior to move-in. \
Tenant is liable for all pet-related damages.

7. MAINTENANCE AND REPAIRS
Landlord shall maintain the structural elements, plumbing, electrical systems, \
HVAC, and common areas in good repair. Tenant shall keep the unit clean and \
sanitary, promptly report maintenance issues via the maintenance request system \
(portal.oakwoodapts.com/maintenance), and shall not make alterations or \
improvements without prior written consent. Tenant is responsible for replacing \
HVAC filters quarterly and maintaining smoke detector batteries. Emergency \
maintenance is available 24/7 at (503) 555-0147.

8. PARKING
One parking space (Space #47) is included with this lease at no additional charge. \
Additional parking spaces are available at a rate of One Hundred Fifty Dollars \
($150) per month, subject to availability. All vehicles must be registered with the \
leasing office and display a valid Oakwood parking permit.

9. QUIET HOURS AND COMMUNITY RULES
Quiet hours are observed from 10:00 PM to 7:00 AM daily. Excessive noise complaints \
may result in fines of $100 per occurrence after the first written warning. Smoking \
is prohibited inside all units and within 25 feet of any building entrance. Grilling \
is permitted only in designated patio areas. Trash and recycling must be placed in \
designated receptacles in the refuse area behind Building 4.

10. UTILITIES
Tenant is responsible for electricity, gas, internet, and cable. Water, sewer, and \
trash removal are included in the monthly rent. Landlord provides shared laundry \
facilities on each floor at no additional charge.

Signatures:
_________________________          _________________________
Margaret A. Sullivan                Jonathan R. Whitfield
Oakwood Property Management LLC    Tenant

Date: February 15, 2025            Date: February 15, 2025\
"""

LAB_REPORT = """\
WATER QUALITY ANALYSIS REPORT

Clearwater Municipal Water Treatment Plant
2850 Reservoir Drive, Clearwater, WA 98501
Laboratory Report No.: CW-2025-01-0347

SAMPLE INFORMATION
- Sample Collection Date: January 8, 2025
- Sample Receipt Date: January 8, 2025
- Analysis Completion Date: January 12, 2025
- Sample Type: Treated Drinking Water (post-filtration, post-disinfection)
- Sample Point: Distribution System Entry Point, Plant Outlet Tap #3
- Collected By: Michael Torres, Certified Water Operator (License WA-4521)
- Chain of Custody ID: COC-20250108-047

ANALYTICAL RESULTS

Parameter                  | Result    | Unit       | MCL/Standard  | Status
---------------------------|-----------|------------|---------------|----------
pH                         | 7.2       | pH units   | 6.5 - 8.5    | PASS
Turbidity                  | 0.3       | NTU        | 1.0 NTU       | PASS
Free Chlorine Residual     | 1.2       | mg/L       | 4.0 mg/L max  | PASS
Total Chlorine Residual    | 1.5       | mg/L       | 4.0 mg/L max  | PASS
Lead (Pb)                  | <0.005    | mg/L       | 0.015 mg/L    | PASS
Copper (Cu)                | 0.42      | mg/L       | 1.3 mg/L      | PASS
Arsenic (As)               | <0.002    | mg/L       | 0.010 mg/L    | PASS
Nitrate (as N)             | 3.1       | mg/L       | 10.0 mg/L     | PASS
Nitrite (as N)             | <0.05     | mg/L       | 1.0 mg/L      | PASS
Fluoride                   | 0.7       | mg/L       | 4.0 mg/L      | PASS
Total Coliform             | Absent    | per 100 mL | Absent        | PASS
E. coli                    | Absent    | per 100 mL | Absent        | PASS
Total Dissolved Solids     | 287       | mg/L       | 500 mg/L      | PASS
Hardness (as CaCO3)        | 142       | mg/L       | N/A (secondary)| INFO
Alkalinity (as CaCO3)      | 98        | mg/L       | N/A           | INFO
Sulfate                    | 45        | mg/L       | 250 mg/L      | PASS
Chloride                   | 32        | mg/L       | 250 mg/L      | PASS
Iron (Fe)                  | 0.08      | mg/L       | 0.3 mg/L      | PASS
Manganese (Mn)             | 0.02      | mg/L       | 0.05 mg/L     | PASS
Total Trihalomethanes      | 38        | µg/L       | 80 µg/L       | PASS
Haloacetic Acids (HAA5)    | 29        | µg/L       | 60 µg/L       | PASS

MICROBIOLOGICAL ANALYSIS
Method: EPA Method 1604 (Total Coliform/E. coli), Colilert-18 IDEXX
Total Coliform: Absent in all five 100 mL sample portions
E. coli: Absent in all five 100 mL sample portions
Heterotrophic Plate Count: 12 CFU/mL (standard: <500 CFU/mL) — PASS

COMPLIANCE STATUS
All parameters tested are within compliance limits established by the \
U.S. Environmental Protection Agency (EPA) Safe Drinking Water Act (SDWA) \
and Washington State Department of Health regulations (WAC 246-290). The \
water quality at the distribution entry point meets all primary and secondary \
maximum contaminant levels (MCLs) as of the analysis date.

NOTES
- Total hardness of 142 mg/L as CaCO3 classifies this water as "moderately hard" \
on the USGS hardness scale. This is within the typical range for the Clearwater \
source aquifer.
- Fluoride is maintained at the CDC-recommended optimal level of 0.7 mg/L for \
dental health benefits.
- Total trihalomethanes and haloacetic acids, while within limits, are monitored \
quarterly as disinfection byproducts. Values have remained stable over the past \
four quarters (range: 32-41 µg/L TTHM, 24-33 µg/L HAA5).

QUALITY ASSURANCE
Laboratory blank, duplicate, and matrix spike results were within acceptable QC \
limits for all analyses. The laboratory is certified under Washington State \
Department of Ecology Accreditation Program (Lab ID: WA-ELAP-1138).

Reviewed and Approved By:
Dr. Sarah Chen, Ph.D.
Director of Analytical Services
Clearwater Environmental Testing Laboratory
Washington State Certified Analyst #SC-7823

Report Date: January 14, 2025
This report shall not be reproduced except in full without written consent.\
"""

MEETING_MINUTES = """\
RIVERSIDE COMMUNITY ASSOCIATION
BOARD OF DIRECTORS MEETING MINUTES

Date: Wednesday, January 15, 2025
Time: 7:00 PM — 9:15 PM
Location: Riverside Community Center, Main Hall, 500 River Road, Riverside, CA 92501

ATTENDEES
Board Members Present:
- Patricia Nakamura, President
- David Okonkwo, Vice President
- Lisa Fernandez, Treasurer
- Robert Kim, Secretary
- Angela Washington, Director
- Thomas Bergström, Director
- Yuki Tanaka, Director
- Michael Reeves, Director
- Diane Kowalski, Director

Board Members Absent:
- None

Also Present:
- Sandra Mitchell, Community Manager (Meridian Property Services)
- Officer James Delgado, Riverside PD Community Liaison
- 23 community residents in attendance

CALL TO ORDER
President Nakamura called the meeting to order at 7:03 PM. A quorum was confirmed \
with all nine board members present.

1. APPROVAL OF PREVIOUS MINUTES
Secretary Kim presented the minutes from the December 11, 2024 meeting. Director \
Washington moved to approve; Director Bergström seconded. Motion carried unanimously \
(9-0).

2. TREASURER'S REPORT
Treasurer Fernandez presented the December 2024 financial summary:
- Operating Account Balance: $78,342.16
- Reserve Fund Balance: $45,000.00
- Total Assessments Collected (December): $32,150 of $33,600 expected (95.7%)
- Outstanding Delinquencies: 4 units totaling $1,450
- Major December Expenses: Landscaping contract ($4,200), holiday lighting ($1,850), \
insurance premium quarterly payment ($3,475)

Fernandez noted that the reserve fund has reached the $45,000 target recommended \
by the 2024 reserve study. The board discussed maintaining this level and adjusting \
the monthly reserve contribution from $2,000 to $1,500 beginning in February. \
Motion by Fernandez, seconded by Okonkwo. Approved 8-1 (Reeves opposed, citing \
preference for continued accumulation).

3. POOL RENOVATION PROJECT
Community Manager Mitchell presented three bids for the pool renovation project:
- AquaPro Builders: $87,500 (includes new filtration, resurfacing, LED lighting)
- Pacific Pool & Spa: $92,300 (includes same scope plus expanded deck area)
- BlueWave Construction: $79,900 (filtration and resurfacing only, no lighting)

After extensive discussion, Director Tanaka moved to approve the AquaPro Builders \
bid at $87,500, funded from the reserve fund with the remaining balance to be \
collected via a special assessment of $150 per unit. Director Fernandez seconded. \
Motion approved 7-2 (Reeves and Kowalski opposed). Work is scheduled to begin \
March 3, 2025, with an estimated completion date of April 18, 2025. The pool will \
be closed during renovation.

4. PARKING REGULATIONS UPDATE
Vice President Okonkwo presented proposed amendments to the parking regulations:
- Guest parking limited to 48 hours without prior approval from management
- Commercial vehicles over 10,000 lbs GVWR prohibited from resident parking areas
- Overnight street parking prohibited between 1:00 AM and 5:00 AM (per city ordinance)
- Violating vehicles subject to towing at owner's expense after one written warning

Motion by Okonkwo, seconded by Washington. Approved 9-0. New regulations take \
effect February 15, 2025. Community Manager Mitchell will distribute notices to \
all residents by January 31.

5. SECURITY CAMERA INSTALLATION
Officer Delgado presented crime statistics for the Riverside area showing a 12% \
increase in vehicle break-ins during Q4 2024. He recommended enhanced lighting and \
camera surveillance at entry points.

Mitchell presented a proposal from SecureVision Inc. for installation of 8 HD \
security cameras covering parking areas, pool gate, main entrance, and mail kiosk. \
Total cost: $12,500 including installation, cabling, and one year of cloud storage. \
Annual renewal for cloud storage: $1,200/year.

Director Washington moved to approve the SecureVision proposal at $12,500, funded \
from the operating budget. Bergström seconded. Approved 9-0. Installation is \
targeted for the week of February 10, 2025.

6. RESIDENT CONCERNS
- Resident Maria Santos (Unit 12A) raised concerns about noise from the dog park \
area during early morning hours. The board directed Mitchell to post signage \
restricting dog park hours to 7:00 AM — 9:00 PM.
- Resident Alan Park (Unit 8C) asked about EV charging station installation. The \
board agreed to research options and present findings at the March meeting.

7. NEXT MEETING
The next Board of Directors meeting is scheduled for Wednesday, February 19, 2025, \
at 7:00 PM at the Riverside Community Center.

ACTION ITEMS
- Mitchell: Distribute new parking regulation notices by January 31
- Mitchell: Coordinate SecureVision installation for week of February 10
- Mitchell: Post dog park hours signage by January 20
- Okonkwo: Research EV charging station vendors and present at March meeting
- Mitchell: Send AquaPro Builders contract for board signatures by January 22
- Fernandez: Prepare special assessment notices for pool renovation ($150/unit)

Meeting adjourned at 9:15 PM.

Respectfully submitted,
Robert Kim, Secretary
Riverside Community Association\
"""

EMPLOYEE_HANDBOOK = """\
MERIDIAN CONSULTING GROUP — EMPLOYEE HANDBOOK (Excerpt)
Section 7: Time Off and Leave Policies
Effective Date: January 1, 2025 | Revision 4.2

7.1 PAID TIME OFF (PTO) — VACATION

Meridian Consulting Group provides paid vacation time to all regular full-time \
employees based on length of continuous service. Vacation time accrues on a \
per-pay-period basis (semi-monthly payroll).

Years of Service         | Annual Vacation Days | Accrual Rate (per pay period)
-------------------------|----------------------|------------------------------
0 through 3 years        | 10 days (80 hours)   | 3.33 hours
4 through 7 years        | 15 days (120 hours)  | 5.00 hours
8 years and above        | 20 days (160 hours)  | 6.67 hours

Vacation time begins accruing on the employee's date of hire. New employees may \
use accrued vacation after completing 90 days of employment. Vacation requests \
must be submitted through the HR portal (hr.meridiancg.com) at least two weeks in \
advance for requests of three or more consecutive days. Single-day requests require \
at least 48 hours' notice. Managers retain discretion to approve or deny requests \
based on business needs and team coverage requirements.

Vacation Carryover Policy: Employees may carry over a maximum of five (5) unused \
vacation days into the following calendar year. Carryover days must be used by \
March 31 or they will be forfeited. Unused vacation beyond the carryover limit \
will not be paid out and is forfeited on December 31 of each year. Upon voluntary \
termination with at least two weeks' notice, accrued but unused vacation (up to \
the annual maximum) will be paid out in the final paycheck.

7.2 SICK LEAVE

All regular full-time employees receive eight (8) days (64 hours) of paid sick \
leave per calendar year, front-loaded on January 1. New hires receive a prorated \
amount based on their start date. Sick leave may be used for the employee's own \
illness, injury, or medical appointments, as well as to care for an immediate \
family member (spouse, child, parent) who is ill.

Employees who are absent due to illness for three or more consecutive workdays \
must provide a physician's note upon return. Unused sick leave does not carry over \
to the following year and is not paid out upon termination.

7.3 BEREAVEMENT LEAVE

In the event of a death in the immediate family (spouse, domestic partner, child, \
parent, sibling, grandparent, grandchild, or in-law equivalent), employees are \
granted five (5) days of paid bereavement leave. For extended family members \
(aunt, uncle, cousin, niece, nephew), three (3) days of paid bereavement leave \
are provided. Additional unpaid time may be approved by the employee's manager \
and HR on a case-by-case basis.

7.4 JURY DUTY

Employees summoned for jury duty will receive their full regular pay for up to \
ten (10) business days per calendar year. Employees must provide a copy of the \
jury summons to their manager and HR within three business days of receipt. Any \
jury duty compensation received from the court may be retained by the employee. \
If jury service extends beyond ten business days, additional time will be unpaid \
unless otherwise required by state law.

7.5 PAID HOLIDAYS

Meridian Consulting Group observes eleven (11) paid holidays per calendar year:
1. New Year's Day (January 1)
2. Martin Luther King Jr. Day (third Monday in January)
3. Presidents' Day (third Monday in February)
4. Memorial Day (last Monday in May)
5. Juneteenth (June 19)
6. Independence Day (July 4)
7. Labor Day (first Monday in September)
8. Thanksgiving Day (fourth Thursday in November)
9. Day after Thanksgiving (fourth Friday in November)
10. Christmas Eve (December 24)
11. Christmas Day (December 25)

When a holiday falls on a Saturday, it will be observed on the preceding Friday. \
When a holiday falls on a Sunday, it will be observed on the following Monday. \
Part-time employees receive holiday pay on a prorated basis.

7.6 DRESS CODE

The standard dress code is business casual Monday through Thursday. Business \
casual includes collared shirts, blouses, slacks, khakis, skirts of appropriate \
length, and closed-toe shoes. Casual Friday permits jeans (no rips or tears), \
sneakers, and company-branded apparel. The following are not permitted on any day: \
athletic wear (gym shorts, sweatpants, yoga pants), flip-flops, clothing with \
offensive graphics or language, and excessively revealing attire. Client-facing \
meetings may require business professional attire at the manager's discretion.

7.7 REMOTE WORK POLICY

Eligible employees may work remotely up to two (2) days per week after completing \
a six-month tenure with the company. Remote work eligibility is determined by \
the employee's role, performance, and manager approval. Remote work requests must \
be submitted and approved through the HR portal. Employees working remotely must \
be available during core business hours (9:00 AM — 3:00 PM local time) and \
maintain a reliable internet connection (minimum 25 Mbps download speed). The \
company provides a one-time $500 home office stipend for approved remote workers \
to purchase ergonomic equipment. Employees are expected to maintain a dedicated, \
private workspace suitable for video conferencing. Remote work privileges may be \
revoked if performance standards are not maintained.

7.8 PARENTAL LEAVE

In addition to any applicable FMLA leave, Meridian Consulting Group provides up \
to six (6) weeks of paid parental leave for the birth, adoption, or foster \
placement of a child. This benefit is available to all regular full-time employees \
who have completed at least one year of service. Paid parental leave runs \
concurrently with FMLA leave where applicable.

For questions about leave policies, contact Human Resources at hr@meridiancg.com \
or extension 2400.\
"""

SAFETY_DATA_SHEET = """\
SAFETY DATA SHEET
According to Regulation (EC) No. 1907/2006 (REACH), GHS Rev. 7

SECTION 1: IDENTIFICATION
Product Name: CleanMax Industrial Degreaser
Product Code: CM-DG-500
Supplier: CleanMax Chemical Solutions, 4100 Industrial Parkway, Houston, TX 77040
Emergency Phone: CHEMTREC 1-800-424-9300 (24 hours)
Information Phone: (713) 555-0198
Recommended Use: Industrial degreasing of metal parts, machinery, and equipment
Restrictions on Use: Not for household use. Not for use on food contact surfaces.

SECTION 2: HAZARD IDENTIFICATION
GHS Classification:
- Acute Toxicity, Oral: Category 4
- Skin Irritation: Category 2
- Serious Eye Irritation: Category 2A

Signal Word: WARNING

Hazard Statements:
- H302: Harmful if swallowed
- H315: Causes skin irritation
- H319: Causes serious eye irritation

Precautionary Statements:
- P264: Wash hands and exposed skin thoroughly after handling
- P270: Do not eat, drink, or smoke when using this product
- P280: Wear protective gloves, eye protection, and protective clothing
- P301+P312: IF SWALLOWED: Call a POISON CENTER if you feel unwell
- P302+P352: IF ON SKIN: Wash with plenty of soap and water
- P305+P351+P338: IF IN EYES: Rinse cautiously with water for several minutes. \
Remove contact lenses, if present and easy to do. Continue rinsing.
- P332+P313: If skin irritation occurs: Get medical advice
- P337+P313: If eye irritation persists: Get medical advice

SECTION 3: COMPOSITION / INFORMATION ON INGREDIENTS
Component                  | CAS Number   | Concentration (w/w)
---------------------------|--------------|--------------------
2-Butoxyethanol            | 111-76-2     | 15 — 20%
Sodium Hydroxide           | 1310-73-2    | 5 — 10%
Sodium Metasilicate        | 6834-92-0    | 3 — 7%
Alkyl Polyglucoside (C8-C10)| 68515-73-1  | 2 — 5%
Water                      | 7732-18-5    | Balance (60 — 75%)

SECTION 4: FIRST AID MEASURES
Inhalation: Move person to fresh air. If breathing is difficult, administer oxygen. \
If not breathing, give artificial respiration. Seek medical attention if symptoms persist.
Skin Contact: Remove contaminated clothing immediately. Wash affected area with \
plenty of soap and water for at least 15 minutes. If irritation develops or persists, \
seek medical attention.
Eye Contact: Rinse cautiously with water for at least 15 minutes, lifting upper \
and lower eyelids periodically. Remove contact lenses if present. Seek immediate \
medical attention if irritation persists.
Ingestion: Do NOT induce vomiting. Rinse mouth with water. Do not give anything \
by mouth to an unconscious person. Seek immediate medical attention. Contact \
Poison Control Center at 1-800-222-1222.

SECTION 5: FIREFIGHTING MEASURES
Suitable Extinguishing Media: Water spray, dry chemical, CO2, alcohol-resistant foam
Unsuitable: Full water jet (may cause splashing and spread of product)
Flash Point: 143°F (62°C) — closed cup method (ASTM D93)
Auto-Ignition Temperature: 460°F (238°C)
Flammable Limits: LEL 1.1%, UEL 12.7% (based on 2-butoxyethanol component)
Special Hazards: Thermal decomposition may produce carbon monoxide, carbon dioxide, \
and sodium oxide fumes.
Firefighter Protection: Wear self-contained breathing apparatus (SCBA) and full \
protective gear.

SECTION 6: ACCIDENTAL RELEASE MEASURES
Contain spill with inert absorbent material (sand, vermiculite, diatomaceous earth). \
Collect in appropriate waste container. Prevent entry into drains, sewers, or \
waterways. For large spills (>55 gallons), notify local environmental authority.

SECTION 7: HANDLING AND STORAGE
Handling: Use only with adequate ventilation. Avoid contact with skin, eyes, and \
clothing. Do not mix with acids (reaction produces heat and may cause spattering).
Storage: Store in original container in a cool, dry, well-ventilated area between \
15°C and 30°C (59°F — 86°F). Keep container tightly closed when not in use. \
Store away from incompatible materials (acids, oxidizers). Shelf life: 24 months \
from date of manufacture when stored as directed.

SECTION 8: EXPOSURE CONTROLS / PERSONAL PROTECTION
Occupational Exposure Limits:
- 2-Butoxyethanol: OSHA PEL TWA 50 ppm (skin), ACGIH TLV TWA 25 ppm (skin)
- Sodium Hydroxide: OSHA PEL Ceiling 2 mg/m³, ACGIH TLV Ceiling 2 mg/m³

Engineering Controls: Use local exhaust ventilation or mechanical ventilation to \
maintain airborne concentrations below exposure limits.
Personal Protective Equipment:
- Respiratory: NIOSH-approved respirator with organic vapor cartridges if ventilation \
is inadequate
- Hands: Chemical-resistant gloves (nitrile, minimum 8 mil thickness)
- Eyes: Chemical splash goggles or face shield
- Skin: Chemical-resistant apron; long sleeves recommended

SECTION 13: DISPOSAL CONSIDERATIONS
Dispose of in accordance with all applicable federal, state, and local regulations. \
Do not dump into sewers or waterways. Container must be triple-rinsed before recycling \
or disposal. Waste code: D002 (corrosive waste, pH-dependent). Contact local \
hazardous waste facility for disposal options.

SECTION 14: TRANSPORT INFORMATION
DOT Classification: UN1760, Corrosive Liquid, N.O.S. (contains sodium hydroxide), \
Class 8, Packing Group III
IATA: Same as DOT
IMDG: Same as DOT

SDS Revision Date: October 15, 2024 | Version 3.1
Prepared by: CleanMax EHS Department\
"""

GRANT_PROPOSAL = """\
NATIONAL SCIENCE FOUNDATION
GRANT PROPOSAL — PROJECT ABSTRACT

Award Number: NSF-AGS-2025-XXXXX (Pending)
Program: Atmosphere and Geospace Sciences — Climate and Large-Scale Dynamics
Title: Adaptive Neural Networks for Real-Time Climate Modeling

PRINCIPAL INVESTIGATOR
Dr. James Morrison, Ph.D.
Associate Professor, Department of Atmospheric Sciences
Pacific Northwest Research Institute (PNRI)
4200 Cascade Research Boulevard, Seattle, WA 98103
Email: j.morrison@pnri.edu | Phone: (206) 555-0234

CO-PRINCIPAL INVESTIGATORS
- Dr. Amara Osei, Assistant Professor of Computer Science, PNRI
- Dr. Kevin Zhao, Research Scientist, NOAA Pacific Marine Environmental Laboratory

REQUESTED FUNDING
Total: $742,000 over 36 months (3 years)
Year 1: $268,000 | Year 2: $251,000 | Year 3: $223,000

PROJECT SUMMARY

1. RESEARCH OBJECTIVES
Current global climate models (GCMs) require enormous computational resources and \
typically operate at spatial resolutions of 50-100 km, which is insufficient to \
capture critical mesoscale phenomena such as convective systems, land-sea breezes, \
and orographic precipitation. This project proposes the development of Adaptive \
Climate Neural Networks (ACNNs) — a novel deep learning architecture that dynamically \
adjusts model resolution and computational allocation based on detected atmospheric \
complexity.

The primary objectives are:
(a) Design and train a multi-scale neural network architecture capable of predicting \
atmospheric state variables (temperature, pressure, humidity, wind fields) at \
variable resolutions from 5 km to 100 km.
(b) Develop an attention-based mechanism that identifies regions of high atmospheric \
variability and automatically allocates finer resolution to those areas in real-time.
(c) Validate ACNN predictions against ERA5 reanalysis data and operational weather \
model output (GFS, ECMWF IFS) over a three-year historical period (2020-2022).
(d) Demonstrate that ACNN can produce 72-hour regional climate forecasts at 10 km \
effective resolution with less than 5% of the computational cost of a traditional \
GCM running at equivalent resolution.

2. METHODOLOGY
The ACNN architecture builds upon recent advances in vision transformers and neural \
operator theory. The model uses a U-Net backbone with transformer-based skip \
connections that process atmospheric data at multiple spatial scales simultaneously. \
A novel "atmospheric attention" module scores each grid cell based on local gradient \
magnitudes of temperature, humidity, and vorticity, then routes computational \
resources accordingly.

Training data will consist of ERA5 reanalysis fields (1979-2022) at 0.25° resolution, \
augmented with high-resolution WRF simulations over the Pacific Northwest and North \
Atlantic basins. The training pipeline will leverage PNRI's GPU cluster (128 NVIDIA \
A100 GPUs) and will employ a curriculum learning strategy, starting from coarse-\
resolution predictions and progressively increasing target resolution over training.

Transfer learning experiments will assess the model's ability to generalize to \
geographical regions not included in training data (e.g., South Asian monsoon region, \
Sahel). Uncertainty quantification will be performed using Monte Carlo dropout and \
deep ensemble methods.

3. EXPECTED OUTCOMES
- A publicly available ACNN model and codebase (released under MIT License on GitHub)
- At least four peer-reviewed publications in journals including Nature Climate Change, \
Journal of Geophysical Research: Atmospheres, and Artificial Intelligence for the \
Earth Systems
- Demonstrated 15-20x speedup over conventional dynamical downscaling methods with \
comparable accuracy (target RMSE within 10% of WRF benchmarks)
- Open training dataset of paired coarse/fine resolution atmospheric fields

4. BROADER IMPACTS
This research addresses the critical need for accessible, high-resolution climate \
information for adaptation planning. The computational efficiency gains of ACNN \
will enable smaller research institutions, developing nations, and local governments \
to generate regional climate projections without access to supercomputing facilities. \
The project will support two Ph.D. students and one postdoctoral researcher, with \
active recruitment from underrepresented groups in atmospheric science through \
PNRI's partnership with the AMS Student Diversity Program.

Community engagement includes annual workshops with Washington State emergency \
management officials to translate research outputs into actionable climate resilience \
tools. Educational outreach will develop a freely available online module \
"AI and Climate Science" suitable for undergraduate atmospheric science and data \
science curricula.

5. KEY PERSONNEL
- Dr. James Morrison (PI): 3 months/year — Climate modeling, project leadership
- Dr. Amara Osei (Co-PI): 2 months/year — Neural network architecture design, ML \
training pipeline
- Dr. Kevin Zhao (Co-PI): 1 month/year — NOAA data integration, model validation
- TBD Postdoctoral Researcher: 12 months/year — Core model development
- TBD Ph.D. Student 1: Research assistantship — Attention mechanism development
- TBD Ph.D. Student 2: Research assistantship — Transfer learning and validation

6. TIMELINE
Phase 1 (Months 1-12): Data pipeline construction, baseline model architecture, \
preliminary training experiments
Phase 2 (Months 13-24): Full ACNN training, atmospheric attention module refinement, \
initial validation against ERA5
Phase 3 (Months 25-36): Transfer learning experiments, operational forecast \
demonstrations, publication of results, public code and data release

BUDGET JUSTIFICATION (SUMMARY)
- Personnel (salaries + benefits): $498,000
- Computing resources (GPU allocation, cloud credits): $108,000
- Travel (conferences, NOAA collaboration visits): $36,000
- Equipment (workstations, storage): $52,000
- Indirect costs (PNRI negotiated rate 26%): $48,000\
"""

IT_INCIDENT_REPORT = """\
IT INCIDENT REPORT

Incident ID: INC-2025-0892
Report Date: January 21, 2025
Report Author: Priya Sharma, Senior Site Reliability Engineer
Organization: NovaTech Solutions Inc.

INCIDENT CLASSIFICATION
- Severity: P1 — Critical (complete service outage affecting external customers)
- Category: Infrastructure — Storage / Database
- Service(s) Affected: Production Database Cluster (db-prod-01 through db-prod-04), \
Customer Portal (portal.novatech.io), REST API Gateway (api.novatech.io), \
Internal Analytics Dashboard
- Business Impact: Complete loss of customer-facing services; internal teams unable \
to access operational data

DETECTION AND NOTIFICATION
- Detection Time: 2025-01-20 03:42 UTC
- Detection Method: Automated — PagerDuty alert triggered by Datadog monitor \
"db-prod write latency > 500ms" followed 2 minutes later by \
"db-prod connection pool exhaustion" alert
- First Responder: Priya Sharma (on-call SRE), acknowledged alert at 03:47 UTC
- Incident Commander: Marcus Chen, Director of Engineering (joined at 04:05 UTC)

TIMELINE OF EVENTS (all times UTC)

03:42 — Datadog alert fires: write latency on db-prod-01 exceeds 500ms threshold. \
Average write latency had been 12ms over the previous 24 hours.

03:44 — Second alert: connection pool utilization on db-prod-01 reaches 95%. \
Cascading alerts begin for db-prod-02 through db-prod-04 as read replicas \
fall behind on replication.

03:47 — Priya Sharma acknowledges PagerDuty alert. Initial triage begins. SSH \
into db-prod-01 shows iostat reporting >98% disk utilization with \
average write queue depth of 247 (normal: <5).

03:55 — Sharma identifies that the underlying storage array (NetStore SX-9000, \
Firmware v4.2.1) is reporting intermittent write acknowledgment failures. \
Storage controller logs show "SCSI sense key: MEDIUM ERROR" on multiple LUNs.

04:02 — Customer portal begins returning HTTP 503 errors. API gateway health check \
failures trigger automatic removal from load balancer. Status page updated \
to "Major Outage — Investigating."

04:05 — Marcus Chen joins incident bridge call. Decision made to escalate to P1 \
and engage NetStore vendor support.

04:15 — NetStore on-call engineer (Raj Patel) joins the call. Reviews storage \
controller diagnostics remotely. Identifies firmware bug in v4.2.1 that \
causes write cache coherency failures under sustained sequential write \
patterns exceeding 850 MB/s. Bug was documented in NetStore advisory \
NS-SA-2024-0847, published December 12, 2024, but had not been applied \
to NovaTech's environment.

04:30 — Decision made to failover database to standby storage array (NetStore \
SX-9000 unit 2, firmware v4.1.9, not affected by the bug). Database team \
begins controlled shutdown of primary database cluster.

04:45 — Primary database cluster shut down cleanly. Filesystem integrity check \
initiated on standby storage.

05:12 — Filesystem check complete — no corruption detected. Database cluster \
restart initiated against standby storage.

05:38 — db-prod-01 (primary) comes online on standby storage. Write tests confirm \
normal latency (8ms average). Replication to db-prod-02 through db-prod-04 \
initiated.

06:15 — All four database nodes confirmed healthy. Read replica lag cleared. \
Connection pool utilization normal at 23%.

06:22 — API gateway health checks passing. Customer portal restored. Status page \
updated to "Monitoring — Services Restored."

07:15 — Extended monitoring period shows stable performance. Replication lag: 0ms. \
Write latency: 11ms average. No errors in storage controller logs.

08:05 — Incident downgraded from P1 to P3 (monitoring). All-clear notification \
sent to engineering and customer success teams.

ROOT CAUSE
The root cause was a firmware bug in NetStore SX-9000 firmware version 4.2.1 that \
caused write cache coherency failures when sustained sequential write throughput \
exceeded 850 MB/s. This triggered cascading write acknowledgment failures across \
multiple LUNs, causing the database's I/O subsystem to stall. The bug was documented \
in NetStore Security Advisory NS-SA-2024-0847 (published December 12, 2024) with \
a recommended upgrade to firmware v4.2.2. NovaTech's storage environment had not \
yet been patched due to the change being scheduled for the January 25, 2025 \
maintenance window.

IMPACT SUMMARY
- Total Downtime: 4 hours 23 minutes (03:42 — 08:05 UTC)
- Customer-Facing Outage: 4 hours 20 minutes (04:02 — 08:22 UTC, including DNS \
cache propagation delay)
- Users Impacted: Approximately 15,000 active users during the outage window \
(based on typical traffic patterns for Monday 03:00-08:00 UTC)
- Revenue Impact: Estimated $47,000 in lost transaction processing fees
- SLA Impact: Monthly uptime dropped to 99.38%, below the 99.9% SLA commitment. \
SLA credit of 10% monthly fee applicable for affected enterprise customers.
- Data Loss: None confirmed. All transactions were either completed before the \
outage or safely rolled back. WAL (Write-Ahead Log) integrity verified.

RESOLUTION
Immediate: Failed over production database cluster to standby storage array \
running unaffected firmware v4.1.9.

FOLLOW-UP ACTIONS
| # | Action Item | Owner | Due Date | Status |
|---|-------------|-------|----------|--------|
| 1 | Apply NetStore firmware v4.2.2 to primary storage array | Infra Team | 2025-01-25 | Scheduled |
| 2 | Apply firmware v4.2.2 to standby storage array | Infra Team | 2025-01-26 | Scheduled |
| 3 | Implement automated vendor advisory monitoring | SRE Team | 2025-02-07 | In Progress |
| 4 | Add storage throughput alerting (>800 MB/s warning) | SRE Team | 2025-01-31 | In Progress |
| 5 | Review and accelerate critical patch SLA (target: 7 days) | Infra Lead | 2025-02-14 | Not Started |
| 6 | Conduct failover drill for database-to-standby-storage | DB Team | 2025-02-28 | Not Started |
| 7 | Customer communication: post-mortem blog post | Comms Team | 2025-01-24 | Draft |

LESSONS LEARNED
1. Vendor security advisories must be triaged within 48 hours of publication, not \
batched into monthly maintenance windows.
2. Storage throughput monitoring had a gap — existing alerts focused on latency and \
IOPS but did not cover sustained sequential write bandwidth.
3. The failover to standby storage, while successful, took longer than target RTO \
(2 hours) due to lack of a documented runbook. The team improvised under pressure.
4. Automated health checks correctly detected the outage within 2 minutes — this \
investment in observability paid off.

Reviewed and Approved By:
Marcus Chen, Director of Engineering
Date: January 22, 2025\
"""


DOCUMENTS = {
    "product_spec": PRODUCT_SPEC,
    "lease_agreement": LEASE_AGREEMENT,
    "lab_report": LAB_REPORT,
    "meeting_minutes": MEETING_MINUTES,
    "employee_handbook": EMPLOYEE_HANDBOOK,
    "safety_data_sheet": SAFETY_DATA_SHEET,
    "grant_proposal": GRANT_PROPOSAL,
    "it_incident_report": IT_INCIDENT_REPORT,
}
