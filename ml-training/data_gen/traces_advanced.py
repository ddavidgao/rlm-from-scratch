"""
Training traces for advanced categories.

Categories:
  - false_positive: First match is wrong, must search further
  - multi_search_synthesis: 2-3 searches combined into one answer
  - llm_query_after_search: Find section, then use llm_query() to summarize
  - llm_query_failure: llm_query returns FAILED, fall back to direct search
  - large_doc_navigation: Check size, find structure, navigate methodically
  - mixed_varied: Miscellaneous patterns (count, case-insensitive, rfind, etc.)

CRITICAL: Each code turn is INDEPENDENTLY executed via exec() with `context` =
document text. Variables do NOT persist between turns.
"""

# ---------------------------------------------------------------------------
# Category 1: false_positive (10 traces)
# First match is wrong/irrelevant; assistant searches further.
# ---------------------------------------------------------------------------

FALSE_POSITIVE_TRACES = [
    # 1 - "table" in cooking book finds table of contents first
    {
        "doc": "boston_cooking_school",
        "question": "What are the measurements for the table of proportions for cooking?",
        "category": "false_positive",
        "turns": [
            {
                "content": "```python\nidx = context.find('table')\nprint(f'First match at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "The first match refers to the Table of Contents, not what we need. Let me search for the next occurrence.\n\n```python\nidx = context.find('table')\nidx2 = context.find('table', idx + 1)\nprint(f'Next match at: {idx2}')\nprint(context[idx2:idx2+300])\n```"
            },
            {
                "content": "FINAL(The table of proportions for cooking is found in the text. Based on the document content, the relevant measurements and proportions are described in the section found at the second match location.)",
                "is_final": True,
            },
        ],
    },
    # 2 - "order" in Cushing's Manual finds table of contents mention first
    {
        "doc": "cushings_manual",
        "question": "What does the text say about a point of order?",
        "category": "false_positive",
        "turns": [
            {
                "content": "```python\nidx = context.find('order')\nprint(f'First match at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "This first mention of 'order' appears in a general heading or table of contents, not the actual discussion. Let me find the next occurrence.\n\n```python\nidx = context.find('order')\nidx2 = context.find('order', idx + 1)\nprint(f'Next match at: {idx2}')\nprint(context[idx2:idx2+400])\n```"
            },
            {
                "content": "FINAL(According to Cushing's Manual, a point of order may be raised by any member who believes that a rule of the assembly is being violated. The presiding officer decides the question of order, and the member raising it must state the rule believed to be violated. The decision of the chair may be appealed to the assembly.)",
                "is_final": True,
            },
        ],
    },
    # 3 - "fire" in safety data sheet finds fire extinguisher before fire hazard
    {
        "doc": "safety_data_sheet",
        "question": "What are the fire hazard warnings for this material?",
        "category": "false_positive",
        "turns": [
            {
                "content": "```python\nidx = context.find('fire')\nprint(f'First match at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "This first mention is about fire extinguishing measures, not the hazard classification. Let me search further.\n\n```python\nidx = context.find('fire')\nidx2 = context.find('fire', idx + 1)\nprint(f'Next match at: {idx2}')\nprint(context[idx2:idx2+300])\n```"
            },
            {
                "content": "```python\nidx = context.find('fire')\nidx2 = context.find('fire', idx + 1)\nidx3 = context.find('hazard', idx2)\nprint(f'Hazard at: {idx3}')\nprint(context[idx3:idx3+400])\n```"
            },
            {
                "content": "FINAL(The fire hazard warnings indicate this material is flammable and should be kept away from open flames and heat sources. Proper fire suppression equipment should be on hand when handling this material.)",
                "is_final": True,
            },
        ],
    },
    # 4 - "guard" in cavalry outpost finds early general mention first
    {
        "doc": "cavalry_outpost",
        "question": "What does the text say about posting the advance guard?",
        "category": "false_positive",
        "turns": [
            {
                "content": "```python\nidx = context.find('guard')\nprint(f'First match at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "This first occurrence is just a general mention in an introductory passage. I need the detailed instructions.\n\n```python\nidx = context.find('guard')\nidx2 = context.find('guard', idx + 1)\nidx3 = context.find('guard', idx2 + 1)\nprint(f'Third match at: {idx3}')\nprint(context[idx3:idx3+400])\n```"
            },
            {
                "content": "FINAL(The text instructs that the advance guard should be posted at a distance sufficient to give the main body time to prepare for action. The guard must occupy high ground when possible and maintain communication with patrols on the flanks. The officer commanding the guard is responsible for reporting all enemy movements.)",
                "is_final": True,
            },
        ],
    },
    # 5 - "term" in lease finds terminology section before lease term
    {
        "doc": "lease_agreement",
        "question": "What is the duration of the lease term?",
        "category": "false_positive",
        "turns": [
            {
                "content": "```python\nidx = context.find('term')\nprint(f'First match at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "This first result is from a definitions or terminology section, not the lease term duration. Let me find the actual lease term clause.\n\n```python\nidx = context.find('Lease Term')\nif idx == -1:\n    idx = context.find('term')\n    idx2 = context.find('term', idx + 1)\n    print(f'Next match at: {idx2}')\n    print(context[idx2:idx2+300])\nelse:\n    print(f'Lease Term at: {idx}')\n    print(context[idx:idx+300])\n```"
            },
            {
                "content": "FINAL(The lease term is for a period of 12 months, commencing on the start date specified in the agreement and ending on the termination date, unless renewed or terminated earlier as provided in the lease.)",
                "is_final": True,
            },
        ],
    },
    # 6 - "minutes" in meeting minutes finds timestamp before actual minutes content
    {
        "doc": "meeting_minutes",
        "question": "What decisions were made during the meeting?",
        "category": "false_positive",
        "turns": [
            {
                "content": "```python\nidx = context.find('decision')\nprint(f'First match at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "This first mention of 'decision' appears in the agenda preview, not the actual decisions section. Let me look further.\n\n```python\nidx = context.find('decision')\nidx2 = context.find('decision', idx + 1)\nprint(f'Next match at: {idx2}')\nprint(context[idx2:idx2+400])\n```"
            },
            {
                "content": "FINAL(The key decisions made during the meeting include approval of the Q3 budget allocation, assignment of the new project lead, and agreement to move the next deadline to the following month.)",
                "is_final": True,
            },
        ],
    },
    # 7 - "light" in rules of road at sea finds "lighthouse" before signal lights
    {
        "doc": "rules_of_road_sea",
        "question": "What are the rules about signal lights on vessels?",
        "category": "false_positive",
        "turns": [
            {
                "content": "```python\nidx = context.find('light')\nprint(f'First match at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "This first match mentions 'lighthouse' or similar, not signal light rules. Let me search specifically for 'signal' nearby.\n\n```python\nidx = context.find('light')\nidx2 = context.find('light', idx + 1)\nidx3 = context.find('light', idx2 + 1)\nprint(f'Third match at: {idx3}')\nprint(context[idx3:idx3+400])\n```"
            },
            {
                "content": "FINAL(Vessels must display signal lights according to their size and type. Power-driven vessels must show a masthead light, sidelights, and a stern light. The rules specify the arcs of visibility and the minimum range at which each light must be visible.)",
                "is_final": True,
            },
        ],
    },
    # 8 - "section" in employee handbook finds table of contents reference
    {
        "doc": "employee_handbook",
        "question": "What does the disciplinary action section say?",
        "category": "false_positive",
        "turns": [
            {
                "content": "```python\nidx = context.find('disciplin')\nprint(f'First match at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "This first mention is in a list of sections or an overview. I need the actual disciplinary action policy.\n\n```python\nidx = context.find('disciplin')\nidx2 = context.find('disciplin', idx + 1)\nprint(f'Next match at: {idx2}')\nprint(context[idx2:idx2+400])\n```"
            },
            {
                "content": "FINAL(The disciplinary action section outlines a progressive discipline policy: verbal warning for first offense, written warning for second offense, suspension for third offense, and termination for fourth offense. All actions are documented in the employee's personnel file.)",
                "is_final": True,
            },
        ],
    },
    # 9 - "method" in lab report finds methods citation before methodology section
    {
        "doc": "lab_report",
        "question": "What experimental methods were used in this study?",
        "category": "false_positive",
        "turns": [
            {
                "content": "```python\nidx = context.find('method')\nprint(f'First match at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "The first hit is a passing reference to methods, not the methodology section itself. Let me find the actual section.\n\n```python\nidx = context.find('method')\nidx2 = context.find('method', idx + 1)\nidx3 = context.find('method', idx2 + 1)\nprint(f'Third match at: {idx3}')\nprint(context[idx3:idx3+500])\n```"
            },
            {
                "content": "FINAL(The experimental methods include spectrophotometric analysis of sample concentrations, with measurements taken at 15-minute intervals over a 2-hour period. Samples were prepared using standard dilution protocols and all measurements were performed in triplicate.)",
                "is_final": True,
            },
        ],
    },
    # 10 - "budget" in grant proposal finds budget justification mention before actual budget
    {
        "doc": "grant_proposal",
        "question": "What is the total budget for this grant proposal?",
        "category": "false_positive",
        "turns": [
            {
                "content": "```python\nidx = context.find('budget')\nprint(f'First match at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "This first match is a mention of 'budget justification' in the table of contents. I need the actual budget figures.\n\n```python\nidx = context.find('budget')\nidx2 = context.find('budget', idx + 1)\nprint(f'Next match at: {idx2}')\nprint(context[idx2:idx2+400])\n```"
            },
            {
                "content": "FINAL(The total budget for the grant proposal is $250,000 over a 3-year period, broken down into personnel costs, equipment, supplies, and indirect costs.)",
                "is_final": True,
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# Category 2: multi_search_synthesis (20 traces)
# 2-3 separate searches, combined into one FINAL answer.
# ---------------------------------------------------------------------------

MULTI_SEARCH_TRACES = [
    # 1 - Cooking: ingredients + baking time
    {
        "doc": "boston_cooking_school",
        "question": "What are the ingredients and baking time for white bread?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('bread')\nprint(f'Bread at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "I found the bread section. Let me look for specific ingredients.\n\n```python\nidx = context.find('flour')\nprint(f'Flour at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "Now let me find the baking time.\n\n```python\nidx = context.find('bake')\nprint(f'Bake at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "FINAL(White bread requires flour, yeast, salt, sugar, butter, and milk. The baking time is approximately 45-60 minutes in a moderate oven until the crust is golden brown.)",
                "is_final": True,
            },
        ],
    },
    # 2 - Cavalry Outpost: terrain selection + enemy approach
    {
        "doc": "cavalry_outpost",
        "question": "What terrain features should outposts occupy, and how should the enemy's approach be handled?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('road')\nprint(f'Road at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "Now let me search for how to handle the enemy's approach.\n\n```python\nidx = context.find('enemy')\nprint(f'Enemy at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(Outposts should occupy positions that command the roads and approaches the enemy is likely to use. High ground, bridges, and defiles are preferred. When the enemy approaches, the outpost must delay their advance long enough for the main body to prepare, sending reports back while the picquets and patrols fall back in good order.)",
                "is_final": True,
            },
        ],
    },
    # 3 - Household physician: symptoms + treatment
    {
        "doc": "household_physician",
        "question": "What are the symptoms and treatment for fever?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('fever')\nprint(f'Fever at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "Found information about fever symptoms. Now let me find the treatment.\n\n```python\nidx = context.find('fever')\nidx2 = context.find('treatment', idx)\nprint(f'Treatment at: {idx2}')\nprint(context[idx2:idx2+400])\n```"
            },
            {
                "content": "FINAL(Symptoms of fever include elevated temperature, chills, sweating, headache, and general malaise. Treatment includes rest, plenty of fluids, and cool compresses. For persistent fever, the physician may administer appropriate remedies to reduce temperature.)",
                "is_final": True,
            },
        ],
    },
    # 4 - Lease: rent amount + late fees
    {
        "doc": "lease_agreement",
        "question": "What is the monthly rent and what are the late payment penalties?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('rent')\nprint(f'Rent at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "Found the rent clause. Now let me find late fees.\n\n```python\nidx = context.find('late')\nprint(f'Late at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "FINAL(The monthly rent is $2,500 due on the first of each month. Late payment penalties include a $50 late fee if rent is not received within 5 days of the due date, plus $10 per day for each additional day of delinquency.)",
                "is_final": True,
            },
        ],
    },
    # 5 - Product spec: dimensions + weight
    {
        "doc": "product_spec",
        "question": "What are the product dimensions and weight?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('dimension')\nprint(f'Dimensions at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "Now let me find the weight.\n\n```python\nidx = context.find('weight')\nprint(f'Weight at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "FINAL(The product dimensions are 12.5 x 8.3 x 4.2 inches (L x W x H). The unit weighs 3.7 pounds without accessories, and 4.2 pounds with the standard accessory kit.)",
                "is_final": True,
            },
        ],
    },
    # 6 - Safety data sheet: first aid + storage
    {
        "doc": "safety_data_sheet",
        "question": "What are the first aid measures and storage requirements?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('first aid')\nif idx == -1:\n    idx = context.find('First Aid')\nprint(f'First aid at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "Found first aid info. Now searching for storage requirements.\n\n```python\nidx = context.find('storage')\nif idx == -1:\n    idx = context.find('Storage')\nprint(f'Storage at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(First aid measures: For skin contact, wash with soap and water for 15 minutes. For eye contact, flush with water for 20 minutes. For inhalation, move to fresh air. Storage requirements: Store in a cool, dry, well-ventilated area below 25C. Keep container tightly closed and away from incompatible materials.)",
                "is_final": True,
            },
        ],
    },
    # 7 - Employee handbook: PTO policy + holidays
    {
        "doc": "employee_handbook",
        "question": "How much PTO do employees get and what are the company holidays?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('PTO')\nif idx == -1:\n    idx = context.find('paid time off')\nprint(f'PTO at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "Found PTO info. Now let me find the holidays list.\n\n```python\nidx = context.find('holiday')\nif idx == -1:\n    idx = context.find('Holiday')\nprint(f'Holiday at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(Employees receive 15 days of PTO per year for the first 3 years, increasing to 20 days after 3 years of service. Company holidays include New Year's Day, Memorial Day, Independence Day, Labor Day, Thanksgiving, and Christmas Day, for a total of 6 paid holidays.)",
                "is_final": True,
            },
        ],
    },
    # 8 - Cushing's Manual: quorum + presiding officer
    {
        "doc": "cushings_manual",
        "question": "What constitutes a quorum and what are the duties of the presiding officer?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('quorum')\nprint(f'Quorum at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "Found quorum information. Now let me find presiding officer duties.\n\n```python\nidx = context.find('presiding')\nprint(f'Presiding at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(According to Cushing's Manual, a quorum is the number of members required to be present for the assembly to conduct business, typically a majority unless otherwise specified. The presiding officer's duties include maintaining order, recognizing members who wish to speak, stating questions for vote, and announcing the results of each vote taken by the assembly.)",
                "is_final": True,
            },
        ],
    },
    # 9 - Lab report: hypothesis + results
    {
        "doc": "lab_report",
        "question": "What was the hypothesis and what were the experimental results?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('hypothesis')\nif idx == -1:\n    idx = context.find('Hypothesis')\nprint(f'Hypothesis at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "Found the hypothesis. Now let me find the results.\n\n```python\nidx = context.find('result')\nif idx == -1:\n    idx = context.find('Result')\nprint(f'Results at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The hypothesis stated that increasing the concentration of the catalyst would proportionally increase the reaction rate. The results confirmed this hypothesis: doubling the catalyst concentration increased the reaction rate by approximately 1.8x, and tripling it increased the rate by 2.7x.)",
                "is_final": True,
            },
        ],
    },
    # 10 - Grant proposal: objectives + timeline
    {
        "doc": "grant_proposal",
        "question": "What are the project objectives and the proposed timeline?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('objective')\nif idx == -1:\n    idx = context.find('Objective')\nprint(f'Objectives at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "Found objectives. Now let me find the timeline.\n\n```python\nidx = context.find('timeline')\nif idx == -1:\n    idx = context.find('Timeline')\nprint(f'Timeline at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(The project has three main objectives: (1) develop a novel detection algorithm, (2) validate it on real-world datasets, and (3) publish findings in a peer-reviewed journal. The proposed timeline is 36 months: Year 1 for development, Year 2 for validation and testing, and Year 3 for analysis and publication.)",
                "is_final": True,
            },
        ],
    },
    # 11 - IT incident report: root cause + resolution + impact
    {
        "doc": "it_incident_report",
        "question": "What was the root cause of the incident, how was it resolved, and what was the impact?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('root cause')\nif idx == -1:\n    idx = context.find('Root Cause')\nprint(f'Root cause at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "Found root cause. Now resolution.\n\n```python\nidx = context.find('resolution')\nif idx == -1:\n    idx = context.find('Resolution')\nprint(f'Resolution at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "Now let me find the impact assessment.\n\n```python\nidx = context.find('impact')\nif idx == -1:\n    idx = context.find('Impact')\nprint(f'Impact at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "FINAL(Root cause: A misconfigured load balancer directed all traffic to a single server, which became overloaded. Resolution: The load balancer configuration was corrected and traffic was redistributed across all available servers. Impact: The outage lasted 2 hours and 15 minutes, affecting approximately 5,000 users and resulting in an estimated $12,000 in lost revenue.)",
                "is_final": True,
            },
        ],
    },
    # 12 - Cavalry Outpost: patrol duties + night procedures
    {
        "doc": "cavalry_outpost",
        "question": "What are the patrol duties and how do procedures change at night?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('patrol')\nprint(f'Patrol at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "Found the section on patrols. Now let me find night procedures.\n\n```python\nidx = context.find('night')\nprint(f'Night at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(Patrols are sent out from the outpost line to observe the enemy's movements and to maintain communication between posts. They must move quietly and avoid detection. At night, patrols are sent out more frequently, the distance between sentries is reduced, and all troops remain on the alert as the enemy is more likely to attempt a surprise advance under cover of darkness.)",
                "is_final": True,
            },
        ],
    },
    # 13 - Household physician: causes + prevention
    {
        "doc": "household_physician",
        "question": "What are the causes and prevention methods for cholera?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('cholera')\nprint(f'Cholera at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "Found cholera info. Let me find prevention guidance.\n\n```python\nidx = context.find('cholera')\nidx2 = context.find('prevent', idx)\nprint(f'Prevention at: {idx2}')\nprint(context[idx2:idx2+400])\n```"
            },
            {
                "content": "FINAL(Cholera is caused by contaminated water and food, particularly in areas with poor sanitation. Prevention methods include boiling drinking water, maintaining clean living conditions, proper disposal of waste, and avoiding raw or undercooked food in affected areas.)",
                "is_final": True,
            },
        ],
    },
    # 14 - Rules of road: fog signals + right of way
    {
        "doc": "rules_of_road_sea",
        "question": "What are the fog signal rules and the right-of-way hierarchy between vessel types?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('fog')\nprint(f'Fog at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "Found fog signals. Now right-of-way.\n\n```python\nidx = context.find('right')\nprint(f'Right at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(In fog, power-driven vessels underway must sound a prolonged blast at intervals of not more than 2 minutes. Sailing vessels sound one prolonged blast followed by two short blasts. For right-of-way: vessels not under command have priority, followed by vessels restricted in ability to maneuver, then vessels engaged in fishing, then sailing vessels, and finally power-driven vessels.)",
                "is_final": True,
            },
        ],
    },
    # 15 - GPO manual: capitalization + punctuation
    {
        "doc": "gpo_manual",
        "question": "What are the GPO rules for capitalization and punctuation of titles?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('capitaliz')\nprint(f'Capitalization at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "Found capitalization rules. Now punctuation.\n\n```python\nidx = context.find('punctuat')\nprint(f'Punctuation at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(For capitalization of titles, the GPO style manual requires capitalizing the first word and all principal words. For punctuation, titles of published works are set in italics, and short works use quotation marks. Periods and commas always go inside closing quotation marks.)",
                "is_final": True,
            },
        ],
    },
    # 16 - Meeting minutes: attendees + action items
    {
        "doc": "meeting_minutes",
        "question": "Who attended the meeting and what action items were assigned?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('attend')\nif idx == -1:\n    idx = context.find('Attend')\nprint(f'Attendees at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "Found attendees. Now action items.\n\n```python\nidx = context.find('action item')\nif idx == -1:\n    idx = context.find('Action Item')\nprint(f'Action items at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(Attendees included the project manager, lead engineer, QA lead, and two stakeholder representatives. Action items assigned: (1) Project manager to finalize the revised schedule by Friday, (2) Lead engineer to complete the API integration by end of sprint, (3) QA lead to prepare the test plan for the next release.)",
                "is_final": True,
            },
        ],
    },
    # 17 - Cooking: preparation + serving suggestion
    {
        "doc": "boston_cooking_school",
        "question": "How do you prepare and serve soup stock?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('soup stock')\nif idx == -1:\n    idx = context.find('stock')\nprint(f'Stock at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "Found preparation info. Now serving.\n\n```python\nidx = context.find('serv')\nprint(f'Serve at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "FINAL(To prepare soup stock: use bones, meat trimmings, and vegetables simmered in water for several hours, then strain. For serving, soup stock can be used as a base for various soups, served clear as a broth, or used in sauces and gravies.)",
                "is_final": True,
            },
        ],
    },
    # 18 - Product spec: power requirements + operating temperature
    {
        "doc": "product_spec",
        "question": "What are the power requirements and operating temperature range?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('power')\nif idx == -1:\n    idx = context.find('Power')\nprint(f'Power at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "Found power specs. Now temperature.\n\n```python\nidx = context.find('temperature')\nif idx == -1:\n    idx = context.find('Temperature')\nprint(f'Temperature at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "FINAL(Power requirements: 120V AC, 60Hz, 2.5A maximum draw (300W). Operating temperature range: 0 to 40 degrees Celsius (32 to 104 degrees Fahrenheit). The device should not be operated outside this range to avoid damage.)",
                "is_final": True,
            },
        ],
    },
    # 19 - Lease agreement: security deposit + termination
    {
        "doc": "lease_agreement",
        "question": "What are the security deposit terms and early termination conditions?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('deposit')\nprint(f'Deposit at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "Found deposit info. Now early termination.\n\n```python\nidx = context.find('terminat')\nprint(f'Termination at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(The security deposit is equal to one month's rent ($2,500) and is refundable within 30 days of lease end, minus deductions for damages. Early termination requires 60 days written notice and payment of a penalty equal to 2 months' rent.)",
                "is_final": True,
            },
        ],
    },
    # 20 - Grant proposal: methodology + expected outcomes
    {
        "doc": "grant_proposal",
        "question": "What research methodology will be used and what are the expected outcomes?",
        "category": "multi_search_synthesis",
        "turns": [
            {
                "content": "```python\nidx = context.find('methodol')\nif idx == -1:\n    idx = context.find('Methodol')\nprint(f'Methodology at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "Found methodology. Now expected outcomes.\n\n```python\nidx = context.find('outcome')\nif idx == -1:\n    idx = context.find('expected')\nprint(f'Outcomes at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(The methodology uses a mixed-methods approach combining quantitative data analysis with qualitative case studies. Expected outcomes include a validated detection framework with >90% accuracy, two peer-reviewed publications, and an open-source toolkit for the research community.)",
                "is_final": True,
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# Category 3: llm_query_after_search (10 traces)
# Find a section, then use llm_query() to summarize/analyze it.
# ---------------------------------------------------------------------------

LLM_QUERY_TRACES = [
    # 1 - Summarize cavalry outpost chapter
    {
        "doc": "cavalry_outpost",
        "question": "Can you summarize the advice on selecting outpost positions?",
        "category": "llm_query_after_search",
        "turns": [
            {
                "content": "```python\nidx = context.find('distance')\nprint(f'Distance at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "Found the relevant section. Let me use llm_query to get a good summary.\n\n```python\nidx = context.find('distance')\nresult = llm_query('What advice does the text give about selecting outpost positions?', context[idx:idx+2000])\nprint(result)\n```"
            },
            {
                "content": "FINAL(The text advises that outpost positions should be selected to command the roads and avenues of approach. The distance from the main body depends on the proximity of the enemy and the nature of the terrain. High ground is preferred, and positions should allow sentries and picquets to observe a wide area while maintaining communication with the rear.)",
                "is_final": True,
            },
        ],
    },
    # 2 - Summarize household physician section
    {
        "doc": "household_physician",
        "question": "What does this medical text recommend for treating burns?",
        "category": "llm_query_after_search",
        "turns": [
            {
                "content": "```python\nidx = context.find('burn')\nprint(f'Burns at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "Found the section. Let me get a summary using llm_query.\n\n```python\nidx = context.find('burn')\nresult = llm_query('What are the recommended treatments for burns?', context[idx:idx+2000])\nprint(result)\n```"
            },
            {
                "content": "FINAL(The text recommends treating burns by first removing the source of heat, then applying cool compresses. For minor burns, a soothing ointment or oil may be applied. For severe burns, the patient should be kept warm, given fluids, and medical attention sought immediately.)",
                "is_final": True,
            },
        ],
    },
    # 3 - Analyze methodology in lab report
    {
        "doc": "lab_report",
        "question": "Can you analyze the methodology used in this lab report?",
        "category": "llm_query_after_search",
        "turns": [
            {
                "content": "```python\nidx = context.find('methodology')\nif idx == -1:\n    idx = context.find('Method')\nprint(f'Methodology at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "Found the methodology section. Let me analyze it.\n\n```python\nidx = context.find('methodology')\nif idx == -1:\n    idx = context.find('Method')\nresult = llm_query('Analyze the strengths and weaknesses of this methodology', context[idx:idx+2000])\nprint(result)\n```"
            },
            {
                "content": "FINAL(The methodology employs standard analytical procedures with triplicate measurements, which is a strength for reproducibility. However, the sample size is relatively small, and the study would benefit from additional controls. The measurement intervals are appropriate for the reaction kinetics being studied.)",
                "is_final": True,
            },
        ],
    },
    # 4 - Summarize grant proposal abstract
    {
        "doc": "grant_proposal",
        "question": "Give me a plain-language summary of this grant proposal's research plan.",
        "category": "llm_query_after_search",
        "turns": [
            {
                "content": "```python\nidx = context.find('research plan')\nif idx == -1:\n    idx = context.find('abstract')\nif idx == -1:\n    idx = context.find('Abstract')\nprint(f'Research plan at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "Let me use llm_query to create a plain-language summary.\n\n```python\nidx = context.find('research plan')\nif idx == -1:\n    idx = context.find('abstract')\nif idx == -1:\n    idx = context.find('Abstract')\nresult = llm_query('Summarize this research plan in plain language that a non-expert could understand', context[idx:idx+3000])\nprint(result)\n```"
            },
            {
                "content": "FINAL(This grant proposal aims to develop a new computer-based tool that can automatically detect patterns in large datasets. The research team plans to build the tool over 3 years, test it on real data, and share it freely with other researchers. The goal is to make data analysis faster and more accurate for scientists across multiple fields.)",
                "is_final": True,
            },
        ],
    },
    # 5 - Summarize safety data sheet hazards
    {
        "doc": "safety_data_sheet",
        "question": "Summarize all hazard information in this safety data sheet.",
        "category": "llm_query_after_search",
        "turns": [
            {
                "content": "```python\nidx = context.find('hazard')\nif idx == -1:\n    idx = context.find('Hazard')\nprint(f'Hazard at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "Found the hazard section. Let me get a comprehensive summary.\n\n```python\nidx = context.find('hazard')\nif idx == -1:\n    idx = context.find('Hazard')\nresult = llm_query('Summarize all hazard warnings and safety precautions', context[idx:idx+3000])\nprint(result)\n```"
            },
            {
                "content": "FINAL(The safety data sheet identifies the material as flammable (Category 2) with health hazards including skin and eye irritation. Key hazards: flammable liquid and vapor, may cause respiratory irritation if inhaled, harmful if swallowed. Required precautions include wearing protective gloves, eye protection, and working in a well-ventilated area.)",
                "is_final": True,
            },
        ],
    },
    # 6 - Interpret Cushing's Manual section
    {
        "doc": "cushings_manual",
        "question": "Explain the rules around amending a motion in simple terms.",
        "category": "llm_query_after_search",
        "turns": [
            {
                "content": "```python\nidx = context.find('amendment')\nprint(f'Amendment at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "Found the amendment section. Let me get a plain-language explanation.\n\n```python\nidx = context.find('amendment')\nresult = llm_query('Explain in simple terms how amending a motion works according to this text', context[idx:idx+2000])\nprint(result)\n```"
            },
            {
                "content": "FINAL(According to Cushing's Manual, to amend a motion a member proposes a change to the wording while the motion is pending. The amendment must be seconded and is open to debate. The assembly votes on the amendment first, then on the original motion as amended or unchanged. An amendment to an amendment is permitted, but no further amendments to that are allowed.)",
                "is_final": True,
            },
        ],
    },
    # 7 - Summarize cooking technique
    {
        "doc": "boston_cooking_school",
        "question": "Summarize the key principles of making good pastry from this cookbook.",
        "category": "llm_query_after_search",
        "turns": [
            {
                "content": "```python\nidx = context.find('pastry')\nif idx == -1:\n    idx = context.find('Pastry')\nprint(f'Pastry at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "Found the pastry section. Let me summarize the key principles.\n\n```python\nidx = context.find('pastry')\nif idx == -1:\n    idx = context.find('Pastry')\nresult = llm_query('What are the key principles for making good pastry?', context[idx:idx+2000])\nprint(result)\n```"
            },
            {
                "content": "FINAL(The key principles for making good pastry are: use cold ingredients (especially butter), handle the dough as little as possible to avoid developing gluten, use the right proportion of fat to flour, and bake in a hot oven. Overworking the dough results in tough pastry rather than flaky.)",
                "is_final": True,
            },
        ],
    },
    # 8 - Analyze IT incident for lessons learned
    {
        "doc": "it_incident_report",
        "question": "What lessons can be learned from this IT incident?",
        "category": "llm_query_after_search",
        "turns": [
            {
                "content": "```python\nidx = context.find('lesson')\nif idx == -1:\n    idx = context.find('recommend')\nif idx == -1:\n    idx = context.find('Recommend')\nprint(f'Lessons at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "Let me get a broader analysis using llm_query on the incident summary.\n\n```python\nidx = context.find('lesson')\nif idx == -1:\n    idx = context.find('recommend')\nif idx == -1:\n    idx = context.find('Recommend')\nresult = llm_query('What lessons can be learned from this incident? What should be done differently?', context[idx:idx+2000])\nprint(result)\n```"
            },
            {
                "content": "FINAL(Key lessons from this incident: (1) Configuration changes should go through a review process before deployment, (2) Automated monitoring should have alerted the team sooner, (3) A rollback procedure should be documented for quick recovery, and (4) Load testing should be performed after any infrastructure changes.)",
                "is_final": True,
            },
        ],
    },
    # 9 - Explain sea navigation rule
    {
        "doc": "rules_of_road_sea",
        "question": "Explain the collision avoidance rules in plain language.",
        "category": "llm_query_after_search",
        "turns": [
            {
                "content": "```python\nidx = context.find('collision')\nif idx == -1:\n    idx = context.find('avoid')\nprint(f'Collision at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "Found the section. Let me get a plain-language explanation.\n\n```python\nidx = context.find('collision')\nif idx == -1:\n    idx = context.find('avoid')\nresult = llm_query('Explain the collision avoidance rules in simple terms', context[idx:idx+2000])\nprint(result)\n```"
            },
            {
                "content": "FINAL(Collision avoidance boils down to three principles: (1) Every vessel must keep a proper lookout at all times, (2) Vessels must travel at a safe speed that allows time to react, and (3) When two vessels approach each other, the one that must give way should take early and obvious action to avoid collision, while the other should maintain its course and speed.)",
                "is_final": True,
            },
        ],
    },
    # 10 - Summarize employee benefits
    {
        "doc": "employee_handbook",
        "question": "Give me a summary of the employee benefits package.",
        "category": "llm_query_after_search",
        "turns": [
            {
                "content": "```python\nidx = context.find('benefit')\nif idx == -1:\n    idx = context.find('Benefit')\nprint(f'Benefits at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "Found the benefits section. Let me summarize.\n\n```python\nidx = context.find('benefit')\nif idx == -1:\n    idx = context.find('Benefit')\nresult = llm_query('Summarize the complete employee benefits package', context[idx:idx+3000])\nprint(result)\n```"
            },
            {
                "content": "FINAL(The employee benefits package includes: health insurance (medical, dental, vision) with company paying 80% of premiums, 401k retirement plan with 4% company match, 15-20 days PTO based on tenure, 6 paid holidays, life insurance at 1x salary, and professional development reimbursement up to $2,000 per year.)",
                "is_final": True,
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# Category 4: llm_query_failure (5 traces)
# llm_query returns FAILED because the chunk is too short/empty.
# ---------------------------------------------------------------------------

LLM_FAILURE_TRACES = [
    # 1 - Search for nonexistent keyword, get bad slice
    {
        "doc": "cavalry_outpost",
        "question": "What does the text say about aerial reconnaissance?",
        "category": "llm_query_failure",
        "turns": [
            {
                "content": "```python\nidx = context.find('aerial')\nprint(f'Index: {idx}')\nresult = llm_query('What does this say about aerial reconnaissance?', context[idx:idx+100])\nprint(result)\n```"
            },
            {
                "content": "The keyword wasn't found (idx=-1) and llm_query failed with insufficient context. Let me try searching for related concepts directly.\n\n```python\nidx = context.find('patrol')\nprint(f'Patrol at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(The text does not discuss aerial reconnaissance, as it predates the use of aircraft in military operations. However, it extensively covers ground-based reconnaissance through cavalry patrols, which served the same purpose of observing the enemy and reporting their movements back to the commanding officer.)",
                "is_final": True,
            },
        ],
    },
    # 2 - Misspelled keyword leads to bad slice
    {
        "doc": "household_physician",
        "question": "What treatments does this book suggest for diphtheria?",
        "category": "llm_query_failure",
        "turns": [
            {
                "content": "```python\nidx = context.find('diptheria')\nprint(f'Index: {idx}')\nresult = llm_query('What treatments are suggested for diptheria?', context[idx:idx+100])\nprint(result)\n```"
            },
            {
                "content": "The misspelled search returned -1 and llm_query failed. Let me try the correct spelling.\n\n```python\nidx = context.find('diphtheria')\nprint(f'Diphtheria at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The Household Physician recommends several treatments for diphtheria, including isolating the patient, keeping the throat clean with antiseptic gargles, maintaining adequate nutrition and fluids, and seeking medical attention promptly as the disease can be life-threatening.)",
                "is_final": True,
            },
        ],
    },
    # 3 - Looking for section that doesn't exist
    {
        "doc": "lease_agreement",
        "question": "What does the lease say about cryptocurrency payments?",
        "category": "llm_query_failure",
        "turns": [
            {
                "content": "```python\nidx = context.find('cryptocurrency')\nprint(f'Index: {idx}')\nresult = llm_query('What are the cryptocurrency payment terms?', context[idx:idx+100])\nprint(result)\n```"
            },
            {
                "content": "The keyword was not found and llm_query failed. Let me check what payment methods are actually mentioned.\n\n```python\nidx = context.find('payment')\nprint(f'Payment at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(The lease agreement does not mention cryptocurrency payments. Accepted payment methods are check, bank transfer, or electronic payment through the landlord's approved payment portal. All payments must be in US dollars.)",
                "is_final": True,
            },
        ],
    },
    # 4 - Empty chunk from product spec
    {
        "doc": "product_spec",
        "question": "What are the Bluetooth specifications for this product?",
        "category": "llm_query_failure",
        "turns": [
            {
                "content": "```python\nidx = context.find('bluetooth')\nif idx == -1:\n    idx = context.find('Bluetooth')\nprint(f'Index: {idx}')\nresult = llm_query('What are the Bluetooth specifications?', context[idx:idx+100])\nprint(result)\n```"
            },
            {
                "content": "The search returned -1 and llm_query couldn't analyze the empty chunk. Let me check what connectivity options are available.\n\n```python\nidx = context.find('connect')\nif idx == -1:\n    idx = context.find('wireless')\nprint(f'Connectivity at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(The product specification does not include Bluetooth connectivity. The available connectivity options are USB 3.0, Ethernet (RJ-45), and Wi-Fi 802.11ac. For wireless needs, the built-in Wi-Fi module is the recommended option.)",
                "is_final": True,
            },
        ],
    },
    # 5 - Nonexistent section in grant proposal
    {
        "doc": "grant_proposal",
        "question": "What clinical trial phases are described in the proposal?",
        "category": "llm_query_failure",
        "turns": [
            {
                "content": "```python\nidx = context.find('clinical trial')\nprint(f'Index: {idx}')\nresult = llm_query('What clinical trial phases are described?', context[idx:idx+100])\nprint(result)\n```"
            },
            {
                "content": "The term 'clinical trial' was not found and llm_query returned a failure. This appears to be a computational research proposal, not a clinical one. Let me check what the actual research involves.\n\n```python\nidx = context.find('research')\nprint(f'Research at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(This grant proposal does not describe any clinical trial phases. It is a computational research proposal focused on developing data analysis algorithms. The research phases described are: algorithm development, validation on benchmark datasets, and publication of results -- not clinical trials.)",
                "is_final": True,
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# Category 5: large_doc_navigation (10 traces)
# Check document size, find structure, navigate methodically.
# ---------------------------------------------------------------------------

LARGE_DOC_TRACES = [
    # 1 - Navigate GPO manual
    {
        "doc": "gpo_manual",
        "question": "What does the GPO style manual say about abbreviations?",
        "category": "large_doc_navigation",
        "turns": [
            {
                "content": "```python\nprint(f'Document length: {len(context)}')\n```"
            },
            {
                "content": "This is a large document. Let me look at the beginning to understand the structure.\n\n```python\nprint(context[:500])\n```"
            },
            {
                "content": "Now let me find the abbreviations section.\n\n```python\nidx = context.find('abbreviat')\nif idx == -1:\n    idx = context.find('Abbreviat')\nprint(f'Abbreviations at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The GPO style manual provides extensive rules on abbreviations. Standard abbreviations are used for titles (Mr., Mrs., Dr.), states (using postal codes in addresses), and common terms in technical writing. Abbreviations should be spelled out on first use with the abbreviation in parentheses.)",
                "is_final": True,
            },
        ],
    },
    # 2 - Navigate household physician
    {
        "doc": "household_physician",
        "question": "What does this medical encyclopedia say about diseases of the eye?",
        "category": "large_doc_navigation",
        "turns": [
            {
                "content": "```python\nprint(f'Document length: {len(context)}')\n```"
            },
            {
                "content": "Very large document. Let me check the beginning for a table of contents.\n\n```python\nprint(context[:500])\n```"
            },
            {
                "content": "Let me search for the eye diseases section.\n\n```python\nidx = context.find('eye')\nprint(f'Eye at: {idx}')\nprint(context[idx:idx+200])\n```"
            },
            {
                "content": "Let me find a more specific section heading.\n\n```python\nidx = context.find('Diseases of the Eye')\nif idx == -1:\n    idx = context.find('diseases of the eye')\nif idx == -1:\n    idx = context.find('EYE')\nprint(f'Section at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The Household Physician covers several diseases of the eye including inflammation of the eyelids, conjunctivitis, cataracts, and problems with vision such as near-sightedness and far-sightedness. It recommends consulting a specialist for serious eye conditions and provides basic home care for minor irritations.)",
                "is_final": True,
            },
        ],
    },
    # 3 - Navigate Cushing's Manual
    {
        "doc": "cushings_manual",
        "question": "How are committees organized according to Cushing's Manual?",
        "category": "large_doc_navigation",
        "turns": [
            {
                "content": "```python\nprint(f'Document length: {len(context)}')\n```"
            },
            {
                "content": "Let me check the structure.\n\n```python\nprint(context[:500])\n```"
            },
            {
                "content": "Now let me find the committees section.\n\n```python\nidx = context.find('committee')\nif idx == -1:\n    idx = context.find('Committee')\nprint(f'Committee at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(According to Cushing's Manual, committees are appointed by the assembly or the presiding officer, depending on the rules of the body. A committee may be a standing committee with ongoing responsibilities or a select committee appointed for a specific purpose. The committee deliberates on the matter referred to it and reports its findings and recommendations back to the assembly.)",
                "is_final": True,
            },
        ],
    },
    # 4 - Navigate Cavalry Outpost
    {
        "doc": "cavalry_outpost",
        "question": "How is this cavalry manual structured and what does it say about the duties of the officer on outpost?",
        "category": "large_doc_navigation",
        "turns": [
            {
                "content": "```python\nprint(f'Document length: {len(context)}')\nprint(context[:500])\n```"
            },
            {
                "content": "Let me find the section about the officer's duties.\n\n```python\nidx = context.find('officer')\nif idx == -1:\n    idx = context.find('Officer')\nprint(f'Officer at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The cavalry outpost manual covers the organization and duties of outpost forces, including picquets, sentries, and patrols. The officer commanding the outpost is responsible for selecting positions, posting sentries, dispatching patrols, and maintaining communication with the main body. The officer must exercise constant vigilance and report all observations of enemy activity without delay.)",
                "is_final": True,
            },
        ],
    },
    # 5 - Navigate Boston Cooking School
    {
        "doc": "boston_cooking_school",
        "question": "What sections does this cookbook cover and what does it say about preserving food?",
        "category": "large_doc_navigation",
        "turns": [
            {
                "content": "```python\nprint(f'Document length: {len(context)}')\n```"
            },
            {
                "content": "Let me look at the table of contents.\n\n```python\nprint(context[:500])\n```"
            },
            {
                "content": "Now let me find the preserving section.\n\n```python\nidx = context.find('preserv')\nif idx == -1:\n    idx = context.find('Preserv')\nprint(f'Preserving at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The Boston Cooking School Cookbook covers a wide range of topics including beverages, breads, soups, meats, vegetables, desserts, and food preservation. The section on preserving discusses methods for canning fruits, making jams and jellies, and pickling vegetables. Key principles include proper sterilization of jars, using the right proportion of sugar, and ensuring airtight seals.)",
                "is_final": True,
            },
        ],
    },
    # 6 - Navigate rules of road at sea
    {
        "doc": "rules_of_road_sea",
        "question": "How is this maritime rules document organized and what does it say about distress signals?",
        "category": "large_doc_navigation",
        "turns": [
            {
                "content": "```python\nprint(f'Document length: {len(context)}')\nprint(context[:500])\n```"
            },
            {
                "content": "Let me find the distress signals section.\n\n```python\nidx = context.find('distress')\nif idx == -1:\n    idx = context.find('Distress')\nprint(f'Distress at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The Rules of the Road at Sea is organized into parts covering steering and sailing rules, lights and shapes, sound and light signals, and special rules. Distress signals include firing a gun at intervals, continuous sounding of a fog signal, rockets or shells throwing red stars, the signal SOS by radiotelegraphy, and the spoken word 'Mayday' by radiotelephony. Any vessel seeing a distress signal is obligated to render assistance.)",
                "is_final": True,
            },
        ],
    },
    # 7 - Navigate employee handbook
    {
        "doc": "employee_handbook",
        "question": "What is the overall structure of this handbook and what does it say about remote work?",
        "category": "large_doc_navigation",
        "turns": [
            {
                "content": "```python\nprint(f'Document length: {len(context)}')\nprint(context[:500])\n```"
            },
            {
                "content": "Let me find the remote work section.\n\n```python\nidx = context.find('remote')\nif idx == -1:\n    idx = context.find('Remote')\nif idx == -1:\n    idx = context.find('telecommut')\nprint(f'Remote work at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The employee handbook is organized into sections covering employment policies, compensation and benefits, workplace conduct, leave policies, and safety. The remote work policy allows eligible employees to work from home up to 3 days per week with manager approval. Remote workers must maintain regular working hours, be reachable during core hours, and ensure a suitable home office setup.)",
                "is_final": True,
            },
        ],
    },
    # 8 - Navigate safety data sheet
    {
        "doc": "safety_data_sheet",
        "question": "Walk me through the structure of this SDS and find the ecological information.",
        "category": "large_doc_navigation",
        "turns": [
            {
                "content": "```python\nprint(f'Document length: {len(context)}')\nprint(context[:500])\n```"
            },
            {
                "content": "SDSs have a standard 16-section format. Let me find the ecological section.\n\n```python\nidx = context.find('ecolog')\nif idx == -1:\n    idx = context.find('Ecolog')\nif idx == -1:\n    idx = context.find('environment')\nprint(f'Ecological at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The SDS follows the standard GHS 16-section format: identification, hazards, composition, first aid, firefighting, accidental release, handling/storage, exposure controls, physical/chemical properties, stability/reactivity, toxicology, ecology, disposal, transport, regulatory, and other info. The ecological information section indicates the material is harmful to aquatic life with long-lasting effects. It should not be released into waterways and spills should be contained immediately.)",
                "is_final": True,
            },
        ],
    },
    # 9 - Navigate product spec
    {
        "doc": "product_spec",
        "question": "What is the structure of this product specification and what warranty information is included?",
        "category": "large_doc_navigation",
        "turns": [
            {
                "content": "```python\nprint(f'Document length: {len(context)}')\nprint(context[:500])\n```"
            },
            {
                "content": "Let me find the warranty section.\n\n```python\nidx = context.find('warranty')\nif idx == -1:\n    idx = context.find('Warranty')\nprint(f'Warranty at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(The product specification covers: overview, technical specifications, physical characteristics, connectivity, power requirements, environmental ratings, and warranty. The warranty provides 2 years of coverage for manufacturing defects, with an optional extended warranty available for purchase. The warranty does not cover damage from misuse, unauthorized modifications, or normal wear and tear.)",
                "is_final": True,
            },
        ],
    },
    # 10 - Navigate GPO manual for specific rule
    {
        "doc": "gpo_manual",
        "question": "How long is the GPO manual and what does it say about formatting numbers?",
        "category": "large_doc_navigation",
        "turns": [
            {
                "content": "```python\nprint(f'Document length: {len(context)}')\nprint(f'Approx pages (at 3000 chars/page): {len(context) // 3000}')\n```"
            },
            {
                "content": "Quite large. Let me check the structure first.\n\n```python\nprint(context[:500])\n```"
            },
            {
                "content": "Now let me find the numbers/numerals section.\n\n```python\nidx = context.find('numeral')\nif idx == -1:\n    idx = context.find('Numeral')\nif idx == -1:\n    idx = context.find('number')\nprint(f'Numbers at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The GPO manual is a substantial document of several hundred pages. For formatting numbers, it specifies that numbers from one to nine are generally spelled out, while 10 and above are expressed in figures. Exceptions include ages, dates, percentages, and measurements, which always use figures. In tables and technical material, all numbers are expressed as figures.)",
                "is_final": True,
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# Category 6: mixed_varied (~16 traces)
# Mix of patterns: count, case-insensitive, rfind, calculations, etc.
# ---------------------------------------------------------------------------

MIXED_TRACES = [
    # 1 - Count occurrences
    {
        "doc": "cavalry_outpost",
        "question": "How many times does the text mention the word 'enemy'?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\ncount = context.lower().count('enemy')\nprint(f'The word enemy appears {count} times')\n```"
            },
            {
                "content": "FINAL(The word 'enemy' appears frequently throughout the cavalry outpost manual, reflecting the central purpose of outpost duty: to observe and guard against the enemy. The text consistently refers to the enemy when describing patrol routes, sentry positions, and the procedures for reporting hostile movements.)",
                "is_final": True,
            },
        ],
    },
    # 2 - Case-insensitive search
    {
        "doc": "boston_cooking_school",
        "question": "Does this cookbook mention chocolate? In what context?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nidx = context.lower().find('chocolate')\nprint(f'Chocolate at: {idx}')\nif idx != -1:\n    print(context[idx:idx+300])\n```"
            },
            {
                "content": "FINAL(Yes, the cookbook mentions chocolate in the context of desserts and confections. Chocolate is used in cake recipes, frosting, and hot beverages. The text provides instructions for melting and tempering chocolate for various preparations.)",
                "is_final": True,
            },
        ],
    },
    # 3 - rfind to get last occurrence
    {
        "doc": "cushings_manual",
        "question": "What is discussed near the end of Cushing's Manual?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nprint(f'Document length: {len(context)}')\nprint(context[-500:])\n```"
            },
            {
                "content": "Let me also check what the last major topic is.\n\n```python\nidx = context.rfind('question')\nif idx == -1:\n    idx = context.rfind('motion')\nif idx == -1:\n    idx = context.rfind('proceed')\nprint(f'Last section at: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(Near the end of Cushing's Manual of Parliamentary Practice, the text covers supplementary rules on the conduct of debate, the rights of members in an assembly, and the resolution of procedural disputes. The final sections serve as a reference for presiding officers on maintaining proper order during deliberations.)",
                "is_final": True,
            },
        ],
    },
    # 4 - Multi-step calculation from found data
    {
        "doc": "lease_agreement",
        "question": "What would be the total cost for the first year including deposit and all monthly payments?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nidx = context.find('rent')\nprint(f'Rent at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "```python\nidx = context.find('deposit')\nprint(f'Deposit at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "FINAL(The total cost for the first year includes the security deposit of $2,500 plus 12 monthly rent payments of $2,500 each, for a total of $2,500 + (12 x $2,500) = $32,500 for the first year.)",
                "is_final": True,
            },
        ],
    },
    # 5 - Count and compare
    {
        "doc": "household_physician",
        "question": "Which is mentioned more frequently: 'fever' or 'pain'?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nfever_count = context.lower().count('fever')\npain_count = context.lower().count('pain')\nprint(f'fever: {fever_count} times')\nprint(f'pain: {pain_count} times')\n```"
            },
            {
                "content": "FINAL(In the Household Physician, both 'fever' and 'pain' are frequently mentioned medical terms. The relative frequency reflects the text's comprehensive coverage of symptoms and treatments across many conditions.)",
                "is_final": True,
            },
        ],
    },
    # 6 - Find first and last mention to determine scope
    {
        "doc": "cavalry_outpost",
        "question": "How extensively does the text discuss 'march' and marching procedures?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nfirst = context.find('march')\nlast = context.rfind('march')\ncount = context.lower().count('march')\nprint(f'First mention at: {first}')\nprint(f'Last mention at: {last}')\nprint(f'Total mentions: {count}')\nprint(f'Span: {last - first} characters')\n```"
            },
            {
                "content": "```python\nfirst = context.find('march')\nprint(context[first:first+300])\n```"
            },
            {
                "content": "FINAL(The text discusses marching procedures throughout, as the movement of cavalry is central to outpost operations. The word 'march' appears multiple times across a wide span of the document. The text covers the order of march, the distance between units on the march, and the precautions to be taken when marching in the presence of the enemy.)",
                "is_final": True,
            },
        ],
    },
    # 7 - Using context.split() to analyze structure
    {
        "doc": "meeting_minutes",
        "question": "How many paragraphs or sections are in these meeting minutes?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nparagraphs = [p.strip() for p in context.split('\\n\\n') if p.strip()]\nprint(f'Number of paragraphs/sections: {len(paragraphs)}')\nfor i, p in enumerate(paragraphs[:5]):\n    print(f'\\nParagraph {i+1} preview: {p[:100]}')\n```"
            },
            {
                "content": "FINAL(The meeting minutes contain several distinct sections/paragraphs covering the meeting header, attendee list, agenda items, discussion notes, decisions made, action items, and adjournment. The document is well-organized into logical sections.)",
                "is_final": True,
            },
        ],
    },
    # 8 - Using context.startswith / checking document type
    {
        "doc": "lab_report",
        "question": "What type of document is this and who authored it?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nprint(context[:300])\n```"
            },
            {
                "content": "```python\nidx = context.lower().find('author')\nif idx == -1:\n    idx = context.lower().find('prepared by')\nif idx == -1:\n    idx = context.lower().find('investigator')\nprint(f'Author info at: {idx}')\nif idx != -1:\n    print(context[idx:idx+200])\n```"
            },
            {
                "content": "FINAL(This is a laboratory report documenting an experimental study. The document begins with a title, author information, and date, followed by standard scientific sections including abstract, introduction, methodology, results, and conclusion.)",
                "is_final": True,
            },
        ],
    },
    # 9 - Finding all occurrences of a pattern
    {
        "doc": "safety_data_sheet",
        "question": "List all the section headers in this safety data sheet.",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nidx = 0\nsections = []\nwhile True:\n    idx = context.find('Section', idx)\n    if idx == -1:\n        break\n    sections.append(context[idx:idx+60].strip())\n    idx += 1\nfor s in sections:\n    print(s)\n```"
            },
            {
                "content": "FINAL(The safety data sheet contains the standard GHS sections: Identification, Hazard Identification, Composition/Ingredients, First-Aid Measures, Fire-Fighting Measures, Accidental Release, Handling and Storage, Exposure Controls, Physical/Chemical Properties, Stability/Reactivity, Toxicological Information, Ecological Information, Disposal Considerations, Transport Information, Regulatory Information, and Other Information.)",
                "is_final": True,
            },
        ],
    },
    # 10 - Checking for contradictions between sections
    {
        "doc": "product_spec",
        "question": "Are there any inconsistencies between the overview and the detailed specs?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nidx = context.find('overview')\nif idx == -1:\n    idx = context.find('Overview')\nprint(f'Overview at: {idx}')\nif idx != -1:\n    print(context[idx:idx+400])\n```"
            },
            {
                "content": "```python\nidx = context.find('specification')\nif idx == -1:\n    idx = context.find('Specification')\nprint(f'Specs at: {idx}')\nif idx != -1:\n    print(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(Based on comparing the overview section with the detailed specifications, the information appears consistent. The overview summarizes the key features that are elaborated in the detailed specs. All stated values in the overview match their corresponding detailed entries.)",
                "is_final": True,
            },
        ],
    },
    # 11 - Using len() to estimate reading time
    {
        "doc": "grant_proposal",
        "question": "How long is this grant proposal? Approximately how long would it take to read?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nchar_count = len(context)\nword_count = len(context.split())\nprint(f'Characters: {char_count}')\nprint(f'Approximate words: {word_count}')\nprint(f'Approximate pages (250 words/page): {word_count // 250}')\nprint(f'Estimated reading time (250 wpm): {word_count // 250} minutes')\n```"
            },
            {
                "content": "FINAL(The grant proposal contains several thousand words across multiple pages. At an average reading speed of 250 words per minute, it would take approximately 15-20 minutes to read through the entire document. This is a typical length for a research grant proposal.)",
                "is_final": True,
            },
        ],
    },
    # 12 - Finding text between two markers
    {
        "doc": "employee_handbook",
        "question": "What is covered between the compensation section and the leave policy section?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nstart = context.lower().find('compensation')\nend = context.lower().find('leave polic')\nif end == -1:\n    end = context.lower().find('leave')\nprint(f'Compensation at: {start}')\nprint(f'Leave policy at: {end}')\nif start != -1 and end != -1:\n    between = context[start:end]\n    print(f'Content between ({len(between)} chars):')\n    print(between[:500])\n```"
            },
            {
                "content": "FINAL(Between the compensation section and the leave policy section, the handbook covers benefits enrollment, health insurance options, retirement plan details, and performance review procedures. This section bridges the discussion of pay with time-off policies.)",
                "is_final": True,
            },
        ],
    },
    # 13 - Case insensitive search with context around match
    {
        "doc": "household_physician",
        "question": "Does this book mention 'vaccination' or 'vaccine'?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nlower = context.lower()\nidx1 = lower.find('vaccination')\nidx2 = lower.find('vaccine')\nprint(f'vaccination at: {idx1}')\nprint(f'vaccine at: {idx2}')\nbest = idx1 if idx1 != -1 else idx2\nif best != -1:\n    start = max(0, best - 100)\n    print(context[start:best+300])\n```"
            },
            {
                "content": "FINAL(The Household Physician does reference vaccination in the context of smallpox prevention. As an older medical text, it discusses the practice of vaccination as established by Edward Jenner and recommends it as a preventive measure against smallpox, which was one of the most feared diseases of the era.)",
                "is_final": True,
            },
        ],
    },
    # 14 - Using multiple find strategies
    {
        "doc": "it_incident_report",
        "question": "When did the incident start and when was it resolved?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nidx_start = context.find('start')\nif idx_start == -1:\n    idx_start = context.find('began')\nif idx_start == -1:\n    idx_start = context.find('detected')\nprint(f'Start at: {idx_start}')\nif idx_start != -1:\n    print(context[idx_start:idx_start+200])\n```"
            },
            {
                "content": "```python\nidx_end = context.find('resolved')\nif idx_end == -1:\n    idx_end = context.find('restored')\nif idx_end == -1:\n    idx_end = context.find('closed')\nprint(f'Resolution at: {idx_end}')\nif idx_end != -1:\n    print(context[idx_end:idx_end+200])\n```"
            },
            {
                "content": "FINAL(The incident was detected at approximately 2:15 AM when monitoring alerts fired. The issue was fully resolved by 4:30 AM after the root cause was identified and the configuration was corrected. Total incident duration was approximately 2 hours and 15 minutes.)",
                "is_final": True,
            },
        ],
    },
    # 15 - Searching for numerical patterns
    {
        "doc": "boston_cooking_school",
        "question": "What oven temperatures are mentioned in this cookbook?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nidx = context.find('degrees')\nif idx == -1:\n    idx = context.find('oven')\nprint(f'First temp reference at: {idx}')\nif idx != -1:\n    print(context[idx:idx+200])\n```"
            },
            {
                "content": "```python\nidx = context.find('oven')\nif idx != -1:\n    idx2 = context.find('oven', idx + 1)\n    idx3 = context.find('oven', idx2 + 1) if idx2 != -1 else -1\n    if idx2 != -1:\n        print(f'Second oven ref at: {idx2}')\n        print(context[idx2:idx2+200])\n    if idx3 != -1:\n        print(f'Third oven ref at: {idx3}')\n        print(context[idx3:idx3+200])\n```"
            },
            {
                "content": "FINAL(The cookbook references several oven temperatures using period-appropriate terms: 'slow oven' (around 250-300 degrees), 'moderate oven' (around 350 degrees), 'hot oven' (around 400-425 degrees), and 'very hot oven' (450+ degrees). These descriptive terms were standard before oven thermometers became common.)",
                "is_final": True,
            },
        ],
    },
    # 16 - Comparing document beginning and end
    {
        "doc": "rules_of_road_sea",
        "question": "How does this maritime rules document begin and end? Is there a summary or conclusion?",
        "category": "mixed_varied",
        "turns": [
            {
                "content": "```python\nprint('=== BEGINNING ===')\nprint(context[:400])\nprint('\\n=== END ===')\nprint(context[-400:])\n```"
            },
            {
                "content": "```python\nidx = context.lower().find('summary')\nif idx == -1:\n    idx = context.lower().find('conclusion')\nprint(f'Summary/conclusion at: {idx}')\nif idx != -1:\n    print(context[idx:idx+400])\nelse:\n    print('No explicit summary or conclusion section found.')\n```"
            },
            {
                "content": "FINAL(The Rules of the Road at Sea begins with general provisions and definitions, establishing the scope and applicability of the rules to all vessels upon the high seas. The document ends with annexes covering technical details of lights, shapes, and sound signals. There is no explicit summary or conclusion -- as a regulatory document, it is structured as a complete reference rather than a narrative with a conclusion.)",
                "is_final": True,
            },
        ],
    },
]
