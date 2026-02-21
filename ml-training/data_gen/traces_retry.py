"""
Training traces for keyword retry and dead-end search patterns.

Category 1 (keyword_retry): The model tries 1-3 keywords that return -1,
then finds a synonym that works, extracts text, and gives a FINAL answer.

Category 2 (dead_end): The model tries 5+ keywords that all return -1,
then gives a FINAL saying the information was not found.

IMPORTANT: Each code turn is executed independently via exec(). Variables
from previous turns are NOT preserved between turns.
"""

# ---------------------------------------------------------------------------
# Category 1: keyword_retry (20 traces)
# Pattern: First 1-3 keyword searches return -1, then a synonym works.
# ---------------------------------------------------------------------------

KEYWORD_RETRY_TRACES = [
    # --- Trace 1: cavalry_outpost - scouting/patrol ---
    {
        "doc": "cavalry_outpost",
        "question": "What does the text say about scouting procedures?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('scouting')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('reconnaissance')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('patrol')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('patrol')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The text discusses patrol duties extensively. It describes how patrols are sent out from the outpost line to observe the enemy and gather intelligence about their movements. Patrols should move cautiously, maintain communication with the main body, and report their observations promptly to the commanding officer.)", "is_final": True},
        ],
    },
    # --- Trace 2: boston_cooking_school - dessert/cake ---
    {
        "doc": "boston_cooking_school",
        "question": "Does the book contain instructions for making a chocolate dessert?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('mousse')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('ganache')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('chocolate')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('chocolate')\nprint(context[idx:idx+600])\n```"},
            {"content": "FINAL(Yes, the book contains instructions involving chocolate. The text includes recipes and references to chocolate as an ingredient, describing its use in various preparations.)", "is_final": True},
        ],
    },
    # --- Trace 3: household_physician - headaches ---
    {
        "doc": "household_physician",
        "question": "What remedies does the text suggest for headaches?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('migraine')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('headache')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('headache')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The text discusses headaches and suggests various remedies. It covers causes and treatments available in the era of the book's writing, including rest, dietary adjustments, and various preparations intended to relieve head pain.)", "is_final": True},
        ],
    },
    # --- Trace 4: rules_of_road_sea - collision avoidance ---
    {
        "doc": "rules_of_road_sea",
        "question": "What are the rules regarding collision avoidance?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('collision avoidance')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('radar')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('vessel')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('vessel')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The text describes rules for vessels at sea to prevent collisions. It specifies that every vessel shall proceed at a safe speed and outlines the actions to be taken when vessels are in sight of one another or in restricted visibility conditions.)", "is_final": True},
        ],
    },
    # --- Trace 5: cushings_manual - tabling a question ---
    {
        "doc": "cushings_manual",
        "question": "How does the text describe the procedure for tabling a question?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('tabling')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('postpone')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('table')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('table')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The text describes the motion to lay on the table as a means of temporarily setting aside a question. According to Cushing's Manual, a question may be laid on the table by a majority vote, and it can be taken up again when the assembly chooses to resume consideration of it.)", "is_final": True},
        ],
    },
    # --- Trace 6: product_spec - bluetooth ---
    {
        "doc": "product_spec",
        "question": "Does the thermostat support Bluetooth connectivity?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('Bluetooth')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('bluetooth')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('wifi')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('wifi')\nprint(context[idx:idx+400])\n```"},
            {"content": "FINAL(The document does not mention Bluetooth connectivity. However, it does reference wifi as the wireless connectivity method for the smart thermostat. Bluetooth does not appear to be a supported feature based on the spec sheet.)", "is_final": True},
        ],
    },
    # --- Trace 7: lease_agreement - subletting ---
    {
        "doc": "lease_agreement",
        "question": "What does the lease say about subletting the apartment?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('subletting')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('sublet')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('tenant')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('tenant')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The lease agreement addresses tenant obligations. While the specific term 'subletting' may not appear, the document covers tenant responsibilities and restrictions regarding the use and occupancy of the premises, which would govern any subletting arrangements.)", "is_final": True},
        ],
    },
    # --- Trace 8: lab_report - arsenic ---
    {
        "doc": "lab_report",
        "question": "Were arsenic levels tested in the water samples?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('arsenic')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('heavy metal')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('sample')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('sample')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The lab report discusses water quality samples and various measurements. While arsenic is not specifically mentioned by name, the report covers sample collection and analysis of water quality parameters.)", "is_final": True},
        ],
    },
    # --- Trace 9: meeting_minutes - CEO resignation ---
    {
        "doc": "meeting_minutes",
        "question": "Was a CEO resignation discussed at the board meeting?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('resignation')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('CEO')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('board')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('board')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The meeting minutes do not mention a CEO resignation. The board meeting covered other agenda items. The term 'resignation' does not appear in the document.)", "is_final": True},
        ],
    },
    # --- Trace 10: employee_handbook - remote work ---
    {
        "doc": "employee_handbook",
        "question": "What is the company's policy on remote work?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('remote work')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('telecommuting')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('policy')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('policy')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The employee handbook contains various workplace policies. While 'remote work' and 'telecommuting' are not specifically mentioned, the handbook covers general employment policies that may govern work arrangements.)", "is_final": True},
        ],
    },
    # --- Trace 11: safety_data_sheet - carcinogen ---
    {
        "doc": "safety_data_sheet",
        "question": "Is the chemical classified as a carcinogen?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('carcinogen')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('cancer')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('hazard')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('hazard')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The safety data sheet describes the hazard classification of the chemical. While the specific term 'carcinogen' was not found, the document details hazard information including health hazards and safety precautions associated with the chemical.)", "is_final": True},
        ],
    },
    # --- Trace 12: grant_proposal - machine learning ---
    {
        "doc": "grant_proposal",
        "question": "Does the grant proposal involve machine learning techniques?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('machine learning')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('neural network')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('research')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('research')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The grant proposal describes a research project. While 'machine learning' and 'neural network' are not mentioned explicitly, the proposal covers the research methodology and objectives of the funded project.)", "is_final": True},
        ],
    },
    # --- Trace 13: it_incident_report - ransomware ---
    {
        "doc": "it_incident_report",
        "question": "Was the incident caused by ransomware?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('ransomware')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('malware')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('database')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('database')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The IT incident report describes a database outage, not a ransomware attack. The incident was related to database issues rather than any form of malware or ransomware. The report details the database-related root cause and resolution steps.)", "is_final": True},
        ],
    },
    # --- Trace 14: cavalry_outpost - night operations ---
    {
        "doc": "cavalry_outpost",
        "question": "What does the text say about conducting operations at night?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('nocturnal')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('darkness')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('nightfall')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('night')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('night')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The text discusses night operations in the context of outpost duty. At night, picquets and sentries must be especially vigilant as the enemy is more likely to attempt an advance under cover of darkness. The distance between outpost positions should be reduced at night, and patrols should be sent out more frequently to guard against surprise attacks.)", "is_final": True},
        ],
    },
    # --- Trace 15: boston_cooking_school - vegan ---
    {
        "doc": "boston_cooking_school",
        "question": "Are there any vegan recipes in the cookbook?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('vegan')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('plant-based')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('vegetable')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('vegetable')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The cookbook does not use the term 'vegan' as this is a historical text predating that concept. However, it does contain sections on vegetables and their preparation. Many of these vegetable recipes may happen to be plant-based, though the book was not written with vegan cooking in mind.)", "is_final": True},
        ],
    },
    # --- Trace 16: household_physician - vaccination ---
    {
        "doc": "household_physician",
        "question": "What does the text say about vaccination?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('immunization')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('vaccine')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('disease')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('disease')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The text covers various diseases and their treatments. While modern vaccination terminology may not appear, the text discusses disease prevention and treatment methods available in the era of its publication.)", "is_final": True},
        ],
    },
    # --- Trace 17: gpo_manual - emoji usage ---
    {
        "doc": "gpo_manual",
        "question": "Does the GPO manual address the use of emojis in publications?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('emoji')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('symbol')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('symbol')\nprint(context[idx:idx+400])\n```"},
            {"content": "FINAL(The GPO manual does not address emojis, as it predates their common usage in publications. However, the manual does discuss the use of symbols and special characters in government publications, covering their proper formatting and placement.)", "is_final": True},
        ],
    },
    # --- Trace 18: rules_of_road_sea - submarine ---
    {
        "doc": "rules_of_road_sea",
        "question": "Are there specific rules for submarines?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('submarine')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('underwater')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('light')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('light')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The rules of the road at sea do not specifically mention submarines. The text primarily addresses surface vessels and their obligations regarding lights, signals, and right-of-way. The rules cover various types of vessels including steam vessels, sailing vessels, and vessels engaged in fishing, but submarines are not called out separately.)", "is_final": True},
        ],
    },
    # --- Trace 19: cushings_manual - secret ballot ---
    {
        "doc": "cushings_manual",
        "question": "Does the text describe the use of a secret ballot?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('secret ballot')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('ballot')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('vote')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('vote')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The text does not use the exact phrase 'secret ballot' but describes voting procedures in detail. Cushing's Manual covers voice votes, division of the assembly, and ballot votes. The ballot method involves members writing their choices on paper, which are then collected and counted by tellers appointed by the presiding officer.)", "is_final": True},
        ],
    },
    # --- Trace 20: lease_agreement - pet policy ---
    {
        "doc": "lease_agreement",
        "question": "Does the lease allow pets?",
        "category": "keyword_retry",
        "turns": [
            {"content": "```python\nidx = context.find('pet')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('animal')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('premises')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('premises')\nprint(context[idx:idx+500])\n```"},
            {"content": "FINAL(The lease agreement covers the terms of occupancy for the premises. While 'pet' and 'animal' were not found as specific terms, the lease describes general tenant obligations regarding the use and condition of the premises. Any pet policy would fall under these general provisions or would need to be addressed in a separate addendum.)", "is_final": True},
        ],
    },
]

# ---------------------------------------------------------------------------
# Category 2: dead_end (10 traces)
# Pattern: 5+ keyword searches all return -1, then FINAL says not found.
# ---------------------------------------------------------------------------

DEAD_END_TRACES = [
    # --- Trace 1: cavalry_outpost - submarine warfare ---
    {
        "doc": "cavalry_outpost",
        "question": "What does the text say about submarine warfare tactics?",
        "category": "dead_end",
        "turns": [
            {"content": "```python\nidx = context.find('submarine')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('torpedo')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('naval')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('ship')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('sea')\nprint(f'Found at: {idx}')\n```"},
            {"content": "FINAL(The document does not contain information about submarine warfare. After searching for 'submarine', 'torpedo', 'naval', 'ship', and 'sea', none were found in the text. This is a manual on cavalry outpost duties, focused entirely on land-based military operations involving mounted troops and sentries.)", "is_final": True},
        ],
    },
    # --- Trace 2: boston_cooking_school - microwave ---
    {
        "doc": "boston_cooking_school",
        "question": "Does the cookbook have microwave cooking instructions?",
        "category": "dead_end",
        "turns": [
            {"content": "```python\nidx = context.find('microwave')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('watt')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('defrost')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('reheat')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('microwave oven')\nprint(f'Found at: {idx}')\n```"},
            {"content": "FINAL(The document does not contain information about microwave cooking. After searching for 'microwave', 'watt', 'defrost', 'reheat', and 'microwave oven', none were found in the text. This is a historical cookbook from the early 1900s, well before microwave ovens were invented.)", "is_final": True},
        ],
    },
    # --- Trace 3: rules_of_road_sea - aircraft ---
    {
        "doc": "rules_of_road_sea",
        "question": "What rules apply to aircraft landing on water?",
        "category": "dead_end",
        "turns": [
            {"content": "```python\nidx = context.find('aircraft')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('airplane')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('seaplane')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('aviation')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('landing')\nprint(f'Found at: {idx}')\n```"},
            {"content": "FINAL(The document does not contain information about aircraft landing on water. After searching for 'aircraft', 'airplane', 'seaplane', 'aviation', and 'landing', none were found in the text. The rules of the road at sea pertain to maritime vessels and do not cover aircraft operations.)", "is_final": True},
        ],
    },
    # --- Trace 4: household_physician - gene therapy ---
    {
        "doc": "household_physician",
        "question": "What does the text say about gene therapy treatments?",
        "category": "dead_end",
        "turns": [
            {"content": "```python\nidx = context.find('gene therapy')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('genetic')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('DNA')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('genome')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('chromosome')\nprint(f'Found at: {idx}')\n```"},
            {"content": "FINAL(The document does not contain information about gene therapy. After searching for 'gene therapy', 'genetic', 'DNA', 'genome', and 'chromosome', none were found in the text. This is a historical medical reference that predates the discovery of DNA's structure and modern genetic medicine.)", "is_final": True},
        ],
    },
    # --- Trace 5: cushings_manual - video conferencing ---
    {
        "doc": "cushings_manual",
        "question": "How does the text address video conferencing during meetings?",
        "category": "dead_end",
        "turns": [
            {"content": "```python\nidx = context.find('video conferencing')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('internet')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('online')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('telephone')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('remote')\nprint(f'Found at: {idx}')\n```"},
            {"content": "FINAL(The document does not contain information about video conferencing. After searching for 'video conferencing', 'internet', 'online', 'telephone', and 'remote', none were found in the text. Cushing's Manual of Parliamentary Practice was written in 1887, long before modern communication technology, and addresses only in-person deliberative assemblies.)", "is_final": True},
        ],
    },
    # --- Trace 6: product_spec - solar power ---
    {
        "doc": "product_spec",
        "question": "Can the thermostat be powered by solar panels?",
        "category": "dead_end",
        "turns": [
            {"content": "```python\nidx = context.find('solar')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('photovoltaic')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('renewable')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('panel')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('solar power')\nprint(f'Found at: {idx}')\n```"},
            {"content": "FINAL(The document does not contain information about solar power compatibility. After searching for 'solar', 'photovoltaic', 'renewable', 'panel', and 'solar power', none were found in the spec sheet. The thermostat specification does not mention solar panel integration as a power source.)", "is_final": True},
        ],
    },
    # --- Trace 7: lab_report - radioactivity ---
    {
        "doc": "lab_report",
        "question": "Were radioactivity levels measured in the water samples?",
        "category": "dead_end",
        "turns": [
            {"content": "```python\nidx = context.find('radioactivity')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('radiation')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('uranium')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('radon')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('becquerel')\nprint(f'Found at: {idx}')\n```"},
            {"content": "FINAL(The document does not contain information about radioactivity measurements. After searching for 'radioactivity', 'radiation', 'uranium', 'radon', and 'becquerel', none were found in the lab report. The water quality analysis does not include radiological testing.)", "is_final": True},
        ],
    },
    # --- Trace 8: meeting_minutes - cryptocurrency ---
    {
        "doc": "meeting_minutes",
        "question": "Did the board discuss investing in cryptocurrency?",
        "category": "dead_end",
        "turns": [
            {"content": "```python\nidx = context.find('cryptocurrency')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('bitcoin')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('crypto')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('blockchain')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('digital currency')\nprint(f'Found at: {idx}')\n```"},
            {"content": "FINAL(The document does not contain information about cryptocurrency investment. After searching for 'cryptocurrency', 'bitcoin', 'crypto', 'blockchain', and 'digital currency', none were found in the meeting minutes. The board meeting did not discuss cryptocurrency-related topics.)", "is_final": True},
        ],
    },
    # --- Trace 9: employee_handbook - stock options ---
    {
        "doc": "employee_handbook",
        "question": "What does the handbook say about stock option vesting?",
        "category": "dead_end",
        "turns": [
            {"content": "```python\nidx = context.find('stock option')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('vesting')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('equity')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('shares')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('RSU')\nprint(f'Found at: {idx}')\n```"},
            {"content": "FINAL(The document does not contain information about stock option vesting. After searching for 'stock option', 'vesting', 'equity', 'shares', and 'RSU', none were found in the employee handbook. The handbook does not appear to cover equity compensation.)", "is_final": True},
        ],
    },
    # --- Trace 10: it_incident_report - phishing ---
    {
        "doc": "it_incident_report",
        "question": "Was phishing identified as the attack vector?",
        "category": "dead_end",
        "turns": [
            {"content": "```python\nidx = context.find('phishing')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('email attack')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('social engineering')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('malicious link')\nprint(f'Found at: {idx}')\n```"},
            {"content": "```python\nidx = context.find('spoofing')\nprint(f'Found at: {idx}')\n```"},
            {"content": "FINAL(The document does not contain information about phishing. After searching for 'phishing', 'email attack', 'social engineering', 'malicious link', and 'spoofing', none were found in the IT incident report. The report describes a database outage, not a phishing-related security incident.)", "is_final": True},
        ],
    },
]
