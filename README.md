# Number Classification API

## Description
The Number Classification API built with the use of Flask framework, it is a service that provides information about numbers. It can determine if a number is prime, perfect, or Armstrong, and it retrieves fun facts from external APIs.

## Features
- Check if a number is prime.
- Check if a number is perfect.
- Check if a number is an Armstrong number.
- Retrieve fun facts about numbers from Numbers API.


## API Endpoint
### Classify Number
- **Endpoint**: `/api/classify-number/`
- **Method**: `GET`
- **Query Params**:
  - `number`: The number to classify (required).

### Example Request
```
GET http://localhost:5000/api/classify-number/?number=5
```

### Example Response
```json
{
  "number": 5,
  "is_prime": true,
  "is_perfect": false,
  "properties": ["odd"],
  "digit_sum": 5,
  "fun_fact": "5 is a prime number."
}
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd Number_classification_API
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application:
```bash
python app.py
```
Access the API at `http://127.0.0.1:5000/api/classify-number/?number=<num>`, where `<num>` is the number you want to inquire about.

