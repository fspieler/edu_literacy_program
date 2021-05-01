import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate some simple test data"
    )
    parser.add_argument(
        "--levels",
        type=int,
        default=6,
        help="Max number of levels (default and max are 6)"
    )
    parser.add_argument(
        "--questions-per-level",
        type=int,
        default=10,
        help="Number of generated questions per level"
    )
    parser.add_argument(
        "--destination",
        default="demo_test.json",
        help="name of file to write"
    )
    parser.add_argument(
        "--name",
        default="Demo test",
        help="Name of test as it will show up in UI"
    )
    args = vars(parser.parse_args())
    return args

def write_test(name, destination, levels, questions_per_level):
    print(name, destination, levels, questions_per_level)
    test = {"name": name, "questions": []}
    for level in range(1, levels+1): # 1-indexed
        for question in range(1, questions_per_level+1): # 1-indexed
            test["questions"].append({
                "name": f"Level {level} Question {question}",
                "difficulty": level,
                "content": {
                    "type": "multiple-choice",
                    "prompt": f"Level {level} Question {question}<br/>What is the answer?",
                    "correct_idx": 0,
                    "answers": [
                        "the correct answer",
                        "an incorrect answer",
                        "an incorrect answer",
                        "an incorrect answer"
                    ]
                }
            })
    with open(destination, 'w') as f:
        json.dump(test, f, indent=4)

def main():
    write_test(**parse_args())


if __name__ == '__main__':
    main()
