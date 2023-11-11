import sys
from analysis import number_one, number_two, number_three, number_four, number_five, number_six, number_seven

# A dictionary mapping argument numbers to functions
functions = {
    '1': number_one,
    '2': number_two,
    '3': number_three,
    '4': number_four,
    '5': number_five,
    '6': number_six,
    '7': number_seven,
}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py <number>")
        sys.exit(1)

    # The second command-line argument is expected to be the number
    arg = sys.argv[1]

    # Get the function to call from the functions dictionary
    func_to_call = functions.get(arg)
    if func_to_call:
        result = func_to_call()
        if hasattr(result, 'show'):
            # If the result has a 'show' method, we assume it's a figure and call 'show'
            result.show()
        else:
            # Otherwise, we just print the result
            print(result)
    else:
        print(f"No function associated with the number {arg}.")
