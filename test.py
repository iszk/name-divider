import divider
import sys


if __name__ == '__main__':
	argv = sys.argv
	if len(argv) != 2:
		print("usage\n\tpython {} name".format(argv[0]))
		sys.exit(-1)

	(first_name, last_name) = divider.divide(argv[1])

	print("{} -> {}\t{}".format(argv[1], first_name, last_name))



