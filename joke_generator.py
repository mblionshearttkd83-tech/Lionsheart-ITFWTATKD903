#!/usr/bin/env python3
"""
Random Joke Generator using external APIs
Fetches jokes from multiple sources for variety
"""

import requests
import random
import json
from typing import Dict, Optional


class JokeGenerator:
    """Generate random jokes from various external APIs"""
    
    # Available joke APIs
    JOKE_APIS = {
        "official_joke_api": {
            "url": "https://official-joke-api.appspot.com/random_joke",
            "parser": "parse_official_joke"
        },
        "jokeapi": {
            "url": "https://v2.jokeapi.dev/joke/Any",
            "parser": "parse_jokeapi"
        },
        "dad_jokes": {
            "url": "https://icanhazdadjoke.com/",
            "parser": "parse_dad_joke",
            "headers": {"Accept": "application/json"}
        }
    }
    
    @staticmethod
    def get_joke(api_source: Optional[str] = None) -> Dict[str, str]:
        """
        Fetch a random joke from an external API
        
        Args:
            api_source: Optional specific API to use. If None, randomly selects one.
                       Options: 'official_joke_api', 'jokeapi', 'dad_jokes'
        
        Returns:
            Dictionary containing the joke with 'joke' and 'source' keys
        
        Raises:
            requests.RequestException: If API call fails
            ValueError: If invalid api_source provided
        """
        if api_source and api_source not in JokeGenerator.JOKE_APIS:
            raise ValueError(f"Invalid API source. Choose from: {list(JokeGenerator.JOKE_APIS.keys())}")
        
        # Select random API if not specified
        selected_api = api_source or random.choice(list(JokeGenerator.JOKE_APIS.keys()))
        
        api_config = JokeGenerator.JOKE_APIS[selected_api]
        
        try:
            headers = api_config.get("headers", {})
            response = requests.get(api_config["url"], headers=headers, timeout=5)
            response.raise_for_status()
            
            # Parse response based on API type
            parser_method = getattr(JokeGenerator, api_config["parser"])
            joke_data = parser_method(response.json())
            joke_data["source"] = selected_api
            
            return joke_data
        
        except requests.RequestException as e:
            return {
                "joke": f"Failed to fetch joke: {str(e)}",
                "source": selected_api,
                "error": True
            }
    
    @staticmethod
    def parse_official_joke(data: Dict) -> Dict[str, str]:
        """Parse joke from Official Joke API format"""
        return {
            "joke": f"{data.get('setup')} {data.get('punchline')}",
            "type": data.get('type', 'unknown')
        }
    
    @staticmethod
    def parse_jokeapi(data: Dict) -> Dict[str, str]:
        """Parse joke from JokeAPI format"""
        if data.get('type') == 'single':
            return {"joke": data.get('joke', 'No joke found')}
        else:
            return {
                "joke": f"{data.get('setup')} {data.get('delivery')}",
                "type": "twopart"
            }
    
    @staticmethod
    def parse_dad_joke(data: Dict) -> Dict[str, str]:
        """Parse joke from Dad Jokes API format"""
        return {"joke": data.get('joke', 'No joke found')}
    
    @staticmethod
    def get_multiple_jokes(count: int = 5, api_source: Optional[str] = None) -> list:
        """
        Fetch multiple jokes
        
        Args:
            count: Number of jokes to fetch (default: 5)
            api_source: Optional specific API to use for all jokes
        
        Returns:
            List of joke dictionaries
        """
        jokes = []
        for _ in range(count):
            joke = JokeGenerator.get_joke(api_source)
            jokes.append(joke)
        return jokes


def main():
    """Main function to demonstrate joke generator"""
    print("=" * 60)
    print("🎭 RANDOM JOKE GENERATOR 🎭")
    print("=" * 60)
    
    # Get a single random joke
    print("\n📝 Single Random Joke:")
    print("-" * 60)
    joke = JokeGenerator.get_joke()
    print(f"Source: {joke.get('source')}")
    print(f"Joke: {joke.get('joke')}")
    
    # Get jokes from each API
    print("\n" + "=" * 60)
    print("🎯 One Joke from Each API:")
    print("=" * 60)
    
    for api_name in JokeGenerator.JOKE_APIS.keys():
        print(f"\n{api_name.upper().replace('_', ' ')}:")
        print("-" * 60)
        joke = JokeGenerator.get_joke(api_name)
        if not joke.get('error'):
            print(f"Joke: {joke.get('joke')}")
        else:
            print(f"Error: {joke.get('joke')}")
    
    # Get multiple jokes
    print("\n" + "=" * 60)
    print("📚 Multiple Random Jokes:")
    print("=" * 60)
    
    jokes = JokeGenerator.get_multiple_jokes(count=3)
    for i, joke in enumerate(jokes, 1):
        print(f"\nJoke {i} ({joke.get('source')}):")
        print(f"  {joke.get('joke')}")


if __name__ == "__main__":
    main()
