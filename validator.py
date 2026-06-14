import argparse

from beta_code.validation.validator import Validator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default='../data', help="Validate data in dir (default 'data')")
    parser.add_argument("--input_file", type=str, default='input',
                        help="Name of instance input file (default 'input')")
    parser.add_argument("--result_file", type=str, default='result',
                        help="Name of instance result file (default 'result')")

    args = parser.parse_args()

    directory = args.dir
    input_file_name = args.input_file
    result_file_name = args.result_file

    input_file_path = f"{directory}/{input_file_name}.json"
    result_file_path = f"{directory}/{result_file_name}.json"
    Validator(input_file_path, result_file_path).validation()
