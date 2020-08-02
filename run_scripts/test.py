import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--boot", type=int, help="bootstrap iteration")
    args = parser.parse_args()
    with open(f"ptf{args.boot}.out", "w") as f:
        f.writelines(f"test {args.boot}")
    print("testing...")
    print(args.boot)
