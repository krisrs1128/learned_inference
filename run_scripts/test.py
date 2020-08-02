import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--boot", type=int, help="bootstrap iteration")
    args = parser.parse_args()
    print("testing...")
    print(args.boot)
