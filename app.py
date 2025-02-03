from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

NcApi = Flask(__name__)
CORS(NcApi)


NUMBERS_API_URL = 'http://numbersapi.com/{}/math?json=true'

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


@NcApi.route('/number/<num>', methods=['GET'])
def get_num_info(num):
    try:
        if num == '':
            return jsonify({'error': 'Please enter a number'}), 400
        
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
        return jsonify({"error": "API request failed", "details": str(e)}), 500
    except KeyError as e:
        logging.error(f"KeyError occurred: {e}")
        return jsonify({"error": "Data format mismatch", "details": str(e)}), 500
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal error occurred", "details": str(e)}), 500

@NcApi.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'The requested URL was not or you did not input any number.',
        'message': 'Please check the URL correct your mistake and try again.'
    }), 404


if __name__ == '__main__':
    NcApi.run(debug=True)