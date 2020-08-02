import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--boot", type=int, help="bootstrap iteration")
    parser.add_argument("-f", "--out_dir", type=str, help="output directory")
    args = parser.parse_args()
    print(args)
    print(args.out_dir)
    with open(f"{args.out_dir}/ptf{args.boot}.out", "w") as f:
        f.writelines(f"test {args.boot}")
    print("testing...")
    print(args.boot)
