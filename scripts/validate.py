#!/usr/bin/env python3
"""Validate generated question JSON files against schema."""
import json, sys, os, glob

def validate_question(q, idx, filename):
    errors = []
    required = ["id", "domain", "difficulty", "vignette", "question", "options", "correct", "explanations", "pearl", "references"]
    
    for field in required:
        if field not in q:
            errors.append(f"  [{idx}] Missing field: {field}")
    
    if "options" in q:
        for letter in "ABCDE":
            if letter not in q["options"]:
                errors.append(f"  [{idx}] Missing option {letter}")
            elif len(q["options"][letter]) < 5:
                errors.append(f"  [{idx}] Option {letter} too short")
    
    if "correct" in q and q["correct"] not in "ABCDE":
        errors.append(f"  [{idx}] Invalid correct answer: {q['correct']}")
    
    if "explanations" in q:
        for letter in "ABCDE":
            if letter not in q["explanations"]:
                errors.append(f"  [{idx}] Missing explanation for {letter}")
            elif len(q["explanations"][letter]) < 20:
                errors.append(f"  [{idx}] Explanation {letter} too short (<20 chars)")
    
    if "vignette" in q and len(q["vignette"]) < 50:
        errors.append(f"  [{idx}] Vignette too short (<50 chars)")
    
    if "difficulty" in q and q["difficulty"] not in [1, 2, 3]:
        errors.append(f"  [{idx}] Invalid difficulty: {q['difficulty']}")
    
    return errors

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gen_dir = os.path.join(base, "data", "generated")
    
    if not os.path.exists(gen_dir):
        print("No data/generated/ directory found.")
        sys.exit(1)
    
    files = glob.glob(os.path.join(gen_dir, "*.json"))
    if not files:
        print("No JSON files in data/generated/")
        sys.exit(1)
    
    total_q = 0
    total_errors = 0
    ids_seen = set()
    
    for filepath in sorted(files):
        fname = os.path.basename(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"FAIL {fname}: Invalid JSON — {e}")
                total_errors += 1
                continue
        
        if not isinstance(data, list):
            print(f"FAIL {fname}: Root must be array")
            total_errors += 1
            continue
        
        file_errors = []
        for i, q in enumerate(data):
            # Check duplicate IDs
            qid = q.get("id", f"UNKNOWN-{i}")
            if qid in ids_seen:
                file_errors.append(f"  [{i}] Duplicate ID: {qid}")
            ids_seen.add(qid)
            
            file_errors.extend(validate_question(q, i, fname))
        
        if file_errors:
            print(f"WARN {fname}: {len(data)} questions, {len(file_errors)} issues:")
            for e in file_errors[:10]:
                print(e)
            if len(file_errors) > 10:
                print(f"  ... and {len(file_errors)-10} more")
            total_errors += len(file_errors)
        else:
            print(f"  OK {fname}: {len(data)} questions")
        
        total_q += len(data)
    
    print(f"\n{'='*40}")
    print(f"Total: {total_q} questions in {len(files)} files")
    print(f"Errors: {total_errors}")
    print(f"Unique IDs: {len(ids_seen)}")
    
    if total_errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
