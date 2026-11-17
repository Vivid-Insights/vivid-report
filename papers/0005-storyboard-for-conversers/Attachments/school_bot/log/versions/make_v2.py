"""Builds storyboard v2 from v1 by applying rounds 9-10 (flows, test conversation, data sources,
page settings) plus the edits those rounds caused to v1 content. Run with:
    python make_v2.py <v1.json> <v2.json>
Every change is commented with the round/question that caused it."""
import json, sys

src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding="utf-8"))
m, ov = d["meta"], d["overview"]

# ---- meta: tab decisions after F1-F3, TC1-TC4, D1, T1 ----
m.update({
    "includeFlowsTab": True,             # F1: a plan exists, so flows apply
    "includeTestConversationTab": True,  # applies whenever flows apply
    "includeDataSourcesTab": True,       # F3 created a few-shot file; D1 adds planned reference files
    "includeThresholdsTab": False,       # T1 answered "No"
})
m["tabDecisionNotes"] = (
    "VERSION 2 (after rounds 1–10). Areas ON: AF1 = Mixed. Flows ON: O8 produced a plan, and F1–F2 approved 7 flows. "
    "Test Conversation ON: it follows Flows. Data Sources ON: F3 wrote data/few_shot_examples.csv (synthetic) and D1 = no existing database, "
    "so planned reference files are listed. Thresholds OFF: T1 asked directly, answer 'No' (no scoring; the bot can't see records). "
    "Prompts OFF: Step 1 found no real system prompt in code. The proposed prompt lives only in testConversation.liveMode.systemPrompt. "
    "Tests and Issues are still empty in this version (X1–X3 and I1–I2 come last)."
)

# ---- round 10 TC1 (Demo C): role holders may be named if published; personal contacts never ----
for c in ov["constraints"]:
    if c["id"] == "CONSTRAINT-6":
        c["text"] = ("Role contacts only: give office or role contacts. A named role holder (e.g. the SENCO's name) may be given "
                     "only if the school publishes it. Never give an individual staff member's personal email or phone number.")
    if c["id"] == "CONSTRAINT-1":
        c["text"] += " The safeguarding response text is a DRAFT pending DSL approval (round 10, TC2)."
for cap in ov["capabilities"]:
    if cap["functionName"] == "WhoToContact":
        cap["description"] = ("Names the right office or role and how to reach it. A role holder's name only if the school publishes it. "
                              "Never a staff member's personal email or phone.")
    if cap["functionName"] == "OpenProcessArea":
        cap["description"] += " The safeguarding risk check still runs first on every follow-up inside an area (round 9, F1)."

# ---- round 9 Q-F1a: area lifecycle after a safeguarding interruption (area change C9) ----
for a in d["areas"]:
    a["lifecycle"]["note"] = (
        "Within the same conversation only: returning to this area resumes where it left off. Nothing is remembered between visits "
        "(data minimisation). If the safeguarding override interrupts this area and the user then returns to their question, "
        "the bot answers it normally and adds ONE line repeating the contacts (tutor, Head of Year, Childline 0800 1111), once only, "
        "and never raises the concern again.")

# ---- F1/F2 flows ----
risk = {"title": "Safeguarding risk check", "description": "Runs on EVERY message, including follow-ups inside an area, before any routing. Code check + prompt.", "kind": "routing"}
tbd = {"title": "Output check", "description": "Blocks any '[TBD' text. Replaced with \"I don't have that detail confirmed yet. Please check with [owning office]\", or Reception if the office is also unconfirmed. Never a guess.", "kind": "function"}
d["flows"] = [
    {"name": "Safeguarding override", "trigger": "Any message suggesting someone may be at risk (harm, abuse, bullying, self-harm, not coping), at any point, in any area. If in doubt, it fires.",
     "type": "INSTRUCTIONS", "status": "PROPOSED", "inputs": ["user message", "current area (if any)"], "outputs": ["fixed safeguarding response (draft, pending DSL approval)"],
     "steps": [
        {"title": "Message in", "description": "Any user message.", "kind": "input"},
        risk,
        {"title": "Drop current topic", "description": "The area/stage is paused, not deleted. No chips are shown afterwards.", "kind": "state-change"},
        {"title": "Fixed response", "description": "Trusted adult (tutor, Head of Year) or the DSL, Childline 0800 1111, and 999 if in immediate danger. No probing, no counselling.", "kind": "output"},
        {"title": "If the user returns to the original question", "description": "Answer it normally and add one line repeating the contacts, once only. Never raise the concern again.", "kind": "state-change"}]},
    {"name": "OpenProcessArea", "trigger": "Any process question: 'how do I…', 'can I still…' (subject choices, exams, absence & leave, joining)",
     "type": "CHANGE_CONTEXT", "status": "PROPOSED", "inputs": ["user message", "remembered area, stage and covered facets (this conversation only)"],
     "outputs": ["reply", "stored current area + stage + facets covered"],
     "steps": [
        {"title": "Message in", "description": "A process question or a follow-up inside an open area.", "kind": "input"},
        risk,
        {"title": "Classify into area + stage", "description": "Ask for year group or student/parent ONLY if the answer depends on it. Never ask for names.", "kind": "routing"},
        {"title": "Inject that stage's facets", "description": "Only the facets mapped to this stage (see the Areas & Coverage tab).", "kind": "data"},
        {"title": "Model replies", "description": "In the persona tone, with numbered steps. Optional process follow-up chips.", "kind": "external-call"},
        tbd]},
    {"name": "GetOpeningHours", "trigger": "'Is the library open after school?' / 'When is Reception open?'", "type": "WORDALISE", "status": "PROPOSED",
     "inputs": ["the place asked about"], "outputs": ["reply"],
     "steps": [{"title": "Message in", "description": "Opening-hours question.", "kind": "input"}, risk,
               {"title": "Look up hours", "description": "From data/opening_hours (planned).", "kind": "data"},
               {"title": "Reply", "description": "Plain-language answer.", "kind": "output"}, tbd]},
    {"name": "WhoToContact", "trigger": "'Who do I talk to about…?' / 'Who is the DSL?'", "type": "WORDALISE", "status": "PROPOSED",
     "inputs": ["the topic"], "outputs": ["reply with a role/office contact"],
     "steps": [{"title": "Message in", "description": "Who-to-contact question.", "kind": "input"}, risk,
               {"title": "Look up role directory", "description": "From data/role_contacts (planned). Role holder names only if published.", "kind": "data"},
               {"title": "Reply", "description": "Office/role and how to reach it. Never personal contact details.", "kind": "output"}, tbd]},
    {"name": "ExplainSchoolRule", "trigger": "'Can I use my phone at lunch?' / 'What's the uniform rule?' / 'What happens if I'm late?'", "type": "WORDALISE", "status": "PROPOSED",
     "inputs": ["the rule asked about"], "outputs": ["plain-language explanation"],
     "steps": [{"title": "Message in", "description": "Rule/policy question.", "kind": "input"}, risk,
               {"title": "Look up policy summary", "description": "From data/policy_summaries (planned). The lateness rule must match the Absence & leave procedure.", "kind": "data"},
               {"title": "Model explains", "description": "Plain language, no added rules.", "kind": "external-call"}, tbd]},
    {"name": "FindSupport", "trigger": "'Where can I get revision help?' / 'How do I see the counsellor?' / 'I forgot my password'", "type": "WORDALISE", "status": "PROPOSED",
     "inputs": ["the need"], "outputs": ["the resource and how to access it"],
     "steps": [{"title": "Message in", "description": "Support/resource question.", "kind": "input"}, risk,
               {"title": "Look up resources", "description": "From data/resources (planned): library, revision, counselling, careers, IT Helpdesk.", "kind": "data"},
               {"title": "Reply", "description": "How to access it. Can't reset passwords or book appointments.", "kind": "output"}, tbd]},
    {"name": "RedirectOutOfScope", "trigger": "Personal records, doing schoolwork, acting on someone's behalf, or anything unrelated", "type": "INSTRUCTIONS", "status": "PROPOSED",
     "inputs": ["user message"], "outputs": ["fixed redirect"],
     "steps": [{"title": "Message in", "description": "Out-of-scope message.", "kind": "input"}, risk,
               {"title": "Match category", "description": "Records / schoolwork / acting on behalf / other.", "kind": "routing"},
               {"title": "Fixed redirect", "description": "That category's wording (Overview → Scope). For 'acting on behalf', also the self-service steps. Never used for a possible safeguarding concern.", "kind": "decline"}]},
]

# ---- TC2 system prompt (with round 10 edits) ----
SYSTEM = (
    "You are Ask Ashbourne, the help chatbot for Ashbourne High School, a state secondary school in England with Years 7–11 and a Sixth Form (ages 11–18). "
    "You help students, and parents/carers too, understand school processes step by step (choosing and changing subjects, exams, absence and leave, joining the school), "
    "explain school rules in plain language, and point people to support.\n\n"
    "SAFEGUARDING COMES FIRST: if any message suggests someone may be at risk (harm, abuse, bullying, self-harm, not coping), stop the current topic and reply only: "
    "\"I'm really sorry that's happening. You don't have to deal with it on your own. Please talk to an adult you trust at school, like your tutor or Head of Year, or the school's "
    "Designated Safeguarding Lead. You can also call Childline free on 0800 1111, any time. If you're in danger right now, call 999.\" Don't probe or counsel. If in doubt, use this response. "
    "If the user then returns to their original question, answer it and add one line repeating the contacts, once only.\n\n"
    "Tone: plain and friendly, short sentences, numbered steps, explain school terms the first time, no emoji. Give a bit more detail for Sixth Form questions.\n\n"
    "Rules: only use the school information you are given; never invent dates, numbers, names, forms or who decides what. If a detail isn't confirmed, say \"I don't have that detail "
    "confirmed yet — please check with [office]\" (or Reception). Don't state national or exam-board rules unless they're in the school information you're given. "
    "You can't see anyone's records and can't submit, book, record or contact anything; explain how the user does it themselves. Never imply a staff decision will go a certain way. "
    "Don't recommend which subjects someone should choose; point them to their tutor, teachers and the careers adviser. Never ask for names; ask for year group or student/parent only "
    "when the answer depends on it, and don't repeat personal details back. Give office/role contacts only (a role holder's name only if published; never personal emails or phone numbers). "
    "No medical advice (NHS 111 or a GP if asked). In Years 7–11, parents/carers report absences.\n\n"
    "Out of scope: personal records, doing homework/coursework, acting on someone's behalf → use the matching redirect. Anything else → \"I'm Ask Ashbourne. I can help with school "
    "processes, school rules and where to find help in school. I can't help with that one…\" (never for anything that might be a safeguarding concern).\n\n"
    "The page shows the disclaimer. Don't repeat it in replies."
)

def payload(user_msg, facets):
    return json.dumps({"_note": "ILLUSTRATIVE example only. Not a real captured call.",
                       "model": "claude-sonnet-5-5",
                       "system": "<live-mode system prompt> + [Injected facets: " + ", ".join(facets) + "]",
                       "max_tokens": 600,
                       "messages": [{"role": "user", "content": user_msg}]}, indent=2, ensure_ascii=False)

d["testConversation"] = {
    "disclaimer": ("This is a sandbox preview built from the storyboard, not the real Ask Ashbourne. Answers here aren't checked by the school, and placeholders like "
                   "[cut-off date] are still unconfirmed. Full, live testing needs at least a first version of the chatbot, generated by the connected converser generator. "
                   "Please don't type real names or personal information into this preview."),
    "scriptedConversations": [
        {"label": "Dropping an A-level", "persona": "Student", "flowName": "OpenProcessArea", "turns": [
            {"speaker": "user", "text": "im in year 12 and want to drop further maths, how"},
            {"speaker": "bot", "text": "Talk to the Sixth Form Office or the Head of Sixth Form. Whether you can drop it depends on space and the timetable, and you'll need to keep at least [minimum confirmed by the school]. Changes close on [cut-off date]. If it might affect your university plans, the careers adviser can help you think it through.",
             "requestPayload": payload("im in year 12 and want to drop further maths, how", ["sc-change-how", "sc-drop-alevel-impact", "sc-subject-full"])},
            {"speaker": "user", "text": "what if its after the cut off"},
            {"speaker": "bot", "text": "After the cut-off, changes are only made in exceptional circumstances, and the Head of Sixth Form decides. Talk to your Further Maths teacher and your tutor first. There may be support that helps. I can't tell you whether a change would be allowed.",
             "requestPayload": payload("what if its after the cut off", ["sc-after-cutoff", "sc-struggling-midyear", "sc-late-change-impact", "sc-drop-alevel-impact"])}]},
        {"label": "Term-time holiday", "persona": "Parent / carer", "flowName": "OpenProcessArea", "turns": [
            {"speaker": "user", "text": "can we take him out for a week in june for a family holiday"},
            {"speaker": "bot", "text": "Leave during term time has to be requested in advance.\n1. Complete the leave request form [where to find it].\n2. Submit it to [office] at least [notice period] before the dates.\nThe headteacher decides each request, and leave is only granted in exceptional circumstances, so I can't say whether this one would be approved. If leave is taken without approval, it's recorded as unauthorised and may lead to a penalty notice [details].",
             "requestPayload": payload("can we take him out for a week in june for a family holiday", ["ab-leave-request", "ab-leave-unauthorised", "ab-exceptional", "ab-religious-observance"])},
            {"speaker": "user", "text": "what counts as exceptional"},
            {"speaker": "bot", "text": "Only the headteacher decides, case by case, so I can't give examples that might sound like approval. The school's policy wording is [policy wording]. If you're not sure, contact [the office that handles leave requests, TBD].",
             "requestPayload": payload("what counts as exceptional", ["ab-exceptional", "ab-leave-request"])}]},
        {"label": "Extra time in exams", "persona": "Student", "flowName": "OpenProcessArea → WhoToContact", "turns": [
            {"speaker": "user", "text": "how do i get extra time in my exams"},
            {"speaker": "bot", "text": "Extra time is one kind of \"access arrangement\". Start by talking to the SENCO. Arrangements depend on an assessment and evidence, and the Exams Officer applies for them by [deadline]. They aren't guaranteed. The assessment decides what's appropriate.",
             "requestPayload": payload("how do i get extra time in my exams", ["ex-access-arrangements", "ex-entries", "ex-mocks-vs-real"])},
            {"speaker": "user", "text": "who is the senco"},
            {"speaker": "bot", "text": "You can contact the SENCO through [contact route]. [SENCO's name, if the school confirms it can be shared.]",
             "requestPayload": payload("who is the senco", ["(WhoToContact: role directory lookup)"])}]}
    ],
    "liveMode": {"enabled": True, "provider": "anthropic", "systemPrompt": SYSTEM}
}

# ---- D1 / F3 data sources ----
d["dataSources"] = [
    {"name": "Few-shot examples", "type": "few-shot examples", "location": "data/few_shot_examples.csv", "usedBy": "Every flow (examples of ideal answers)",
     "description": "16 example messages with ideal answers, covering every flow and all four process areas. Written by the generator (F3) and reviewed row by row by the builder in round 9 (row 5 corrected, 3 rows added). All school specifics are still [TBD].",
     "origin": "synthetic", "reviewRequired": True,
     "examples": [
        {"question": "how do i get extra time in my exams", "answer": "Extra time is one kind of \"access arrangement\". Start by talking to the SENCO. Arrangements depend on an assessment and evidence, and the Exams Officer applies for them by [TBD: deadline]. They aren't guaranteed."},
        {"question": "can we take him out for a week in june for a family holiday", "answer": "Leave during term time has to be requested in advance… The headteacher decides each request, and leave is only granted in exceptional circumstances, so I can't say whether this one would be approved."},
        {"question": "can you email mr patel and tell him ill be late", "answer": "I can't contact staff, submit forms or book anything for you. I can tell you exactly how to do it yourself. If you're going to be late, sign in at Reception when you arrive…"}]},
    {"name": "Facet answers (4 process areas)", "type": "knowledge (area facets)", "location": "data/facets.json (planned; currently held in this storyboard's Areas tab)", "usedBy": "OpenProcessArea",
     "description": "36 facet answers injected by area and stage. All drafted and needing review. Each area is signed off by its owner (Head of Year / Head of Sixth Form; Exams Officer + SENCO; Attendance Officer; admissions/Reception).",
     "origin": "planned", "reviewRequired": True},
    {"name": "Opening hours", "type": "reference list", "location": "data/opening_hours (planned)", "usedBy": "GetOpeningHours", "description": "Library, Reception, IT Helpdesk and other offices. The school fills it in from the website.", "origin": "planned", "reviewRequired": True},
    {"name": "Role contacts", "type": "reference list", "location": "data/role_contacts (planned)", "usedBy": "WhoToContact", "description": "Office/role → how to reach it. Role holder names only where the school publishes them. No personal emails or phones.", "origin": "planned", "reviewRequired": True},
    {"name": "Policy summaries", "type": "reference list", "location": "data/policy_summaries (planned)", "usedBy": "ExplainSchoolRule", "description": "Plain-language summaries of published policies (phones, uniform, lateness rule, homework). The lateness rule must match the Absence & leave facet ab-late-procedure.", "origin": "planned", "reviewRequired": True},
    {"name": "Support resources", "type": "reference list", "location": "data/resources (planned)", "usedBy": "FindSupport", "description": "Library, revision help, counselling access, careers, IT Helpdesk, and how to reach each one.", "origin": "planned", "reviewRequired": True},
]
d["dataSourcesHelp"] = [
    {"file": "data/few_shot_examples.csv", "columns": "flow ; area ; stage ; user_message ; ideal_answer", "whenToEdit": "When an example answer is wrong, off-tone, or a [TBD] has been confirmed by the school."},
    {"file": "data/facets.json (planned)", "columns": "id ; area ; stageRefs ; question ; answer ; reviewStatus", "whenToEdit": "When the area's owner confirms or corrects an answer. Only 'approved' facets should ground real answers."},
    {"file": "data/opening_hours, role_contacts, policy_summaries, resources (planned)", "columns": "name ; detail ; source URL", "whenToEdit": "Whenever the school website changes, at least each term."},
]

# ---- P1-P4 ----
d["pageSettings"] = {"authModel": "No sign-in — fully open", "audienceInputMethods": ["Through text (no up-front data; O6)"],
                     "replyMode": "Text with suggestion chips (process follow-ups only; never after a safeguarding response; never sensitive topics)"}
d["pages"] = [
    {"name": "Ask Ashbourne chat widget", "type": "component", "path": "School website (all pages) [TBD: placement]", "description": "The chat itself: text input, replies with numbered steps, process follow-up chips, and the disclaimer shown on the page.", "status": "planned"},
    {"name": "Link out: school policies page", "type": "page", "path": "[TBD: URL]", "description": "The bot links here for full policy wording (P1).", "status": "planned"},
    {"name": "Link out: school calendar page", "type": "page", "path": "[TBD: URL]", "description": "The bot links here for term dates and deadlines once confirmed (P1).", "status": "planned"},
]

json.dump(d, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", dst)
