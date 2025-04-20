import json
import random
import argparse


# Usage - python generate_inputs.py -n 20 -o inputs.txt --min 1 --max 50 -v :x :y :z :p
# Generates 20 random input lines for exampl1.tl
def main():
    p = argparse.ArgumentParser(
        description="Generate N random input‐dict lines for Ball‑Larus profiling"
    )
    p.add_argument("-n", "--num", type=int, default=10,
                   help="Number of input lines to generate")
    p.add_argument("-o", "--out", default="inputs.txt",
                   help="Output filename")
    p.add_argument("--min", type=int, default=0,
                   help="Minimum random value (inclusive)")
    p.add_argument("--max", type=int, default=100,
                   help="Maximum random value (inclusive)")
    p.add_argument("-v", "--vars", nargs="+",
                   default=[":x", ":y", ":z", ":p"],
                   help="List of variable names (include leading colon)")
    args = p.parse_args()

    with open(args.out, "w") as f:
        for _ in range(args.num):
            data = {var: random.randint(args.min, args.max) for var in args.vars}
            json.dump(data, f)
            f.write("\n")

    print(f"Wrote {args.num} random inputs to {args.out}")

if __name__ == "__main__":
    main()