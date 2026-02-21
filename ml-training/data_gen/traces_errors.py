"""
Training traces for error-correction categories.

Each trace is a multi-turn conversation where the assistant makes a mistake
(redefining context, responding without code, runtime error, or ignoring context)
and then corrects itself. These teach the model to recover from common failure modes.

IMPORTANT: Each code turn is executed independently via exec(). Variables from
previous turns are NOT preserved -- every turn must be self-contained.
"""

# ---------------------------------------------------------------------------
# Category 1: error_redefine_context
# Assistant tries to redefine the `context` variable, gets canned error, corrects.
# ---------------------------------------------------------------------------

REDEFINE_CONTEXT_TRACES = [
    # Trace 1: open() redefinition -- cavalry_outpost
    {
        "doc": "cavalry_outpost",
        "question": "What does the text say about the duties of a picquet?",
        "category": "error_redefine_context",
        "turns": [
            {
                "content": "```python\ncontext = open('cavalry_outpost.txt').read()\nidx = context.find('picquet')\nprint(context[idx:idx+500])\n```",
                "error_type": "redefine_context",
            },
            {
                "content": "```python\nidx = context.find('picquet')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('picquet')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "The text describes the picquet as a body of troops posted at a short distance from the main force to provide security. The picquet's duties include maintaining sentries, sending out patrols, and being ready to resist any advance by the enemy. The officer in command of the picquet must remain vigilant and report any movements to the outpost commander.",
                "is_final": True,
            },
        ],
    },
    # Trace 2: load_document() redefinition -- household_physician
    {
        "doc": "household_physician",
        "question": "What remedies does the text recommend for a common cold?",
        "category": "error_redefine_context",
        "turns": [
            {
                "content": "```python\ncontext = load_document('household_physician.pdf')\nprint(context[:500])\n```",
                "error_type": "redefine_context",
            },
            {
                "content": "```python\nidx = context.find('cold')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('cold')\nprint(context[idx:idx+600])\n```",
            },
            {
                "content": "The text recommends several remedies for a common cold, including rest, warm fluids, and keeping the patient in a well-ventilated room. It advises against heavy medication in mild cases, instead suggesting hot foot baths and light diet to help the body recover naturally.",
                "is_final": True,
            },
        ],
    },
    # Trace 3: requests.get() redefinition -- boston_cooking_school
    {
        "doc": "boston_cooking_school",
        "question": "How does the book suggest making white sauce?",
        "category": "error_redefine_context",
        "turns": [
            {
                "content": "```python\nimport requests\ncontext = requests.get('http://example.com/boston_cooking.txt').text\nprint(context.find('white sauce'))\n```",
                "error_type": "redefine_context",
            },
            {
                "content": "```python\nidx = context.find('White Sauce')\nif idx == -1:\n    idx = context.find('white sauce')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('White Sauce')\nif idx == -1:\n    idx = context.find('white sauce')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "The Boston Cooking-School Cook Book describes white sauce as a foundational recipe made from butter, flour, and milk. The butter is melted, flour is stirred in to form a roux, and then milk is added gradually while stirring to prevent lumps. Different thicknesses are achieved by varying the ratio of flour to liquid.",
                "is_final": True,
            },
        ],
    },
    # Trace 4: triple-quoted literal redefinition -- rules_of_road_sea
    {
        "doc": "rules_of_road_sea",
        "question": "What are the rules for vessels meeting head-on?",
        "category": "error_redefine_context",
        "turns": [
            {
                "content": '```python\ncontext = """Rules of the Road at Sea - Full Text"""\nidx = context.find(\'head-on\')\nprint(context[idx:idx+300])\n```',
                "error_type": "redefine_context",
            },
            {
                "content": "```python\nidx = context.find('head-on')\nif idx == -1:\n    idx = context.find('head on')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('head-on')\nif idx == -1:\n    idx = context.find('head on')\nif idx == -1:\n    idx = context.find('meeting')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "When two vessels are meeting head-on or nearly head-on, both vessels must alter their course to starboard so that each passes on the port side of the other. This rule applies when vessels are approaching on reciprocal or nearly reciprocal courses. If there is any doubt whether the situation exists, it should be assumed to exist and the rule should be followed.",
                "is_final": True,
            },
        ],
    },
    # Trace 5: with open() redefinition -- cushings_manual
    {
        "doc": "cushings_manual",
        "question": "How does the assembly handle a motion to adjourn?",
        "category": "error_redefine_context",
        "turns": [
            {
                "content": "```python\nwith open('data/cushings_manual.txt') as f:\n    context = f.read()\nidx = context.find('adjourn')\nprint(context[idx:idx+400])\n```",
                "error_type": "redefine_context",
            },
            {
                "content": "```python\nidx = context.find('motion to adjourn')\nif idx == -1:\n    idx = context.find('adjourn')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('motion to adjourn')\nif idx == -1:\n    idx = context.find('adjourn')\nprint(context[idx:idx+600])\n```",
            },
            {
                "content": "According to Cushing's Manual, a motion to adjourn is always in order and takes precedence over other motions. The motion requires a second and a majority vote. When the motion is carried, the presiding officer declares the assembly adjourned. The motion to adjourn cannot be debated or amended.",
                "is_final": True,
            },
        ],
    },
    # Trace 6: json.load() redefinition -- product_spec
    {
        "doc": "product_spec",
        "question": "What are the performance requirements listed in the product spec?",
        "category": "error_redefine_context",
        "turns": [
            {
                "content": "```python\nimport json\nwith open('product_spec.json') as f:\n    context = json.load(f)\nprint(context['performance'])\n```",
                "error_type": "redefine_context",
            },
            {
                "content": "```python\nidx = context.find('performance')\nif idx == -1:\n    idx = context.find('Performance')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('Performance')\nif idx == -1:\n    idx = context.find('performance')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "The product specification lists several performance requirements including a maximum response latency of 200ms for API calls, 99.9% uptime SLA, support for at least 10,000 concurrent users, and data processing throughput of 500 records per second. It also specifies that page load time should not exceed 3 seconds under normal conditions.",
                "is_final": True,
            },
        ],
    },
    # Trace 7: pathlib read_text() redefinition -- lease_agreement
    {
        "doc": "lease_agreement",
        "question": "What are the tenant's obligations regarding maintenance?",
        "category": "error_redefine_context",
        "turns": [
            {
                "content": "```python\nfrom pathlib import Path\ncontext = Path('lease_agreement.txt').read_text()\nprint(context.find('maintenance'))\n```",
                "error_type": "redefine_context",
            },
            {
                "content": "```python\nidx = context.find('maintenance')\nif idx == -1:\n    idx = context.find('Maintenance')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('Maintenance')\nif idx == -1:\n    idx = context.find('maintenance')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "The lease agreement specifies that the tenant is responsible for routine maintenance of the premises including keeping the unit clean, replacing light bulbs and air filters, maintaining plumbing fixtures, and promptly reporting any damage or needed repairs to the landlord. Major structural repairs remain the landlord's responsibility.",
                "is_final": True,
            },
        ],
    },
    # Trace 8: document_text variable reassignment -- gpo_manual
    {
        "doc": "gpo_manual",
        "question": "What does the GPO manual say about capitalizing titles?",
        "category": "error_redefine_context",
        "turns": [
            {
                "content": "```python\ncontext = document_text\nidx = context.find('capitalize')\nprint(context[idx:idx+400])\n```",
                "error_type": "redefine_context",
            },
            {
                "content": "```python\nidx = context.find('capitaliz')\nif idx == -1:\n    idx = context.lower().find('capitaliz')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('capitaliz')\nif idx == -1:\n    idx = context.find('Capitaliz')\nprint(context[idx:idx+600])\n```",
            },
            {
                "content": "The GPO Style Manual provides detailed rules for capitalizing titles. Official titles of persons are capitalized when preceding a name (e.g., President Lincoln) but are lowercased when used as a general description or following a name. Titles of publications, acts, and treaties follow specific capitalization conventions outlined in the manual's dedicated chapter.",
                "is_final": True,
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Category 2: error_no_code
# Assistant responds with plain text instead of code, gets canned error, corrects.
# ---------------------------------------------------------------------------

NO_CODE_TRACES = [
    # Trace 1: Generic knowledge answer -- cavalry_outpost
    {
        "doc": "cavalry_outpost",
        "question": "What does the text say about the role of the advance guard?",
        "category": "error_no_code",
        "turns": [
            {
                "content": "Based on typical military manuals, the advance guard is a detachment sent ahead of the main body to prevent surprise and to gather information about the enemy. The advance guard typically consists of cavalry and is responsible for clearing the road and securing key terrain features.",
                "error_type": "no_code",
            },
            {
                "content": "```python\nidx = context.find('advance')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('advance')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "According to the text, the advance guard moves ahead of the main body along the line of march. Its duty is to clear the road of enemy forces, secure bridges and defiles, and give timely warning of the enemy's approach. The strength and composition of the advance guard depends on the distance from the enemy and the nature of the terrain.",
                "is_final": True,
            },
        ],
    },
    # Trace 2: Clarifying question -- household_physician
    {
        "doc": "household_physician",
        "question": "What does the book recommend for treating burns?",
        "category": "error_no_code",
        "turns": [
            {
                "content": "Could you specify what type of burn you're asking about? There are several classifications -- first-degree, second-degree, and third-degree burns -- and the recommended treatment varies significantly depending on severity. Also, are you looking for emergency first aid or long-term care guidance?",
                "error_type": "no_code",
            },
            {
                "content": "```python\nidx = context.find('burn')\nif idx == -1:\n    idx = context.find('Burns')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('burn')\nif idx == -1:\n    idx = context.find('Burns')\nprint(context[idx:idx+600])\n```",
            },
            {
                "content": "The book recommends applying cold water or ice immediately to a burn to reduce pain and swelling. For minor burns, it suggests covering the area with a clean cloth and applying soothing ointments. For more severe burns, it advises seeking medical attention promptly and warns against breaking blisters or applying grease or butter to the wound.",
                "is_final": True,
            },
        ],
    },
    # Trace 3: Confident wrong answer from "common knowledge" -- boston_cooking_school
    {
        "doc": "boston_cooking_school",
        "question": "What temperature does the cookbook recommend for roasting beef?",
        "category": "error_no_code",
        "turns": [
            {
                "content": "For roasting beef, the standard temperature is 350 degrees Fahrenheit. You should cook it for approximately 20 minutes per pound for medium-rare, or 25 minutes per pound for medium. Always let the meat rest for 10-15 minutes before carving.",
                "error_type": "no_code",
            },
            {
                "content": "```python\nidx = context.find('roast')\nif idx == -1:\n    idx = context.find('Roast')\nprint(idx)\n```",
            },
            {
                "content": "```python\nfor keyword in ['roast beef', 'Roast Beef', 'roasting', 'beef']:\n    idx = context.find(keyword)\n    if idx != -1:\n        print(f'{keyword}: position {idx}')\n        print(context[idx:idx+500])\n        print('---')\n        break\n```",
            },
            {
                "content": "According to the Boston Cooking-School Cook Book, roasting beef should be done in a hot oven. The book provides specific timing instructions based on the cut and weight of the meat, emphasizing the importance of searing the outside at high heat first to retain juices, then reducing heat for the remainder of cooking. The exact temperatures differ from modern conventions as the book predates standardized oven thermometers.",
                "is_final": True,
            },
        ],
    },
    # Trace 4: Polite deflection -- employee_handbook
    {
        "doc": "employee_handbook",
        "question": "What is the company's policy on remote work?",
        "category": "error_no_code",
        "turns": [
            {
                "content": "I'd be happy to help you with that! Remote work policies can vary quite a bit between organizations. Generally, companies have been moving toward hybrid models since the pandemic. I'd recommend checking with your HR department for the most up-to-date policy details specific to your role and department.",
                "error_type": "no_code",
            },
            {
                "content": "```python\nidx = context.find('remote')\nif idx == -1:\n    idx = context.find('Remote')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('Remote')\nif idx == -1:\n    idx = context.find('remote')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "According to the employee handbook, the company allows eligible employees to work remotely up to three days per week with manager approval. Employees must maintain a dedicated workspace, remain available during core hours of 10 AM to 3 PM, and attend all mandatory in-person meetings. Remote work arrangements are reviewed quarterly and may be revoked for performance issues.",
                "is_final": True,
            },
        ],
    },
    # Trace 5: Generic knowledge with hedging -- safety_data_sheet
    {
        "doc": "safety_data_sheet",
        "question": "What are the first aid measures for skin contact with the chemical?",
        "category": "error_no_code",
        "turns": [
            {
                "content": "Generally speaking, for chemical skin contact the standard first aid procedure is to immediately flush the affected area with plenty of water for at least 15-20 minutes. Remove contaminated clothing and seek medical attention if irritation persists. However, specific chemicals may have different requirements.",
                "error_type": "no_code",
            },
            {
                "content": "```python\nidx = context.find('skin contact')\nif idx == -1:\n    idx = context.find('Skin Contact')\nif idx == -1:\n    idx = context.find('SKIN CONTACT')\nprint(idx)\n```",
            },
            {
                "content": "```python\nfor term in ['Skin Contact', 'skin contact', 'SKIN CONTACT', 'First Aid']:\n    idx = context.find(term)\n    if idx != -1:\n        print(f'Found \"{term}\" at {idx}')\n        print(context[idx:idx+500])\n        break\n```",
            },
            {
                "content": "According to the safety data sheet, for skin contact with this chemical: immediately remove contaminated clothing and flush the affected skin with copious amounts of lukewarm water for at least 20 minutes. Do not use hot water. If a rash, burning, or irritation develops, seek medical attention. Wash contaminated clothing before reuse. The SDS also notes that prolonged exposure may cause dermatitis.",
                "is_final": True,
            },
        ],
    },
    # Trace 6: Asking for more context -- lab_report
    {
        "doc": "lab_report",
        "question": "What were the results of the pH analysis?",
        "category": "error_no_code",
        "turns": [
            {
                "content": "Before I can answer that, I need a bit more context. Which samples are you referring to? Lab reports typically contain multiple test results across different samples and methodologies. Could you point me to the specific section or sample ID you're interested in?",
                "error_type": "no_code",
            },
            {
                "content": "```python\nidx = context.find('pH')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('pH')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "The lab report shows pH analysis results for three samples: Sample A measured 6.8, Sample B measured 7.2, and Sample C measured 5.9. All samples were tested using a calibrated digital pH meter at 25 degrees Celsius. The report notes that Sample C's acidic reading was outside the expected range and flagged for retesting.",
                "is_final": True,
            },
        ],
    },
    # Trace 7: Overly verbose non-answer -- grant_proposal
    {
        "doc": "grant_proposal",
        "question": "What is the total budget requested in the grant proposal?",
        "category": "error_no_code",
        "turns": [
            {
                "content": "Grant proposals typically include detailed budget breakdowns covering personnel costs, equipment, supplies, travel, and indirect costs. The total budget depends on the scope and duration of the proposed research. Federal grants from agencies like NSF or NIH often have specific budget caps depending on the funding mechanism.",
                "error_type": "no_code",
            },
            {
                "content": "```python\nfor term in ['budget', 'Budget', 'total', 'Total', '$']:\n    idx = context.find(term)\n    if idx != -1:\n        print(f'\"{term}\" at {idx}: {context[idx:idx+200]}')\n        print('---')\n```",
            },
            {
                "content": "```python\nidx = context.find('Budget')\nif idx == -1:\n    idx = context.find('budget')\nprint(context[idx:idx+600])\n```",
            },
            {
                "content": "The grant proposal requests a total budget of $1,250,000 over three years. This breaks down to approximately $450,000 for personnel (PI salary, two graduate research assistants, and a postdoc), $200,000 for equipment, $150,000 for supplies and materials, $50,000 for travel, and $400,000 in indirect costs at the university's negotiated rate.",
                "is_final": True,
            },
        ],
    },
    # Trace 8: Conversational non-answer -- meeting_minutes
    {
        "doc": "meeting_minutes",
        "question": "What action items were assigned at the meeting?",
        "category": "error_no_code",
        "turns": [
            {
                "content": "Action items in meetings are usually assigned to specific team members with deadlines. They typically cover follow-up tasks discussed during the meeting. Let me know if you'd like help organizing or tracking action items -- I can suggest some project management tools that work well for that!",
                "error_type": "no_code",
            },
            {
                "content": "```python\nidx = context.find('action item')\nif idx == -1:\n    idx = context.find('Action Item')\nif idx == -1:\n    idx = context.find('ACTION')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('Action')\nif idx == -1:\n    idx = context.find('action')\nprint(context[idx:idx+600])\n```",
            },
            {
                "content": "According to the meeting minutes, three action items were assigned: (1) Sarah will prepare the Q3 budget revision by Friday, (2) Mike will schedule vendor demos for the new CRM system by next Tuesday, and (3) the engineering team will provide an updated project timeline by end of week. All items are to be reviewed at the next weekly standup.",
                "is_final": True,
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Category 3: error_runtime
# Assistant writes code that produces a real Python runtime error.
# NO error_type set -- the exec engine produces a real traceback.
# ---------------------------------------------------------------------------

RUNTIME_ERROR_TRACES = [
    # Trace 1: NameError -- undefined variable -- cavalry_outpost
    {
        "doc": "cavalry_outpost",
        "question": "What does the text say about the qualities of a good outpost officer?",
        "category": "error_runtime",
        "turns": [
            {
                "content": "```python\nidx = context.find('officer')\nprint(context[start_pos:start_pos+500])\n```",
            },
            {
                "content": "```python\nidx = context.find('officer')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "```python\nidx = context.find('duty')\nif idx == -1:\n    idx = context.find('command')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "The text describes the qualities expected of a good outpost officer: vigilance, sound judgment, and knowledge of the terrain. The officer must be able to make quick decisions, maintain discipline among the guard, and accurately report the enemy's movements to the commanding officer without delay.",
                "is_final": True,
            },
        ],
    },
    # Trace 2: IndexError -- boston_cooking_school
    {
        "doc": "boston_cooking_school",
        "question": "What are the different types of soups described in the cookbook?",
        "category": "error_runtime",
        "turns": [
            {
                "content": "```python\nsections = context.split('CHAPTER')\nprint(sections[50])\n```",
            },
            {
                "content": "```python\nidx = context.find('soup')\nif idx == -1:\n    idx = context.find('Soup')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('Soup')\nif idx == -1:\n    idx = context.find('soup')\nprint(context[idx:idx+800])\n```",
            },
            {
                "content": "The cookbook describes several categories of soups including clear soups (bouillon and consomme), thick soups (cream soups, purees, and bisques), and chowders. It explains that stock forms the foundation of most soups and provides detailed instructions for preparing both white and brown stock from meat bones and vegetables.",
                "is_final": True,
            },
        ],
    },
    # Trace 3: NameError -- calling undefined function -- rules_of_road_sea
    {
        "doc": "rules_of_road_sea",
        "question": "What lights must a sailing vessel display at night?",
        "category": "error_runtime",
        "turns": [
            {
                "content": "```python\nresult = search_document('sailing vessel', 'lights')\nprint(result)\n```",
            },
            {
                "content": "```python\nidx = context.find('sailing vessel')\nif idx == -1:\n    idx = context.find('sailing')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('sailing')\nprint(context[idx:idx+600])\n```",
            },
            {
                "content": "According to the rules, a sailing vessel underway at night must display sidelights (red on port, green on starboard) and a sternlight (white). Optionally, a sailing vessel may display two all-round lights at or near the top of the mast -- the upper one red and the lower one green. A sailing vessel under 20 meters may combine all these lights into a single lantern at the masthead.",
                "is_final": True,
            },
        ],
    },
    # Trace 4: AttributeError -- nonexistent method -- cushings_manual
    {
        "doc": "cushings_manual",
        "question": "What is the procedure for calling the previous question?",
        "category": "error_runtime",
        "turns": [
            {
                "content": "```python\nresults = context.search('previous')\nprint(results)\n```",
            },
            {
                "content": "```python\nidx = context.find('previous')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('previous')\nprint(context[idx:idx+600])\n```",
            },
            {
                "content": "According to Cushing's Manual, calling the previous question is a motion to end debate and proceed immediately to a vote on the pending question. A member calls for the previous question, and if seconded, the presiding officer puts it to the assembly. If adopted by a majority vote, debate ceases and the assembly votes on the original motion without further discussion.",
                "is_final": True,
            },
        ],
    },
    # Trace 5: ZeroDivisionError -- gpo_manual
    {
        "doc": "gpo_manual",
        "question": "How does the GPO manual handle abbreviations?",
        "category": "error_runtime",
        "turns": [
            {
                "content": "```python\ncount = context.count('abbreviation')\navg_spacing = len(context) / (count - count)\nprint(f'Average spacing: {avg_spacing}')\n```",
            },
            {
                "content": "```python\nidx = context.find('abbreviation')\nif idx == -1:\n    idx = context.find('Abbreviation')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('Abbreviation')\nif idx == -1:\n    idx = context.find('abbreviation')\nprint(context[idx:idx+600])\n```",
            },
            {
                "content": "The GPO Style Manual provides extensive guidelines on abbreviations. Standard abbreviations are used for titles before names (Mr., Mrs., Dr.), geographic terms (U.S., D.C.), and units of measure. The manual specifies that abbreviations should generally be avoided in formal text except for well-established ones. It includes comprehensive lists of approved abbreviations for government agencies, military terms, and technical usage.",
                "is_final": True,
            },
        ],
    },
    # Trace 6: SyntaxError -- bad f-string -- lease_agreement
    {
        "doc": "lease_agreement",
        "question": "What is the lease duration and renewal process?",
        "category": "error_runtime",
        "turns": [
            {
                "content": "```python\ncount = context.count('lease')\nprint(f\"Found {context.count('lease') results for 'lease'\")\n```",
            },
            {
                "content": "```python\nidx = context.find('duration')\nif idx == -1:\n    idx = context.find('term')\nif idx == -1:\n    idx = context.find('Term')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('Term')\nif idx == -1:\n    idx = context.find('term')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "The lease agreement specifies a 12-month term beginning on the first of the month following signing. Renewal is automatic for successive 12-month periods unless either party provides written notice of termination at least 60 days before the lease expiration. Rent may be increased upon renewal with 30 days written notice. Early termination requires a fee equal to two months' rent.",
                "is_final": True,
            },
        ],
    },
    # Trace 7: TypeError -- wrong argument type -- product_spec
    {
        "doc": "product_spec",
        "question": "What authentication methods does the product support?",
        "category": "error_runtime",
        "turns": [
            {
                "content": "```python\nlines = context.split('\\n')\nfiltered = list(filter('auth', lines))\nprint(filtered[:10])\n```",
            },
            {
                "content": "```python\nidx = context.find('auth')\nif idx == -1:\n    idx = context.find('Auth')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('Auth')\nif idx == -1:\n    idx = context.find('auth')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "The product specification supports three authentication methods: OAuth 2.0 with PKCE for third-party integrations, SAML 2.0 for enterprise SSO, and API key authentication for service-to-service communication. Multi-factor authentication is required for all user-facing login flows, supporting both TOTP and hardware security keys. Session tokens expire after 24 hours of inactivity.",
                "is_final": True,
            },
        ],
    },
    # Trace 8: NameError -- using variable from previous turn -- it_incident_report
    {
        "doc": "it_incident_report",
        "question": "What was the root cause of the incident?",
        "category": "error_runtime",
        "turns": [
            {
                "content": "```python\nidx = context.find('root cause')\nif idx == -1:\n    idx = context.find('Root Cause')\nresult = context[idx:idx+500]\n```",
            },
            {
                "content": "```python\nprint(result)\n```",
            },
            {
                "content": "```python\nidx = context.find('Root Cause')\nif idx == -1:\n    idx = context.find('root cause')\nresult = context[idx:idx+500]\nprint(result)\n```",
            },
            {
                "content": "The IT incident report identifies the root cause as an expired TLS certificate on the primary load balancer, which caused all HTTPS connections to fail starting at 2:47 AM. The certificate had been issued 12 months prior and the automated renewal process failed silently due to a misconfigured DNS record. The issue was resolved by manually installing a new certificate at 4:15 AM.",
                "is_final": True,
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Category 4: error_no_context_ref
# Assistant writes code that doesn't reference `context` at all.
# ---------------------------------------------------------------------------

NO_CONTEXT_REF_TRACES = [
    # Trace 1: Print statement only -- household_physician
    {
        "doc": "household_physician",
        "question": "What does the text say about treating fevers?",
        "category": "error_no_context_ref",
        "turns": [
            {
                "content": "```python\nprint('Searching for information about fevers...')\n```",
                "error_type": "no_context_ref",
            },
            {
                "content": "```python\nidx = context.find('fever')\nif idx == -1:\n    idx = context.find('Fever')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('Fever')\nif idx == -1:\n    idx = context.find('fever')\nprint(context[idx:idx+600])\n```",
            },
            {
                "content": "The text recommends several approaches for treating fevers: keeping the patient in bed with light coverings, providing plenty of cool water to drink, and sponging the body with tepid water to reduce temperature. It cautions against over-medicating and advises that a moderate fever is the body's natural defense mechanism. Severe or prolonged fevers warrant calling a physician.",
                "is_final": True,
            },
        ],
    },
    # Trace 2: Hardcoded sample data -- meeting_minutes
    {
        "doc": "meeting_minutes",
        "question": "Who attended the meeting?",
        "category": "error_no_context_ref",
        "turns": [
            {
                "content": "```python\ndata = 'sample meeting minutes text'\nprint(data.find('attendees'))\n```",
                "error_type": "no_context_ref",
            },
            {
                "content": "```python\nidx = context.find('attendees')\nif idx == -1:\n    idx = context.find('Attendees')\nif idx == -1:\n    idx = context.find('Present')\nprint(idx)\n```",
            },
            {
                "content": "```python\nfor term in ['Attendees', 'Present', 'Attendance', 'Members']:\n    idx = context.find(term)\n    if idx != -1:\n        print(context[idx:idx+400])\n        break\n```",
            },
            {
                "content": "According to the meeting minutes, the following people attended: Sarah Chen (Project Manager), Mike Williams (Engineering Lead), Lisa Park (QA Director), James Rodriguez (Product Owner), and David Kim (UX Designer). Two members were absent: Tom Anderson (DevOps) and Rachel Green (Marketing).",
                "is_final": True,
            },
        ],
    },
    # Trace 3: os.listdir() -- safety_data_sheet
    {
        "doc": "safety_data_sheet",
        "question": "What personal protective equipment is required when handling this chemical?",
        "category": "error_no_context_ref",
        "turns": [
            {
                "content": "```python\nimport os\nfiles = os.listdir('.')\nprint(files)\n```",
                "error_type": "no_context_ref",
            },
            {
                "content": "```python\nidx = context.find('protective')\nif idx == -1:\n    idx = context.find('PPE')\nprint(idx)\n```",
            },
            {
                "content": "```python\nfor term in ['PPE', 'Protective', 'protective equipment', 'Personal Protection']:\n    idx = context.find(term)\n    if idx != -1:\n        print(f'Found at {idx}:')\n        print(context[idx:idx+500])\n        break\n```",
            },
            {
                "content": "The safety data sheet requires the following PPE when handling this chemical: chemical-resistant gloves (nitrile recommended), safety goggles or a full face shield, a laboratory coat or chemical-resistant apron, and closed-toe shoes. In cases of potential vapor exposure, a NIOSH-approved respirator with organic vapor cartridges is required. All PPE should be inspected before use and properly decontaminated afterward.",
                "is_final": True,
            },
        ],
    },
    # Trace 4: Web request -- grant_proposal
    {
        "doc": "grant_proposal",
        "question": "What is the proposed research methodology?",
        "category": "error_no_context_ref",
        "turns": [
            {
                "content": "```python\nimport urllib.request\nresponse = urllib.request.urlopen('http://example.com/grant.txt')\nprint(response.read())\n```",
                "error_type": "no_context_ref",
            },
            {
                "content": "```python\nidx = context.find('methodology')\nif idx == -1:\n    idx = context.find('Methodology')\nif idx == -1:\n    idx = context.find('Methods')\nprint(idx)\n```",
            },
            {
                "content": "```python\nfor term in ['Methodology', 'methodology', 'Methods', 'Research Design']:\n    idx = context.find(term)\n    if idx != -1:\n        print(context[idx:idx+700])\n        break\n```",
            },
            {
                "content": "The grant proposal outlines a mixed-methods research methodology combining quantitative computational modeling with qualitative field interviews. Phase 1 involves building a simulation model using historical data. Phase 2 conducts semi-structured interviews with 40 participants across four sites. Phase 3 triangulates both data sources. The proposal cites validated instruments for each measurement and includes a detailed timeline spanning 36 months.",
                "is_final": True,
            },
        ],
    },
    # Trace 5: Random computation -- lab_report
    {
        "doc": "lab_report",
        "question": "What concentrations were measured in the samples?",
        "category": "error_no_context_ref",
        "turns": [
            {
                "content": "```python\nsamples = [1.2, 3.4, 5.6, 7.8]\navg = sum(samples) / len(samples)\nprint(f'Average: {avg}')\n```",
                "error_type": "no_context_ref",
            },
            {
                "content": "```python\nidx = context.find('concentration')\nif idx == -1:\n    idx = context.find('Concentration')\nprint(idx)\n```",
            },
            {
                "content": "```python\nidx = context.find('concentration')\nif idx == -1:\n    idx = context.find('Concentration')\nprint(context[idx:idx+500])\n```",
            },
            {
                "content": "The lab report documents the following measured concentrations: Sample 1 had 0.45 mg/L, Sample 2 had 0.62 mg/L, Sample 3 had 0.38 mg/L, and the control sample measured 0.02 mg/L. All samples exceeded the detection limit of 0.01 mg/L. Samples 1 and 2 were above the regulatory threshold of 0.50 mg/L and were flagged for additional analysis.",
                "is_final": True,
            },
        ],
    },
]
