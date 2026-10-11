"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


import re
import config
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    listings = load_listings()
    filtered = []

    for item in listings:
        # 1. Filter by max_price
        if max_price is not None and item.get("price", 0) > max_price:
            continue
        
        # 2. Filter by size
        if size is not None:
            item_size = str(item.get("size", "")).lower()
            target_size = size.lower()
            item_tokens = re.findall(r'[a-z0-9]+', item_size)
            
            match_found = False
            if len(target_size) > 1:
                if target_size in item_size:
                    match_found = True
            else:
                if target_size in item_tokens:
                    match_found = True
            if not match_found:
                continue

        # 3. Score by keyword overlap with description
        desc_tokens = set(re.findall(r'[a-z0-9]+', description.lower()))
        if not desc_tokens:
            score = 1
        else:
            searchable_text = f"{item.get('title', '')} {item.get('description', '')} {' '.join(item.get('style_tags', []))} {item.get('category', '')} {' '.join(item.get('colors', []))}".lower()
            searchable_tokens = set(re.findall(r'[a-z0-9]+', searchable_text))
            overlap = desc_tokens.intersection(searchable_tokens)
            score = len(overlap)

        if score > 0:
            filtered.append((score, item))

    # 4. Sort by score descending, price ascending as tie-breaker
    filtered.sort(key=lambda x: (-x[0], x[1].get("price", 0)))
    results = [item for score, item in filtered]
    return results[:config.SEARCH_RESULT_LIMIT]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    items = wardrobe.get("items", [])
    
    if not items:
        prompt = (
            f"The user is considering buying this thrifted item:\n"
            f"Title: {new_item.get('title')}\n"
            f"Description: {new_item.get('description')}\n"
            f"Category: {new_item.get('category')}\n"
            f"Colors: {new_item.get('colors')}\n"
            f"Style Tags: {new_item.get('style_tags')}\n\n"
            f"The user's wardrobe is currently empty. Provide helpful general styling and outfit ideas "
            f"on how to wear this piece with basic wardrobe staples."
        )
    else:
        wardrobe_str = "\n".join(
            f"- {w.get('name')} (Category: {w.get('category')}, Colors: {w.get('colors')}, Tags: {w.get('style_tags')})"
            for w in items
        )
        prompt = (
            f"The user is considering buying this thrifted item:\n"
            f"Title: {new_item.get('title')}\n"
            f"Description: {new_item.get('description')}\n"
            f"Category: {new_item.get('category')}\n"
            f"Colors: {new_item.get('colors')}\n"
            f"Style Tags: {new_item.get('style_tags')}\n\n"
            f"Here are the items currently in the user's wardrobe:\n{wardrobe_str}\n\n"
            f"Suggest 1-2 specific outfit combinations pairing the new item with items from the user's wardrobe."
        )
    
    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    if not outfit or not outfit.strip():
        return f"Found this great {new_item.get('title', 'item')} for ${new_item.get('price', 0):.2f} on {new_item.get('platform', 'thrift')}!"
    
    prompt = (
        f"Write a short, engaging 2-4 sentence social media caption (fit card) for a thrifted find.\n"
        f"Item: {new_item.get('title')}\n"
        f"Price: ${new_item.get('price')}\n"
        f"Platform: {new_item.get('platform')}\n"
        f"Outfit Suggestion: {outfit}\n\n"
        f"Requirements:\n"
        f"- Read like a real social media post.\n"
        f"- Mention the item, its price, and its platform once each.\n"
        f"- Be specific about the vibe."
    )
    
    return generate(prompt)