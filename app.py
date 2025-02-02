from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

NcApi = Flask(__name__)
CORS(NcApi)


NUMBERS_API_URL = 'http://numbersapi.com/{}/math?json=true'
WIKIPEDIA_API_URL = 'https://en.wikipedia.org/api/rest_v1/page/summary/{}'

def is_prime(n):
    #very important alost skipped my mind
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    #perfectly beautiful
    if n < 2:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def digit_sum(n):
    #possible summation
    return sum(int(digit) for digit in str(n))

def is_armstrong(n):
    #really tried my best not check google for the meaning of this 😂😂😂😂
    digits = [int(digit) for digit in str(n)]
    num_digits = len(digits)
    return sum(digit ** num_digits for digit in digits) == n

def get_properties(n):
    #sequencing
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    return properties


@NcApi.route('/<num>', methods=['GET'])
def get_num_info(num):
    try:
        #error handling to give the response if the input is an alphabet
        if not num.isdigit():
            return jsonify({
                'number': 'alphabet',
                'error': True
            }), 400

        num = int(num)


        num_response = requests.get(NUMBERS_API_URL.format(num))
        num_response.raise_for_status()  # Raise an error for bad responses
        num_data = num_response.json()


        wiki_response = requests.get(WIKIPEDIA_API_URL.format(num))
        wiki_response.raise_for_status()  # Raise an error for bad responses
        wiki_data = wiki_response.json()

        # Calculating the added infos
        prime = is_prime(num)
        perfect = is_perfect(num)
        sum_digits = digit_sum(num)
        properties = get_properties(num)


        # Combination of all THE DATA
        combined_data = {
            'number': num,
            'is_prime': prime,
            'is_perfect': perfect,
            'properties': properties,
            'digit_sum': sum_digits,
            'fun_fact': num_data.get('text', 'No fun fact available'),
        }

        return jsonify(combined_data)

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return jsonify({"error": "API request failed"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500
    

if __name__ == '__main__':
    NcApi.run(debug=True)