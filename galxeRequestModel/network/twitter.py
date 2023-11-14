import requests

from network.network_helper import NetworkHelper
from loguru import logger


class Twitter(NetworkHelper):

    def __init__(self, index, auth_token, csrf, proxy):
        self.index = index

        self.session = NetworkHelper._make_scraper()
        self.session.proxies = proxy
        self.session.user_agent = NetworkHelper.random_user_agent()

        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        authorization_token = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

        self.csrf = csrf
        self.auth_token = auth_token
        self.cookie = f'auth_token={self.auth_token}; ct0={self.csrf}'

        liketweet_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {authorization_token}',
            'x-csrf-token': self.csrf,
            'cookie': self.cookie
        }

        self.session.headers.update(liketweet_headers)

    def tweet(self, text):

        payload = {"variables": {
            "tweet_text": text,
            "dark_request": False,
            "media": {
                "media_entities": [],
                "possibly_sensitive": False
            },
            "withDownvotePerspective": False,
            "withReactionsMetadata": False,
            "withReactionsPerspective": False,
            "withSuperFollowsTweetFields": True,
            "withSuperFollowsUserFields": True,
            "semantic_annotation_ids": []
        }, "features": {
            "tweetypie_unmention_optimization_enabled": True,
            "vibe_api_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "interactive_text_enabled": True,
            "responsive_web_text_conversations_enabled": False,
            "responsive_web_twitter_blue_verified_badge_is_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": False,
            "verified_phone_label_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": False,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_enhance_cards_enabled": False
        },
            "queryId": "Tz_cZL9zkkY2806vRiQP0Q"
        }

        try:
            with self.session.post("https://api.twitter.com/graphql/Tz_cZL9zkkY2806vRiQP0Q/CreateTweet", json=payload, timeout=30) as response:
                if response.ok:
                    logger.success(f'{self.index}: tweet successful')
                    return response.json()['data']['create_tweet']['tweet_results']['result']['rest_id']
                else:
                    logger.error(f'{self.index}: tweet failed')
        except:
            logger.error(f'{self.index}: tweet failed')
