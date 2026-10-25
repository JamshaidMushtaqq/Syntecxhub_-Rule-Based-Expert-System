# Rule-Based Expert System (Forward Chaining)

A small rule-based expert system in Python. The user enters facts (symptoms), and the engine uses forward chaining over a base of IF-THEN rules to infer conclusions. Every inference step is logged so the user can see exactly how each conclusion was reached.

> **Disclaimer:** This is an educational project. It is not a real medical diagnosis tool.

## Features

- Knowledge base of IF-THEN rules (conditions combined with AND)
- Fact base that holds user-supplied facts and newly inferred facts
- Forward chaining inference engine
- Multi-step (chained) reasoning: the conclusion of one rule can be the condition of another
- Full inference log showing every rule that fired
- "Why?" explanation: each conclusion is traced back to the original symptoms as a reasoning tree
- Interactive command-line mode and a built-in demo mode

## Key Concepts

- **Fact:** a statement known to be true, e.g. `fever`.
- **Rule:** `IF condition1 AND condition2 THEN conclusion`.
- **Forward chaining:** start from known facts, fire every rule whose conditions are all satisfied, add the new conclusions to the fact base, and repeat until no new facts can be derived.
- **Chaining:** `cough + sore_throat -> respiratory_infection`, then `respiratory_infection + viral_infection -> flu`, then `flu -> advice_rest_and_fluids`.

## How the Engine Works

1. Load the user's symptoms into the fact base.
2. Go through all rules. If all conditions of a rule are in the fact base and its conclusion is new, fire the rule: add the conclusion and record which rule produced it.
3. Repeat until a full pass fires no new rules.
4. Print the inference log, the final conclusions, and the reasoning path for each one.

## Rule Levels

| Level | Purpose | Example |
|-------|---------|---------|
| 1 | Symptoms to intermediate findings | `fever AND body_ache -> viral_infection` |
| 2 | Findings to diagnosis | `viral_infection AND respiratory_infection -> flu` |
| 3 | Diagnosis to advice | `flu AND high_fever -> advice_see_doctor` |

Run the program and type `rules` to list all rules.

## Requirements

- Python 3.8 or higher
- No external libraries

## Usage

Interactive mode:

```
python expert_system.py
```

Enter symptoms separated by commas, for example:

```
Enter symptoms (comma separated): fever, body ache, cough, sore throat
```

Demo mode (runs three built-in cases):

```
python expert_system.py --demo
```

Supported symptoms: `fever, high_fever, body_ache, cough, sore_throat, runny_nose, sneezing, itchy_eyes, headache, nausea, light_sensitivity, loss_of_taste, shortness_of_breath`

## Sample Output

Input: `fever, high_fever, body_ache, cough, sore_throat`

```
================ INFERENCE LOG ================
Initial facts: body_ache, cough, fever, high_fever, sore_throat
--- Pass 1 ---
Rule R1 fired: body_ache AND fever => viral_infection
Rule R2 fired: cough AND sore_throat => respiratory_infection
Rule R8 fired: respiratory_infection AND viral_infection => flu
Rule R11 fired: flu => advice_rest_and_fluids
Rule R12 fired: flu AND high_fever => advice_see_doctor
--- Pass 2 ---
No new rules can fire. Inference complete.

================ RESULT ================
Inferred findings: flu, respiratory infection, viral infection
Advice: rest and fluids, see doctor

================ WHY? (reasoning path) ================
Conclusion: flu
- flu  (by R8)
    - respiratory_infection  (by R2)
        - cough  (given by user)
        - sore_throat  (given by user)
    - viral_infection  (by R1)
        - body_ache  (given by user)
        - fever  (given by user)
```

## Adding Your Own Rules

Edit `build_rules()` in `expert_system.py`:

```python
make_rule("R18", ["fever", "rash"], "measles_suspected"),
```

Then add any new symptom names to `KNOWN_SYMPTOMS`.

## Project Structure

```
.
├── expert_system.py          # Rules, fact base, forward chaining engine, CLI
└── README_expert_system.md   # Documentation
```

## Possible Improvements

- Backward chaining mode
- OR conditions and negation (NOT)
- Certainty factors (confidence scores for each rule)
- Loading rules from a JSON or text file
- A simple GUI or web interface
