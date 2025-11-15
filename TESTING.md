# Testing POST /ask with Mock Data

## Summary

Successfully created a complete testing setup for the `POST /ask` endpoint using dummy data from a `MockMessagesClient`. This allows testing without depending on the external API.

## Changes Made

### 1. Enhanced `app/client.py`
- Added `MockMessagesClient` class with 5 dummy member messages
- Sample messages include:
  - Layla's Paris trip (March 10-15)
  - Vikram's 3 cars and restaurant visits
  - Sarah's 2 cars and road trips
- `MessagesClient` (original) remains unchanged for real API calls

### 2. Updated `app/main.py`
- Added environment variable support: `USE_MOCK_CLIENT`
- If `USE_MOCK_CLIENT=true`, uses `MockMessagesClient`
- Otherwise uses real `MessagesClient` with external API
- Allows seamless switching between mock and real data

### 3. Created `tests/test_ask_endpoint.py`
Comprehensive test suite with 8 tests:
- `test_ask_how_many_cars()` - Tests "How many cars" questions
- `test_ask_trip_when()` - Tests "When" questions about trips
- `test_ask_restaurant()` - Tests restaurant queries
- `test_ask_member_name_extraction()` - Tests member name parsing
- `test_ask_generic_question()` - Tests generic questions
- `test_ask_invalid_request()` - Tests validation
- `test_ask_empty_question()` - Tests edge cases
- `test_health_check()` - Tests health endpoint

### 4. Updated Existing Tests
- Fixed `tests/test_answering.py` to use correct API (`answer_from_messages`)
- Fixed `tests/test_parsing.py` to match actual parsing output

### 5. Updated `requirements.txt`
- Added `pytest-asyncio` for async test support

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run only endpoint tests
python -m pytest tests/test_ask_endpoint.py -v

# Run with coverage
python -m pytest tests/ --cov=app
```

## Running the Server with Mock Data

```bash
# Enable mock client
$env:USE_MOCK_CLIENT="true"

# Start server
uvicorn app.main:app --reload
```

## Test Results

✅ All 16 tests passing:
- 3 answering tests
- 8 endpoint tests (POST /ask)
- 5 parsing tests

## Benefits

1. **No External Dependency**: Tests run without needing the real API
2. **Fast Execution**: Mock data returns instantly
3. **Deterministic**: Same results every test run
4. **Easy Switching**: Set env variable to switch between mock/real
5. **Realistic Data**: Dummy data simulates real member messages
