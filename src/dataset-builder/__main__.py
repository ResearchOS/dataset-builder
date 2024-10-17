import argparse

def main():
    # Parse the arguments

    # Command: build
    # Arguments: --path
    # Description: Build the dataset
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    build_parser = subparsers.add_parser('build', help='Build the dataset')
    build_parser.add_argument('--path', required=True)

    args = parser.parse_args()
    if args.command == 'build':
        print('Building the dataset at path:', args.path)
    else:
        print('Unknown command:', args.command)

if __name__ == '__main__':
    main()