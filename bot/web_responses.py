import json
import requests


def get_encouragement_quote():
      response = requests.get('https://zenquotes.io/api/quotes/')
      json_data = json.loads(response.text)
      discord_response = f"""I have {len(json_data)} different encouragement quotations for you.
A quote by {json_data[0]['a']} has been radomly chosen:
\"{json_data[0]['q']}\""""

      return discord_response