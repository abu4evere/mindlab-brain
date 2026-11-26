"""CX2-C's analysis: the frozen analyse_cx2.py, imported unchanged, run on CX2-C's four arms.

CX2-C (CX2/questions.md, "CX2-C, the confirmatory run") repeats LEARN, RANDOM-5P, BLIND and NAMED; LEARN-NP is not
repeated, so the frozen script stops at the missing learn_np.jsonl. This wrapper only removes LEARN-NP from the arm list
(the rest keeps the frozen order: learn, named, blind, random5p, one generator default_rng(0)) and drops the one
comparison that needs it (learn - learn_np, "what the poke adds"). Scores, bootstrap, intervals, readings and the
'close' rule are the frozen code's. Written 26 Nov 2026 (EST), after CX2-C's data existed: a mechanical change,
recorded openly in CX2/questions.md.

  python analyse_cx2c.py CX2/output_confirm   -> CX2/output_confirm/analysis.json and the printed table
"""
import analyse_cx2 as A

A.ARMS = ("learn", "named", "blind", "random5p")
A.COMPARE = [c for c in A.COMPARE if "learn_np" not in (c[0], c[1])]

if __name__ == "__main__":
    A.main()
