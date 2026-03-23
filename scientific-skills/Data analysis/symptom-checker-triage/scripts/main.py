#!/usr/bin/env python3
"""Symptom Checker Triage (ID: 165)
Recommended triage level (emergency vs outpatient) based on red flags of common symptoms"""

import sys
import json
import argparse
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class TriageLevel(Enum):
    EMERGENCY = "emergency"      # life-threatening
    URGENT = "urgent"            # Urgent but not immediately fatal
    OUTPATIENT = "outpatient"    # non-urgent


@dataclass
class TriageResult:
    triage_level: str
    confidence: float
    red_flags: List[str]
    reason: str
    recommendation: str
    department: str
    warning: str = "This is AI-assisted advice and cannot replace professional medical diagnosis."


# Red flag sign definition: symptom keywords -> (red flag sign name, triage level, weight, department recommendation, reason)
RED_FLAGS = {
    # Cardiovascular System - Emergency
    "chest pain": ("chest pain", TriageLevel.EMERGENCY, 0.95, "Emergency Department/Cardiology", "Chest pain may be a sign of myocardial infarction, aortic dissection, or pulmonary embolism"),
    "Chest tightness": ("Chest tightness", TriageLevel.EMERGENCY, 0.85, "Emergency Department/Cardiology", "Chest tightness may be a symptom of angina pectoris or myocardial infarction"),
    "Palpitations": ("Palpitations", TriageLevel.URGENT, 0.70, "Cardiology", "Palpitations may be a sign of arrhythmia"),
    "Fainting": ("Fainting", TriageLevel.EMERGENCY, 0.90, "Emergency Department/Neurology", "Fainting may indicate serious cardiac arrhythmia or cerebrovascular accident"),
    "coma": ("coma", TriageLevel.EMERGENCY, 1.0, "emergency department", "Coma is a life-threatening emergency"),

    # Respiratory System - Emergency
    "difficulty breathing": ("difficulty breathing", TriageLevel.EMERGENCY, 0.95, "Emergency Department/Respiratory Department", "Severe dyspnea indicates risk of respiratory failure"),
    "Shortness of breath": ("Shortness of breath", TriageLevel.URGENT, 0.75, "emergency department", "Shortness of breath may be a sign of lung or heart disease"),
    "Hemoptysis": ("Hemoptysis", TriageLevel.EMERGENCY, 0.90, "Emergency Department/Respiratory Department", "Hemoptysis may indicate serious lung disease"),
    "asphyxia": ("asphyxia", TriageLevel.EMERGENCY, 1.0, "emergency department", "Choking is a life-threatening emergency"),

    # Nervous System - Emergency
    "severe headache": ("severe headache", TriageLevel.EMERGENCY, 0.85, "Emergency Department/Neurology", "Sudden severe headache may be subarachnoid hemorrhage"),
    "The most painful thing in life": ("The most painful thing in life", TriageLevel.EMERGENCY, 0.95, "Emergency Department/Neurology", "Indicates the possibility of subarachnoid hemorrhage"),
    "unclear speech": ("unclear speech", TriageLevel.EMERGENCY, 0.90, "Emergency Department/Neurology", "May be a sign of stroke"),
    "hemiplegia": ("hemiplegia", TriageLevel.EMERGENCY, 0.95, "Emergency Department/Neurology", "Typical symptoms of stroke"),
    "Hemiplegia": ("Hemiplegia", TriageLevel.EMERGENCY, 0.95, "Emergency Department/Neurology", "Typical symptoms of stroke"),
    "twitch": ("twitch", TriageLevel.URGENT, 0.80, "Emergency Department/Neurology", "possible epileptic seizure"),
    "epilepsy": ("epilepsy", TriageLevel.URGENT, 0.80, "Neurology", "Epileptic seizures require prompt medical attention"),

    # Digestive System - Emergency
    "Vomiting blood": ("Vomiting blood", TriageLevel.EMERGENCY, 0.95, "Emergency Department/Gastroenterology", "Massive upper gastrointestinal bleeding"),
    "black stool": ("black stool", TriageLevel.URGENT, 0.80, "Gastroenterology", "May indicate upper gastrointestinal bleeding"),
    "Blood in the stool": ("Blood in the stool", TriageLevel.URGENT, 0.75, "Gastroenterology/Anorectology", "gastrointestinal bleeding"),
    "severe abdominal pain": ("severe abdominal pain", TriageLevel.EMERGENCY, 0.85, "emergency department", "It may be acute abdomen such as appendicitis or intestinal perforation"),
    "plate-like belly": ("plate-like belly", TriageLevel.EMERGENCY, 0.95, "Emergency Department/Surgery", "suggestive of peritonitis"),
    "stop exhaust": ("stop exhaust", TriageLevel.URGENT, 0.75, "surgical", "possible intestinal obstruction"),

    # Other Systems - Emergency
    "severe trauma": ("severe trauma", TriageLevel.EMERGENCY, 0.95, "Emergency Department/Surgery", "Severe trauma requires emergency treatment"),
    "Heavy bleeding": ("Heavy bleeding", TriageLevel.EMERGENCY, 1.0, "emergency department", "Risk of hemorrhagic shock"),
    "drug overdose": ("drug overdose", TriageLevel.EMERGENCY, 0.90, "emergency department", "Poisoning requires emergency gastric lavage or detoxification"),
    "Poisoned": ("Poisoned", TriageLevel.EMERGENCY, 0.95, "emergency department", "Poisoning requires emergency treatment"),

    # Pediatric/maternity related
    "Reduced fetal movement": ("Reduced fetal movement", TriageLevel.URGENT, 0.80, "Obstetrics and Gynecology", "May indicate fetal distress"),
    "vaginal bleeding": ("vaginal bleeding", TriageLevel.URGENT, 0.80, "Obstetrics and Gynecology", "Bleeding during pregnancy requires vigilance for miscarriage or placental abruption"),
    "febrile convulsions": ("febrile convulsions", TriageLevel.URGENT, 0.85, "Pediatric emergency", "Febrile convulsions in children require emergency treatment"),
}

# Symptom synonym expansion
SYNONYMS = {
    "chest pain": ["chest pain", "Heartache", "Precordial pain", "chest pain"],
    "difficulty breathing": ["Shortness of breath", "Shortness of breath", "out of breath", "Shortness of breath", "suffocation"],
    "severe headache": ["Exploding headache", "explosion headache", "The most painful thing in life"],
    "hemiplegia": ["Hemiplegia", "Weakness on one side of the body", "Weakness in limbs"],
    "unclear speech": ["Can't speak clearly", "Slurred speech", "difficulty expressing"],
    "coma": ["loss of consciousness", "unconscious", "Can't wake up"],
    "Vomiting blood": ["Vomiting blood", "Vomiting blood"],
    "black stool": ["Tarry stool", "black stool"],
    "severe abdominal pain": ["severe stomach pain", "severe abdominal pain", "Writhing in pain"],
    "Heavy bleeding": ["Bleeding won't stop", "heavy bleeding"],
}

# Clinic-level definitions of common symptoms
OUTPATIENT_SYMPTOMS = {
    "mild headache": ("mild headache", TriageLevel.OUTPATIENT, 0.60, "Neurology", "Common symptoms, recommended outpatient investigation"),
    "low fever": ("low fever", TriageLevel.OUTPATIENT, 0.50, "Internal Medicine", "If the body temperature is <38.5°C, you can go to the outpatient clinic."),
    "cough": ("cough", TriageLevel.OUTPATIENT, 0.40, "Respiratory department", "Cough without dyspnea can be treated in an outpatient setting"),
    "runny nose": ("runny nose", TriageLevel.OUTPATIENT, 0.30, "Otolaryngology", "Common symptoms of upper respiratory tract infection"),
    "sore throat": ("sore throat", TriageLevel.OUTPATIENT, 0.40, "Otolaryngology", "Common in upper respiratory tract infections"),
    "mild abdominal pain": ("mild abdominal pain", TriageLevel.OUTPATIENT, 0.50, "Gastroenterology", "Mild abdominal pain without red flag signs"),
    "diarrhea": ("diarrhea", TriageLevel.OUTPATIENT, 0.50, "Gastroenterology", "Diarrhea without bloody stools or dehydration"),
    "rash": ("rash", TriageLevel.OUTPATIENT, 0.40, "dermatology", "Afebrile rash"),
    "joint pain": ("joint pain", TriageLevel.OUTPATIENT, 0.40, "Rheumatology and Immunology", "chronic joint pain"),
    "Insomnia": ("Insomnia", TriageLevel.OUTPATIENT, 0.30, "Neurology/Psychology", "sleep disorders"),
    "Weakness": ("Weakness", TriageLevel.OUTPATIENT, 0.40, "Internal Medicine", "Need to check for anemia, hypothyroidism, etc."),
}


def expand_synonyms(text: str) -> str:
    """Expand synonyms, replacing all synonyms with standard symptom names"""
    expanded = text
    for standard, synonyms in SYNONYMS.items():
        for syn in synonyms:
            if syn in expanded:
                expanded = expanded.replace(syn, standard)
    return expanded


def extract_red_flags(text: str) -> List[Tuple[str, TriageLevel, float, str, str]]:
    """Extract red flag signs from symptom descriptions"""
    expanded_text = expand_synonyms(text)
    found_flags = []

    for keyword, (name, level, weight, dept, reason) in RED_FLAGS.items():
        if keyword in expanded_text:
            found_flags.append((name, level, weight, dept, reason))

    # Remove duplicates and sort by weight
    seen = set()
    unique_flags = []
    for flag in sorted(found_flags, key=lambda x: x[2], reverse=True):
        if flag[0] not in seen:
            seen.add(flag[0])
            unique_flags.append(flag)

    return unique_flags


def calculate_temperature(text: str) -> Optional[float]:
    """Extract body temperature from text"""
    # Match various body temperature formats
    patterns = [
        '(\\d+\\.?\\d*)\\s*degree',
        r'(\d+\.?\d*)\s*°C',
        r'(\d+\.?\d*)\s*°',
        'Body temperature\\s*(\\d+\\.?\\d*)',
        'Fever\\s*(\\d+\\.?\\d*)',
        'Fever\\s*(\\d+\\.?\\d*)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                temp = float(match.group(1))
                # Determine whether it is Celsius or Fahrenheit
                if temp > 50:  # Convert Fahrenheit to Celsius
                    temp = (temp - 32) * 5 / 9
                return temp
            except ValueError:
                continue
    return None


def extract_outpatient_symptoms(text: str) -> List[Tuple[str, TriageLevel, float, str, str]]:
    """Extract clinic-level symptoms from symptom descriptions"""
    found = []
    text_lower = text.lower()
    
    # Check your temperature first
    temperature = calculate_temperature(text)
    
    for keyword, (name, level, weight, dept, reason) in OUTPATIENT_SYMPTOMS.items():
        if keyword in text:
            found.append((name, level, weight, dept, reason))
    
    # If no specific symptoms are found but body temperature is present, judge based on body temperature
    if not found and temperature:
        if temperature < 38:
            found.append(("low fever", TriageLevel.OUTPATIENT, 0.50, "Internal Medicine", f"body temperature{temperature:.1f}°C，Recommend outpatient consultation"))
        elif temperature < 39:
            found.append(("moderate fever", TriageLevel.OUTPATIENT, 0.60, "Fever clinic", f"body temperature{temperature:.1f}°C，English"))
    
    # Identify common symptom keywords
    if not found:
        common_keywords = {
            "Headache": ("Headache", TriageLevel.OUTPATIENT, 0.60, "Neurology", "Headache without red flags can be investigated in the outpatient clinic"),
            "Dizziness": ("Dizziness", TriageLevel.OUTPATIENT, 0.50, "Neurology/ENT", "Dizziness needs investigation"),
            "nausea": ("nausea", TriageLevel.OUTPATIENT, 0.50, "Gastroenterology", "Nausea without vomiting can be treated in an outpatient clinic"),
            "Vomit": ("Vomit", TriageLevel.OUTPATIENT, 0.60, "Gastroenterology", "Non-severe vomiting can be treated on an outpatient basis"),
            "cold": ("cold symptoms", TriageLevel.OUTPATIENT, 0.50, "Internal Medicine", "common cold symptoms"),
            "fever": ("fever", TriageLevel.OUTPATIENT, 0.60, "Fever clinic", "Fever requires further examination"),
            "fever": ("fever", TriageLevel.OUTPATIENT, 0.60, "Fever clinic", "Fever requires further examination"),
        }
        for keyword, symptom_info in common_keywords.items():
            if keyword in text:
                found.append(symptom_info)
    
    return found


def triage(symptom_text: str) -> TriageResult:
    """main triage function

    Args:
        symptom_text: symptom description text

    Returns:
        TriageResult: Triage result"""
    if not symptom_text or not symptom_text.strip():
        return TriageResult(
            triage_level=TriageLevel.OUTPATIENT.value,
            confidence=0.0,
            red_flags=[],
            reason="No description of symptoms provided",
            recommendation="Please provide a description of symptoms for triage",
            department="unknown"
        )

    # Extract red flag signs
    red_flags = extract_red_flags(symptom_text)

    # Extract body temperature
    temperature = calculate_temperature(symptom_text)

    # Check for high fever
    if temperature and temperature >= 40:
        red_flags.append(("High fever (≥40°C)", TriageLevel.EMERGENCY, 0.90, "emergency department", "High fever accompanied by changes in consciousness requires emergency treatment"))
    elif temperature and temperature >= 39:
        red_flags.append(("High fever (≥39°C)", TriageLevel.URGENT, 0.70, "Fever clinic", "High fever requires prompt medical treatment"))

    # If there are red flags
    if red_flags:
        # Take the most severe level
        max_level = max(red_flags, key=lambda x: x[2])
        level = max_level[1]
        confidence = min(0.95, max(flag[2] for flag in red_flags))
        flag_names = [flag[0] for flag in red_flags]
        departments = list(dict.fromkeys(flag[3] for flag in red_flags))  # Remove duplication and maintain order
    
        if level == TriageLevel.EMERGENCY:
            recommendation = "Go to the emergency room immediately and call 120 if necessary"
        elif level == TriageLevel.URGENT:
            recommendation = "It is recommended to seek medical treatment within 2-4 hours, and you can go to the emergency room or fever clinic"
        else:
            recommendation = "It is recommended to make an appointment for outpatient treatment as soon as possible"

        # Reasons for merger
        reasons = [f"{flag[0]}: {flag[4]}" for flag in red_flags[:3]]
        reason = "; ".join(reasons)

        return TriageResult(
            triage_level=level.value,
            confidence=confidence,
            red_flags=flag_names,
            reason=reason,
            recommendation=recommendation,
            department="/".join(departments[:2])
        )

    # Check for clinic-level symptoms
    outpatient = extract_outpatient_symptoms(symptom_text)
    if outpatient:
        max_symptom = max(outpatient, key=lambda x: x[2])
        return TriageResult(
            triage_level=TriageLevel.OUTPATIENT.value,
            confidence=max_symptom[2],
            red_flags=[],
            reason=f"symptom'{max_symptom[0]}'No red flags，English",
            recommendation="It is recommended to make an appointment for outpatient treatment. If symptoms worsen, please seek medical treatment in time.",
            department=max_symptom[3]
        )

    # unrecognized symptoms
    return TriageResult(
        triage_level=TriageLevel.OUTPATIENT.value,
        confidence=0.30,
        red_flags=[],
        reason="Unrecognizable symptoms, it is recommended to seek medical evaluation",
        recommendation="It is recommended to make an appointment with the internal medicine clinic for initial evaluation.",
        department="Internal Medicine"
    )


def interactive_mode():
    """interactive mode"""
    print("=" * 50)
    print("Symptom Checker Triage")
    print("=" * 50)
    print("Please enter a symptom description (such as 'chest pain, difficulty breathing') and enter 'quit' to exit")
    print("-" * 50)

    while True:
        try:
            user_input = input("Symptom description:").strip()
            if user_input.lower() in ['quit', 'exit', 'q', 'quit']:
                print("Thanks for using, bye!")
                break

            if not user_input:
                continue

            result = triage(user_input)
            print_result(result)

        except KeyboardInterrupt:
            print("Thanks for using, bye!")
            break
        except EOFError:
            break


def supports_color() -> bool:
    """Check if the terminal supports colors"""
    import os
    return sys.stdout.isatty() and os.environ.get('TERM') not in ('dumb', '')


def print_result(result: TriageResult, verbose: bool = False):
    """Print triage results"""
    use_color = supports_color()
    level_colors = {
        "emergency": "\033[91m" if use_color else "",  # red
        "urgent": "\033[93m" if use_color else "",     # yellow
        "outpatient": "\033[92m" if use_color else "", # green
    }
    reset = "\033[0m" if use_color else ""

    level_display = {
        "emergency": "🔴 Emergency",
        "urgent": "🟠 Urgent",
        "outpatient": "🟢Outpatient",
    }

    level = result.triage_level
    color = level_colors.get(level, "")

    print("\n" + "=" * 50)
    print(f"triage level: {color}{level_display.get(level, level)}{reset}")
    print(f"Confidence: {result.confidence:.0%}")

    if result.red_flags:
        print(f"\n🚨 Red flags identified:")
        for flag in result.red_flags:
            print(f"   - {flag}")

    print(f"\n📋 Reasons for triage:")
    print(f"   {result.reason}")

    print(f"\n💡 suggestion:")
    print(f"   {result.recommendation}")

    print(f"\n🏥 Suggested departments: {result.department}")

    if verbose:
        print(f"\n⚠️  Disclaimer: {result.warning}")

    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Symptom Triage Assistant - Recommends triage levels based on red flags",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Example:
  python main.py "Chest pain, radiating to left arm, sweating"
  python main.py --interactive
  python main.py "Headache, fever 38 degrees" --verbose"""
    )
    parser.add_argument(
        "symptoms",
        nargs="?",
        help="Description of symptoms (e.g. 'chest pain, difficulty breathing')"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Enter interactive mode"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show details"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
        return

    if not args.symptoms:
        parser.print_help()
        print("Error: Please provide a symptom description or use --interactive to enter interactive mode")
        sys.exit(1)

    result = triage(args.symptoms)

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print_result(result, verbose=args.verbose)


if __name__ == "__main__":
    main()
