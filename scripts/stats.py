#!/usr/bin/env python3
"""Print statistics about the question bank."""
import json, os, glob

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("PSYCH QBANK — Statistics")
print("=" * 50)

# PreTest
pretest_dir = os.path.join(base, "data", "pretest")
if os.path.exists(pretest_dir):
    pt_total = 0
    for f in sorted(glob.glob(os.path.join(pretest_dir, "*.json"))):
        data = json.load(open(f, encoding='utf-8'))
        name = os.path.basename(f).replace('.json', '')
        pt_total += len(data)
        print(f"  PreTest/{name:20s}: {len(data):3d}")
    print(f"  {'PreTest TOTAL':24s}: {pt_total:3d}")

print()

# Generated
gen_dir = os.path.join(base, "data", "generated")
if os.path.exists(gen_dir):
    gen_total = 0
    for f in sorted(glob.glob(os.path.join(gen_dir, "*.json"))):
        data = json.load(open(f, encoding='utf-8'))
        name = os.path.basename(f).replace('.json', '')
        gen_total += len(data)
        d1 = sum(1 for q in data if q.get('difficulty') == 1)
        d2 = sum(1 for q in data if q.get('difficulty') == 2)
        d3 = sum(1 for q in data if q.get('difficulty') == 3)
        print(f"  Generated/{name:17s}: {len(data):3d}  (d1:{d1} d2:{d2} d3:{d3})")
    print(f"  {'Generated TOTAL':24s}: {gen_total:3d}")

print(f"\n  {'GRAND TOTAL':24s}: {pt_total + gen_total:3d}")
