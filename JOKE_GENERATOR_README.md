# 🎭 Random Joke Generator

A Python application that fetches random jokes from multiple external APIs.

## Features

- 🎲 Fetches jokes from 3 different external APIs for variety
- 🔄 Automatic fallback and error handling
- 📦 Support for single or multiple jokes
- 🎯 Choose specific API or use random selection
- 📝 Clean, well-documented code

## Supported APIs

1. **Official Joke API** (`official_joke_api`)
   - URL: https://official-joke-api.appspot.com/
   - Format: Setup/Punchline jokes

2. **JokeAPI** (`jokeapi`)
   - URL: https://v2.jokeapi.dev/
   - Format: Single or two-part jokes

3. **Dad Jokes** (`dad_jokes`)
   - URL: https://icanhazdadjoke.com/
   - Format: Single-line dad jokes

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### As a Script

```bash
python joke_generator.py
```

Output:
```
============================================================
🎭 RANDOM JOKE GENERATOR 🎭
============================================================

📝 Single Random Joke:
------------------------------------------------------------
Source: dad_jokes
Joke: Why don't scientists trust atoms? Because they make up everything!
```

### As a Module

```python
from joke_generator import JokeGenerator

# Get a single random joke
joke = JokeGenerator.get_joke()
print(joke["joke"])

# Get a joke from a specific API
joke = JokeGenerator.get_joke(api_source="official_joke_api")
print(f"{joke['joke']} (Source: {joke['source']})")

# Get multiple jokes
jokes = JokeGenerator.get_multiple_jokes(count=5)
for joke in jokes:
    print(f"- {joke['joke']}")
```

## API Reference

### `JokeGenerator.get_joke(api_source=None)`

Fetch a single random joke.

**Parameters:**
- `api_source` (str, optional): Specific API to use. Options: `'official_joke_api'`, `'jokeapi'`, `'dad_jokes'`. If None, randomly selects one.

**Returns:**
- Dictionary with keys:
  - `joke` (str): The joke text
  - `source` (str): Which API was used
  - `type` (str, optional): Joke type (setup/punchline or twopart)
  - `error` (bool, optional): True if an error occurred

**Example:**
```python
joke = JokeGenerator.get_joke()
# Returns: {"joke": "...", "source": "dad_jokes"}
```

### `JokeGenerator.get_multiple_jokes(count=5, api_source=None)`

Fetch multiple random jokes.

**Parameters:**
- `count` (int): Number of jokes to fetch (default: 5)
- `api_source` (str, optional): Specific API to use for all jokes

**Returns:**
- List of joke dictionaries

**Example:**
```python
jokes = JokeGenerator.get_multiple_jokes(count=3)
# Returns: [{"joke": "...", "source": "..."}, ...]
```

## Error Handling

The generator includes robust error handling:

```python
try:
    joke = JokeGenerator.get_joke("invalid_api")
except ValueError as e:
    print(f"Invalid API source: {e}")

# API errors are gracefully handled
joke = JokeGenerator.get_joke()
if joke.get('error'):
    print(f"Failed to fetch: {joke['joke']}")
```

## Examples

### Example 1: Daily Joke

```python
from joke_generator import JokeGenerator
import schedule
import time

def daily_joke():
    joke = JokeGenerator.get_joke()
    print(f"Today's joke: {joke['joke']}")

# Schedule once per day
schedule.every().day.at("10:30").do(daily_joke)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Example 2: Joke of the Day with Stats

```python
from joke_generator import JokeGenerator

jokes = JokeGenerator.get_multiple_jokes(count=10)

# Display all jokes
for i, joke in enumerate(jokes, 1):
    print(f"{i}. ({joke['source']}) {joke['joke']}")

# Stats
sources = {}
for joke in jokes:
    source = joke['source']
    sources[source] = sources.get(source, 0) + 1

print("\nAPI Usage Stats:")
for source, count in sources.items():
    print(f"  {source}: {count} jokes")
```

### Example 3: Web API Integration (Flask)

```python
from flask import Flask
from joke_generator import JokeGenerator

app = Flask(__name__)

@app.route('/joke', methods=['GET'])
def get_random_joke():
    joke = JokeGenerator.get_joke()
    return {
        'joke': joke['joke'],
        'source': joke['source']
    }

@app.route('/jokes/<int:count>', methods=['GET'])
def get_multiple(count):
    jokes = JokeGenerator.get_multiple_jokes(count=min(count, 20))
    return {'jokes': jokes}

if __name__ == '__main__':
    app.run(debug=True)
```

## Notes

- All APIs are free and public, no authentication required
- Requests have a 5-second timeout to prevent hanging
- If an API is down, you'll get an error message, but you can still use other APIs
- The selection of jokes from `jokeapi` can sometimes include potentially offensive content (configure in settings if needed)

## Dependencies

- `requests` - HTTP library for API calls

## License

MIT

## Contributing

Feel free to add more joke APIs or improve the existing implementation!

## Troubleshooting

**Q: I'm getting timeout errors**
A: The external APIs might be slow. The timeout is set to 5 seconds. You can modify this in the `get_joke()` method.

**Q: All APIs are returning errors**
A: Check your internet connection and verify that the external APIs are accessible:
- https://official-joke-api.appspot.com/random_joke
- https://v2.jokeapi.dev/joke/Any
- https://icanhazdadjoke.com/?format=json

**Q: How do I add a new joke API?**
A: Add an entry to `JOKE_APIS` dictionary and create a corresponding parser method following the existing pattern.
