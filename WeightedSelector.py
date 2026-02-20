"""
Weighted Selector Microservice
Reads weighted outcome requests from weighted_selector.txt and returns one randomly selected outcome
Format: outcome1:weight1,outcome2:weight2,outcome3:weight3
"""

import random
import time


def parse_request(request_string):
    """
    Parse the request string into outcomes and weights.
    Returns tuple: (outcomes_list, weights_list) or (None, error_message)
    """
    try:
        request_string = request_string.strip()

        if not request_string:
            return None, "ERROR: Invalid format. Use outcome1:weight1,outcome2:weight2"

        # split by comma to get pairs
        pairs = request_string.split(',')

        if len(pairs) < 2:
            return None, "ERROR: Invalid format. Use outcome1:weight1,outcome2:weight2"

        outcomes = []
        weights = []

        for pair in pairs:
            pair = pair.strip()

            # check for colon
            if ':' not in pair:
                return None, "ERROR: Invalid format. Use outcome1:weight1,outcome2:weight2"

            # split on colon
            parts = pair.split(':', 1)  # limit to 1 split in case outcome has colons

            if len(parts) != 2:
                return None, "ERROR: Invalid format. Use outcome1:weight1,outcome2:weight2"

            outcome = parts[0].strip()
            weight_str = parts[1].strip()

            # validate outcome not empty
            if not outcome:
                return None, "ERROR: Invalid format. Use outcome1:weight1,outcome2:weight2"

            # parse weight
            try:
                weight = float(weight_str)
            except ValueError:
                return None, "ERROR: Invalid format. Use outcome1:weight1,outcome2:weight2"

            # validate weight is positive
            if weight <= 0:
                return None, "ERROR: Weights must be positive numbers"

            outcomes.append(outcome)
            weights.append(weight)

        # check we have at least 2 outcomes
        if len(outcomes) < 2:
            return None, "ERROR: Must provide at least 2 outcomes"

        # check we don't exceed 100 outcomes
        if len(outcomes) > 100:
            return None, "ERROR: Maximum 100 outcomes allowed"

        return outcomes, weights

    except Exception as e:
        return None, "ERROR: Invalid format. Use outcome1:weight1,outcome2:weight2"


def weighted_select(outcomes, weights):
    """
    Select one outcome based on weighted probabilities.
    Uses the cumulative weight algorithm.
    """
    # calculate total weight
    total_weight = sum(weights)

    # generate random value in range
    random_value = random.uniform(0, total_weight)

    # find outcome using cumulative ranges
    cumulative = 0
    for outcome, weight in zip(outcomes, weights):
        cumulative += weight
        if random_value < cumulative:
            return outcome

    # fallback (shouldn't happen, but just in case of floating point issues)
    return outcomes[-1]


def process_request():
    """
    Read request from file, process it, write result back.
    """
    try:
        # read request
        with open('weighted_selector.txt', 'r') as f:
            request = f.read()

        # parse request
        result = parse_request(request)

        if result[0] is None:
            # error occurred
            error_message = result[1]
            with open('weighted_selector.txt', 'w') as f:
                f.write(error_message)
            return

        outcomes, weights = result

        # select outcome
        selected = weighted_select(outcomes, weights)

        # write result
        with open('weighted_selector.txt', 'w') as f:
            f.write(selected)

    except FileNotFoundError:
        # file doesn't exist yet, just wait
        pass
    except Exception as e:
        # unexpected error - write generic error message
        try:
            with open('weighted_selector.txt', 'w') as f:
                f.write("ERROR: Invalid format. Use outcome1:weight1,outcome2:weight2")
        except:
            pass  # can't even write error, just continue


def main():
    """
    Main loop - continuously monitor file for requests.
    """
    print("Weighted Selector microservice running...")
    print("Waiting for requests in weighted_selector.txt")

    last_request = None

    while True:
        try:
            # check if file exists and has content
            with open('weighted_selector.txt', 'r') as f:
                current_request = f.read()

            # only process if content changed
            if current_request and current_request != last_request:
                # check if it's not an error message or result from previous run
                if not current_request.startswith('ERROR:') and ':' in current_request and ',' in current_request:
                    print(f"Processing request: {current_request[:50]}...")
                    process_request()
                    last_request = current_request
                    print("Result written to weighted_selector.txt")

        except FileNotFoundError:
            # file doesn't exist yet, that's fine
            pass
        except Exception as e:
            # unexpected error, log but don't crash
            print(f"Error: {e}")

        # small delay to avoid hammering the file system
        time.sleep(0.1)

if __name__ == '__main__':
    main()