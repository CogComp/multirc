import json
from pprint import pprint

def main():
    print("asdasd")
    eval()

def eval():
    input = json.load(open('/Users/daniel/ideaProjects/multirc/eval/sample-input.json'))
    output = json.load(open('/Users/daniel/ideaProjects/multirc/eval/sample-output-binary.json'))
    pprint(input)
    pprint(output)


if __name__ == "__main__":
    main()