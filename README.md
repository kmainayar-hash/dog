# Dog Influencer Scraper

A web scraper that finds the top 5 most popular dog influencers in all US states and territories.

## Features

- Scrapes social media platforms for dog influencers
- Organizes results by US state and territory
- Returns top 5 influencers per location based on follower count and engagement
- Exports results to JSON format

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python dog_influencer_scraper.py
```

The scraper will collect data and save results to `dog_influencers_by_state.json`.

## Output Format

The output JSON file contains influencers organized by state/territory:

```json
{
  "California": [
    {
      "name": "DogName",
      "handle": "@doghandle",
      "platform": "Instagram",
      "followers": 1000000,
      "engagement_rate": 5.2,
      "url": "https://..."
    }
  ]
}
```

## States and Territories Covered

- All 50 US States
- District of Columbia
- Puerto Rico
- US Virgin Islands
- Guam
- American Samoa
- Northern Mariana Islands

## Requirements

- Python 3.8+
- See requirements.txt for dependencies

## Note

This scraper uses public data only and respects rate limits and robots.txt files.
