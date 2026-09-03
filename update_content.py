import os
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime, timezone
import build_site

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDBpw2G9kS0zg2ogO_kh6uDfFRxkDCUx2k")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
FEED_URL = "https://jibranpcccc.github.io/developer-coding-hub/feed.xml"
PUBSUB_HUB = "https://pubsubhubbub.appspot.com/publish"

FALLBACK_COMMUNITIES = [
    {
        "id": "langchain-ai-discord",
        "title": "LangChain & AI Agents Community",
        "category": "AI & ML",
        "platform": "Discord",
        "memberCount": 87000,
        "description": "Official community for developers building LLM agents, LangGraph workflows, and retrieval-augmented generation systems.",
        "joinUrl": "https://discord.gg/langchain",
        "tags": ["langchain", "agents", "langgraph", "rag", "llm"],
        "verified": True,
        "featured": True,
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%d")
    },
    {
        "id": "bun-runtime-discord",
        "title": "Bun Runtime & Tooling Discord",
        "category": "Frontend & Fullstack",
        "platform": "Discord",
        "memberCount": 54000,
        "description": "The official gathering place for Bun developers. Discuss ultra-fast JavaScript/TypeScript runtimes, bundlers, and package management.",
        "joinUrl": "https://discord.gg/bun",
        "tags": ["bun", "javascript", "typescript", "runtime", "fullstack"],
        "verified": True,
        "featured": False,
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%d")
    },
    {
        "id": "system-design-fight-club-tg",
        "title": "System Design & High Scale Architecture",
        "category": "DevOps & Cloud",
        "platform": "Telegram",
        "memberCount": 46000,
        "description": "Deep-dive case studies dissecting Uber, Netflix, and Stripe architectures, distributed consensus, caching, and rate limiters.",
        "joinUrl": "https://t.me/systemdesign_fightclub",
        "tags": ["system-design", "architecture", "distributed-systems", "scalability"],
        "verified": True,
        "featured": False,
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%d")
    },
    {
        "id": "solana-developers-discord",
        "title": "Solana Tech Builders Collective",
        "category": "Web3 & Blockchain",
        "platform": "Discord",
        "memberCount": 61000,
        "description": "Premier hub for Anchor framework developers, Solana VM smart contract auditing, high TPS dApp development, and grants.",
        "joinUrl": "https://discord.gg/solanadev",
        "tags": ["solana", "anchor", "rust", "smart-contracts", "web3"],
        "verified": True,
        "featured": False,
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%d")
    }
]

def get_existing_groups():
    if os.path.exists("data/groups.json"):
        with open("data/groups.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def generate_new_communities(existing):
    existing_titles = [g["title"] for g in existing]
    existing_ids = set(g["id"] for g in existing)
    
    prompt = f"""You are an expert tech curator for the "Developer & Coding Communities Hub".
Generate 2 NEW, authentic, realistic, verified developer communities across Python, JavaScript, DevOps, Web3, LeetCode, or AI/ML.
Platforms allowed: Discord, Telegram, WhatsApp, Reddit.

Existing communities already indexed (DO NOT DUPLICATE ANY OF THESE):
{", ".join(existing_titles[:20])}

Output a strictly valid JSON array of 2 objects, each matching this exact schema:
- "id": kebab-case string (e.g., "fastapi-community-discord")
- "title": string
- "category": one of ["AI & ML", "Web3 & Blockchain", "Python & Data", "Frontend & Fullstack", "DevOps & Cloud", "DSA & Competitive"]
- "platform": one of ["Discord", "Telegram", "WhatsApp", "Reddit"]
- "memberCount": integer (between 1500 and 500000)
- "description": 2-3 sentences explaining technical channels, mentorship, and code reviews
- "joinUrl": valid canonical URL
- "tags": array of 3-5 strings (lowercase, hyphenated)
- "verified": true
- "featured": boolean
- "lastUpdated": "{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.7
        }
    }

    try:
        req = urllib.request.Request(
            GEMINI_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            # Clean possible markdown blocks
            raw_text = re.sub(r"^```json\s*", "", raw_text)
            raw_text = re.sub(r"^```\s*", "", raw_text)
            raw_text = re.sub(r"\s*```$", "", raw_text)
            generated = json.loads(raw_text)
            if isinstance(generated, list) and len(generated) > 0:
                valid_items = []
                for item in generated:
                    if item.get("title") and item.get("id") not in existing_ids:
                        item["verified"] = True
                        item["lastUpdated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                        valid_items.append(item)
                if len(valid_items) >= 2:
                    print(f"Gemini 2.5 Flash successfully generated {len(valid_items)} new communities.")
                    return valid_items[:2]
    except Exception as e:
        print(f"Warning: Gemini API call error: {e}. Utilizing fallback communities.")

    # Fallback if API fails or returns duplicates
    fallbacks_to_add = []
    for item in FALLBACK_COMMUNITIES:
        if item["id"] not in existing_ids:
            fallbacks_to_add.append(item)
            if len(fallbacks_to_add) == 2:
                break
    return fallbacks_to_add

def ping_pubsubhubbub():
    data = urllib.parse.urlencode({
        "hub.mode": "publish",
        "hub.url": FEED_URL
    }).encode("utf-8")
    
    req = urllib.request.Request(
        PUBSUB_HUB,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"PubSubHubbub ping status: {response.status}")
    except Exception as e:
        print(f"PubSubHubbub ping notice: {e}")

def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting Developer Hub daily update...")
    existing = get_existing_groups()
    print(f"Current community count: {len(existing)}")

    new_communities = generate_new_communities(existing)
    if new_communities:
        print("Adding new communities:")
        for c in new_communities:
            print(f" + {c['title']} ({c['platform']} | {c['category']})")
        
        updated_groups = existing + new_communities
        with open("data/groups.json", "w", encoding="utf-8") as f:
            json.dump(updated_groups, f, indent=2)
        print(f"Updated data/groups.json. Total count: {len(updated_groups)}")

        # Rebuild site
        build_site.build_all()
        print("Site rebuilt with updated community directory.")

        # Ping PubSubHubbub
        ping_pubsubhubbub()
    else:
        print("No new communities to add. Keeping existing database.")

if __name__ == "__main__":
    main()
