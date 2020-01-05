import argparse

parser = argparse.ArgumentParser()

#parser.add_argument("echo", help = "echo the string you use here")
group = parser.add_mutually_exclusive_group()
group.add_argument("-V", "--verbose", help = "increase output verbosity", action = "store_true")
group.add_argument("-Q", '--quiet', help = "decrease output", action = "store_true")
parser.add_argument("square", help = "display a square of a given number", type = int)

args = parser.parse_args()
if args.verbose:
    print(f"the square of {args.square} is {args.square ** 2}")
elif args.quiet:
    print(f'{args.square ** 2}')
#print(args.square ** 2)
#print(args.echo)
#parser.parse_args()
