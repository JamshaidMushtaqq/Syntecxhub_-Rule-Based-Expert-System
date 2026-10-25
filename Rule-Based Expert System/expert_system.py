"""
Rule-Based Expert System (Forward Chaining)
-------------------------------------------
- Knowledge base: a set of IF-THEN rules
- Fact base: facts supplied by the user (symptoms) + facts inferred by the engine
- Inference: forward chaining (data-driven), repeated until no new fact can be derived
- Multi-step reasoning: a conclusion of one rule can be a condition of another
- Logging: every rule firing is recorded so the reasoning path can be displayed

NOTE: Educational demo only. It is NOT a real medical diagnosis tool.
"""

import sys
from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Optional, Set


# ---------------------------------------------------------------- Rule model
@dataclass(frozen=True)
class Rule:
    name: str
    conditions: FrozenSet[str]   # IF all of these facts are known...
    conclusion: str              # ...THEN this fact becomes known

    def __str__(self) -> str:
        conds = " AND ".join(sorted(self.conditions))
        return f"{self.name}: IF {conds} THEN {self.conclusion}"


def make_rule(name: str, conditions: List[str], conclusion: str) -> Rule:
    return Rule(name, frozenset(conditions), conclusion)


# ---------------------------------------------------------------- Knowledge base
def build_rules() -> List[Rule]:
    return [
        # Level 1: symptoms -> intermediate findings
        make_rule("R1", ["fever", "body_ache"], "viral_infection"),
        make_rule("R2", ["cough", "sore_throat"], "respiratory_infection"),
        make_rule("R3", ["runny_nose", "sneezing"], "cold_symptoms"),
        make_rule("R4", ["sneezing", "itchy_eyes"], "allergy_symptoms"),
        make_rule("R5", ["headache", "nausea", "light_sensitivity"], "migraine_suspected"),
        make_rule("R6", ["fever", "loss_of_taste"], "covid_suspected"),
        make_rule("R7", ["fever", "cough", "shortness_of_breath"], "pneumonia_suspected"),

        # Level 2: findings -> diagnosis
        make_rule("R8", ["viral_infection", "respiratory_infection"], "flu"),
        make_rule("R9", ["cold_symptoms"], "common_cold"),
        make_rule("R10", ["allergy_symptoms"], "allergy"),

        # Level 3: diagnosis -> advice
        make_rule("R11", ["flu"], "advice_rest_and_fluids"),
        make_rule("R12", ["flu", "high_fever"], "advice_see_doctor"),
        make_rule("R13", ["common_cold"], "advice_rest_and_warm_drinks"),
        make_rule("R14", ["allergy"], "advice_avoid_allergens"),
        make_rule("R15", ["migraine_suspected"], "advice_rest_in_dark_room"),
        make_rule("R16", ["covid_suspected"], "advice_test_and_isolate"),
        make_rule("R17", ["pneumonia_suspected"], "advice_see_doctor_urgently"),
    ]


KNOWN_SYMPTOMS = [
    "fever", "high_fever", "body_ache", "cough", "sore_throat", "runny_nose",
    "sneezing", "itchy_eyes", "headache", "nausea", "light_sensitivity",
    "loss_of_taste", "shortness_of_breath",
]


# ---------------------------------------------------------------- Inference engine
class ExpertSystem:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
        self.facts: Set[str] = set()
        self.initial_facts: Set[str] = set()
        self.derived_by: Dict[str, Rule] = {}   # fact -> rule that produced it
        self.log: List[str] = []

    def reset(self, initial_facts: Set[str]) -> None:
        self.initial_facts = set(initial_facts)
        self.facts = set(initial_facts)
        self.derived_by = {}
        self.log = []

    def forward_chain(self) -> Set[str]:
        """Fire rules repeatedly until no new facts can be inferred."""
        self.log.append(f"Initial facts: {', '.join(sorted(self.facts)) or '(none)'}")
        iteration = 0

        while True:
            iteration += 1
            fired_this_round = False
            self.log.append(f"--- Pass {iteration} ---")

            for rule in self.rules:
                if rule.conclusion in self.facts:
                    continue  # already known, rule adds nothing new
                if rule.conditions <= self.facts:  # all conditions satisfied
                    self.facts.add(rule.conclusion)
                    self.derived_by[rule.conclusion] = rule
                    fired_this_round = True
                    self.log.append(
                        f"Rule {rule.name} fired: "
                        f"{' AND '.join(sorted(rule.conditions))} => {rule.conclusion}"
                    )

            if not fired_this_round:
                self.log.append("No new rules can fire. Inference complete.")
                break

        return self.facts - self.initial_facts

    # ---- explanation: trace a conclusion back to the original symptoms
    def explain(self, fact: str, indent: int = 0) -> List[str]:
        pad = "    " * indent
        if fact in self.initial_facts:
            return [f"{pad}- {fact}  (given by user)"]
        rule = self.derived_by.get(fact)
        if rule is None:
            return [f"{pad}- {fact}  (unknown)"]
        lines = [f"{pad}- {fact}  (by {rule.name})"]
        for cond in sorted(rule.conditions):
            lines.extend(self.explain(cond, indent + 1))
        return lines


# ---------------------------------------------------------------- Presentation
def pretty(fact: str) -> str:
    return fact.replace("_", " ")


def run_consultation(system: ExpertSystem, symptoms: Set[str]) -> None:
    system.reset(symptoms)
    new_facts = system.forward_chain()

    print("\n================ INFERENCE LOG ================")
    for line in system.log:
        print(line)

    advice = sorted(f for f in new_facts if f.startswith("advice_"))
    findings = sorted(f for f in new_facts if not f.startswith("advice_"))

    print("\n================ RESULT ================")
    if not new_facts:
        print("No conclusions could be inferred from the given facts.")
        return

    print("Inferred findings:", ", ".join(pretty(f) for f in findings) or "none")
    print("Advice:", ", ".join(pretty(f.replace('advice_', '')) for f in advice) or "none")

    print("\n================ WHY? (reasoning path) ================")
    for f in findings + advice:
        print(f"\nConclusion: {pretty(f)}")
        print("\n".join(system.explain(f)))


def parse_input(text: str) -> Set[str]:
    return {t.strip().lower().replace(" ", "_") for t in text.split(",") if t.strip()}


def interactive(system: ExpertSystem) -> None:
    print("Rule-Based Expert System (educational demo, not medical advice)")
    print("Known symptoms:", ", ".join(KNOWN_SYMPTOMS))
    print("Type 'rules' to list rules, 'quit' to exit.\n")

    while True:
        text = input("Enter symptoms (comma separated): ").strip()
        if text.lower() in ("quit", "exit", "q"):
            break
        if text.lower() == "rules":
            for r in system.rules:
                print(" ", r)
            continue

        symptoms = parse_input(text)
        unknown = symptoms - set(KNOWN_SYMPTOMS)
        if unknown:
            print("Warning: unrecognized symptom(s):", ", ".join(sorted(unknown)))
        run_consultation(system, symptoms)
        print()


def demo(system: ExpertSystem) -> None:
    cases = [
        ("Multi-step: flu with high fever", {"fever", "high_fever", "body_ache", "cough", "sore_throat"}),
        ("Common cold", {"runny_nose", "sneezing"}),
        ("Not enough information", {"headache"}),
    ]
    for title, symptoms in cases:
        print(f"\n\n########## CASE: {title} ##########")
        print("Symptoms:", ", ".join(sorted(symptoms)))
        run_consultation(system, symptoms)


if __name__ == "__main__":
    engine = ExpertSystem(build_rules())
    if "--demo" in sys.argv:
        demo(engine)
    else:
        interactive(engine)
