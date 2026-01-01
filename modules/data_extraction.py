import time
import requests
import logging
from typing import Dict, Optional, Any
import config

logger = logging.getLogger(__name__)

def extract_linkedin_profile(
    linkedin_profile_url: str,
    api_key: Optional[str] = None,
    mock: bool = False
) -> Dict[str, Any]:

    start_time = time.time()

    try:
        if mock:
            logger.info("Using mock LinkedIn data")
            response = requests.get(config.MOCK_DATA_URL, timeout=30)
        else:
            if not api_key:
                raise ValueError("ProxyCurl API key required")

            headers = {"Authorization": f"Bearer {api_key}"}
            params = {
                "url": linkedin_profile_url,
                "fallback_to_cache": "on-error",
                "use_cache": "if-present",
                "skills": "include",
                "inferred_salary": "include",
            }

            response = requests.get(
                "https://nubela.co/proxycurl/api/v2/linkedin",
                headers=headers,
                params=params,
                timeout=30,
            )

        logger.info(f"Response received in {time.time() - start_time:.2f}s")

        if response.status_code != 200:
            logger.error(response.text)
            return {}

        data = response.json()
        return {
            k: v
            for k, v in data.items()
            if v not in (None, "", [])
        }

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return {}
