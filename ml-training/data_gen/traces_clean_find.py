"""
Training traces for the "clean find" pattern.

Each trace follows the same structure:
  1. Assistant searches the document with context.find() using a keyword
  2. Gets a valid position (not -1)
  3. Prints the surrounding text
  4. Gives a FINAL answer

The code in each turn is executed via exec() against the real document
content loaded into a `context` variable, so keywords must actually
exist in the source documents.
"""

CLEAN_FIND_TRACES = [
    # ── cavalry_outpost ────────────────────────────────────────────────
    {
        "doc": "cavalry_outpost",
        "question": "What are the instructions for establishing a patrol route?",
        "category": "clean_find",
        "turns": [
            {
                "content": "I'll search for the keyword 'patrol' to find relevant passages.\n\n```python\nidx = context.find('patrol')\nprint(f'Found at position: {idx}')\nif idx != -1:\n    print(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The manual instructs that patrols should be sent out at irregular intervals along routes that cover the front and flanks of the outpost line. Patrol leaders must note the terrain, observe any signs of the enemy, and report back promptly to the officer in command. Night patrols require particular caution and should avoid well-traveled roads where possible.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "cavalry_outpost",
        "question": "What does the manual say about the duties of a picquet?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Let me look for passages about the picquet.\n\n```python\nidx = context.find('picquet')\nprint(f'Position: {idx}')\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(The manual describes the picquet as a key element of the outpost system. A picquet is a body of troops posted at a specific point to guard against surprise. The officer commanding the picquet is responsible for posting sentries, maintaining communication with adjacent picquets, and ensuring that no enemy force can advance undetected.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "cavalry_outpost",
        "question": "How should cavalry officers handle a night march?",
        "category": "clean_find",
        "turns": [
            {
                "content": "I'll search for guidance on night operations.\n\n```python\npos = context.lower().find('night')\nprint(f'Found at: {pos}')\nif pos != -1:\n    start = max(0, pos - 50)\n    print(context[start:pos+450])\n```"
            },
            {
                "content": "FINAL(The manual advises that night marches require heightened vigilance and strict noise discipline. Officers should ensure the advance guard moves at a cautious pace, that horses are kept well in hand, and that frequent halts are made to listen for signs of the enemy. Communication between the main body and the advance is critical during darkness.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "cavalry_outpost",
        "question": "What does the manual say about reporting enemy movements?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Let me search for instructions on reporting.\n\n```python\nidx = context.find('report')\nprint(idx)\nif idx != -1:\n    print(context[idx:idx+500])\nelse:\n    print('not found')\n```"
            },
            {
                "content": "FINAL(The manual stresses that every officer and non-commissioned officer on outpost duty must send reports of enemy movements without delay. Reports should state the direction and estimated strength of the enemy, the time of observation, and the reporter's position. Accurate and timely reporting allows the commanding officer to make informed decisions about advancing or withdrawing forces.)",
                "is_final": True,
            },
        ],
    },
    # ── boston_cooking_school ────────────────────────────────────────────
    {
        "doc": "boston_cooking_school",
        "question": "How does the cookbook say to make pie crust?",
        "category": "clean_find",
        "turns": [
            {
                "content": "I'll look for pie crust instructions.\n\n```python\nidx = context.lower().find('pie crust')\nprint(f'Found at: {idx}')\nif idx != -1:\n    print(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The Boston Cooking-School Cook Book provides instructions for making pie crust using flour, butter or lard, salt, and cold water. The dough should be handled as little as possible to keep it flaky, and the ingredients should be kept cold throughout the process.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "boston_cooking_school",
        "question": "What does the recipe for sugar cookies look like?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Searching for sugar cookie references.\n\n```python\npos = context.find('sugar')\nprint(f'Position: {pos}')\nprint(context[pos:pos+300])\n```"
            },
            {
                "content": "FINAL(The cookbook includes recipes using sugar extensively. Sugar cookies and related recipes call for butter, sugar, eggs, flour, and flavoring. The Boston Cooking-School Cook Book was one of the first to use standardized measurements, making its recipes reproducible.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "boston_cooking_school",
        "question": "What does the cookbook say about baking bread?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Let me search for bread baking instructions.\n\n```python\nidx = context.find('flour')\nprint(f'Found \"flour\" at position {idx}')\nif idx != -1:\n    print(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(The cookbook discusses flour as a fundamental ingredient in bread making. It covers different types of flour and their properties, and provides detailed instructions for kneading, rising, and baking bread at proper temperatures.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "boston_cooking_school",
        "question": "Are there any recipes using eggs and cream together?",
        "category": "clean_find",
        "turns": [
            {
                "content": "I'll look for a passage mentioning cream in the cookbook.\n\n```python\nidx = context.find('cream')\nprint(f'Found at: {idx}')\nstart = max(0, idx - 100)\nprint(context[start:idx+400])\n```"
            },
            {
                "content": "FINAL(Yes, the Boston Cooking-School Cook Book contains numerous recipes combining eggs and cream, including custards, cream sauces, ice creams, and various desserts. Cream is used extensively throughout the book as a key ingredient in both sweet and savory dishes.)",
                "is_final": True,
            },
        ],
    },
    # ── cushings_manual ──────────────────────────────────────────────────
    {
        "doc": "cushings_manual",
        "question": "What is the procedure for making a motion in Cushing's Manual?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Let me find the section on motions.\n\n```python\nidx = context.find('motion')\nprint(f'Found at: {idx}')\nif idx != -1:\n    print(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(According to Cushing's Manual, a motion is a proposal that the assembly take certain action. A member must first obtain the floor by being recognized by the presiding officer, then state the motion. The motion requires a second before it can be considered. Once seconded, the presiding officer states the question and the assembly proceeds to consider it.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "cushings_manual",
        "question": "What constitutes a quorum according to this parliamentary manual?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Searching for the quorum definition.\n\n```python\npos = context.lower().find('quorum')\nprint(pos, context[pos:pos+400] if pos != -1 else 'not found')\n```"
            },
            {
                "content": "FINAL(The manual defines a quorum as the number of members required to be present for the assembly to validly transact business. Without a quorum present, no binding decisions can be made. The specific number constituting a quorum is typically established by the organization's rules or bylaws.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "cushings_manual",
        "question": "How does debate work according to this manual of parliamentary practice?",
        "category": "clean_find",
        "turns": [
            {
                "content": "I'll look for the section on debate.\n\n```python\nidx = context.find('debate')\nprint(f'Position: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(According to Cushing's Manual, debate is the process by which members discuss a pending question. Members must be recognized by the presiding officer before speaking, remarks must be relevant to the question at hand, and members should address the chair rather than other members directly. The presiding officer maintains order during debate.)",
                "is_final": True,
            },
        ],
    },
    # ── product_spec ────────────────────────────────────────────────────
    {
        "doc": "product_spec",
        "question": "What is the warranty period for the ThermoSense Pro X1?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Let me check the warranty section.\n\n```python\nidx = context.find('warranty')\nif idx == -1:\n    idx = context.lower().find('warranty')\nprint(f'Found at: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "FINAL(The ThermoSense Pro X1 product specification includes warranty information covering the device. The warranty details outline the coverage period and what is included or excluded from the manufacturer's warranty.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "product_spec",
        "question": "Does the ThermoSense Pro X1 support WiFi connectivity?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Searching for WiFi details in the spec.\n\n```python\npos = context.find('WiFi')\nif pos == -1:\n    pos = context.lower().find('wifi')\nprint(f'Found at: {pos}')\nif pos != -1:\n    start = max(0, pos - 50)\n    print(context[start:pos+300])\n```"
            },
            {
                "content": "FINAL(Yes, the ThermoSense Pro X1 supports WiFi connectivity. The product specification details the WiFi capabilities, which allow the thermostat to connect to a home network for remote control and monitoring through a companion app.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "product_spec",
        "question": "What temperature range can the ThermoSense measure?",
        "category": "clean_find",
        "turns": [
            {
                "content": "I'll search for the temperature specifications.\n\n```python\nidx = context.lower().find('temperature')\nprint(idx)\nprint(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(The ThermoSense Pro X1 specification lists the temperature measurement capabilities of the device, including the operating range for both the thermostat's internal sensor and any external humidity/temperature sensors it supports.)",
                "is_final": True,
            },
        ],
    },
    # ── lease_agreement ─────────────────────────────────────────────────
    {
        "doc": "lease_agreement",
        "question": "What is the pet policy for the apartment?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Let me find the pet policy section.\n\n```python\nidx = context.lower().find('pet')\nprint(f'Found at position: {idx}')\nif idx != -1:\n    print(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The Oakwood Apartments lease agreement includes a pet policy section that specifies the rules regarding pets on the premises, including any pet deposits, breed or weight restrictions, and the tenant's responsibilities for pet-related damages.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "lease_agreement",
        "question": "How much is the security deposit?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Searching for the deposit amount.\n\n```python\npos = context.find('deposit')\nprint(f'Position: {pos}')\nprint(context[pos:pos+300])\n```"
            },
            {
                "content": "FINAL(The Oakwood Apartments lease agreement specifies the security deposit amount that the tenant must pay upon signing. The deposit section also covers the conditions under which the deposit may be partially or fully withheld, and the timeline for its return after move-out.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "lease_agreement",
        "question": "What are the parking rules in the lease?",
        "category": "clean_find",
        "turns": [
            {
                "content": "I'll look for parking provisions.\n\n```python\nidx = context.lower().find('parking')\nprint(idx, context[idx:idx+400] if idx != -1 else 'not found')\n```"
            },
            {
                "content": "FINAL(The lease agreement includes provisions regarding parking. It outlines the assigned parking spaces, guest parking rules, and any additional fees for covered or reserved parking at Oakwood Apartments.)",
                "is_final": True,
            },
        ],
    },
    # ── lab_report ──────────────────────────────────────────────────────
    {
        "doc": "lab_report",
        "question": "What were the pH levels recorded in the water quality report?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Let me search for pH measurements.\n\n```python\nidx = context.find('pH')\nprint(f'Found at: {idx}')\nif idx != -1:\n    start = max(0, idx - 100)\n    print(context[start:idx+400])\n```"
            },
            {
                "content": "FINAL(The Clearwater water quality analysis lab report includes pH measurements. The report documents the pH levels found in the water samples, which is a critical indicator of water quality and must fall within acceptable ranges for safe consumption.)",
                "is_final": True,
            },
        ],
    },
    {
        "doc": "lab_report",
        "question": "Was lead detected in the water samples?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Searching for lead test results.\n\n```python\nidx = context.lower().find('lead')\nprint(f'Position: {idx}')\nprint(context[idx:idx+300])\n```"
            },
            {
                "content": "FINAL(The Clearwater lab report includes analysis for lead content in the water samples. The results indicate whether lead levels were detected and whether they fall within the EPA's acceptable limits for drinking water.)",
                "is_final": True,
            },
        ],
    },
    # ── employee_handbook ───────────────────────────────────────────────
    {
        "doc": "employee_handbook",
        "question": "How much PTO do new employees receive?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Let me find the PTO policy.\n\n```python\nidx = context.find('PTO')\nif idx == -1:\n    idx = context.lower().find('paid time off')\nprint(f'Found at: {idx}')\nif idx != -1:\n    print(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The employee handbook outlines the PTO (Paid Time Off) policy for new employees, including the accrual rate, when PTO becomes available, and any caps on accumulated time. The policy details differ based on employment status and tenure.)",
                "is_final": True,
            },
        ],
    },
    # ── safety_data_sheet ───────────────────────────────────────────────
    {
        "doc": "safety_data_sheet",
        "question": "What are the first aid measures for skin contact with CleanMax?",
        "category": "clean_find",
        "turns": [
            {
                "content": "I'll search for first aid information.\n\n```python\npos = context.lower().find('first aid')\nprint(f'Found at: {pos}')\nif pos != -1:\n    print(context[pos:pos+500])\n```"
            },
            {
                "content": "FINAL(The CleanMax Industrial Degreaser Safety Data Sheet includes first aid measures for skin contact. The SDS recommends removing contaminated clothing, washing the affected area thoroughly with soap and water, and seeking medical attention if irritation persists.)",
                "is_final": True,
            },
        ],
    },
    # ── meeting_minutes ─────────────────────────────────────────────────
    {
        "doc": "meeting_minutes",
        "question": "What budget items were discussed at the board meeting?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Searching for budget discussion in the minutes.\n\n```python\nidx = context.lower().find('budget')\nprint(f'Found at: {idx}')\nif idx != -1:\n    start = max(0, idx - 50)\n    print(context[start:idx+400])\n```"
            },
            {
                "content": "FINAL(The Riverside Community Association board meeting minutes include discussion of budget items. The minutes record the budget proposals presented, any motions made regarding budget allocation, and the outcomes of votes on financial matters.)",
                "is_final": True,
            },
        ],
    },
    # ── grant_proposal ──────────────────────────────────────────────────
    {
        "doc": "grant_proposal",
        "question": "What is the research methodology described in the grant proposal?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Let me find the methodology section.\n\n```python\nidx = context.lower().find('neural network')\nprint(f'Found at: {idx}')\nprint(context[idx:idx+500])\n```"
            },
            {
                "content": "FINAL(The NSF grant proposal for neural networks in climate modeling describes a methodology that uses deep learning architectures to improve climate prediction accuracy. The research approach includes training neural networks on historical climate data and validating predictions against known outcomes.)",
                "is_final": True,
            },
        ],
    },
    # ── it_incident_report ──────────────────────────────────────────────
    {
        "doc": "it_incident_report",
        "question": "What was the root cause of the database outage?",
        "category": "clean_find",
        "turns": [
            {
                "content": "I'll search for the root cause analysis.\n\n```python\nidx = context.lower().find('root cause')\nif idx == -1:\n    idx = context.lower().find('database')\nprint(f'Found at: {idx}')\nif idx != -1:\n    print(context[idx:idx+400])\n```"
            },
            {
                "content": "FINAL(The IT incident report INC-2025-0892 documents a database outage. The root cause analysis identifies the factors that led to the outage, the timeline of events, and the corrective actions taken to restore service and prevent recurrence.)",
                "is_final": True,
            },
        ],
    },
    # ── household_physician ─────────────────────────────────────────────
    {
        "doc": "household_physician",
        "question": "What does the medical reference say about treating a fever?",
        "category": "clean_find",
        "turns": [
            {
                "content": "Searching for fever treatment guidance.\n\n```python\npos = context.lower().find('fever')\nprint(pos)\nif pos != -1:\n    print(context[pos:pos+500])\n```"
            },
            {
                "content": "FINAL(The Household Physician medical reference includes guidance on treating fevers. The text describes the symptoms of fever, its common causes, and the recommended treatments available at the time of publication, including rest, hydration, and various remedies.)",
                "is_final": True,
            },
        ],
    },
]
