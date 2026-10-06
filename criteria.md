# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

# Acceptance Criteria

**1. Given a query that matches at least one listing, the agent completes all three tool calls and returns a fit card — in at least 4 of 5 tries.**
*Why this target:* I picked 4 of 5 because generating outfit suggestions and fit cards relies on an LLM, which can occasionally timeout or refuse a prompt, but the happy path should succeed the vast majority of the time.

**2. Given a query that matches no listings, the agent stops before calling suggest_outfit and returns a message naming what to change — 5 of 5 tries.**
*Why this target:* I picked 5 of 5 because this branch relies purely on a deterministic Python list check (`if not results:`). It does not rely on the LLM to decide when to stop, so it should never fail.

**3. State Integrity: When a matching item is found, the item ID received as an input by `suggest_outfit` exactly matches the item ID returned by `search_listings` in 5 of 5 tries.**
*Why this target:* I picked 5 of 5 because passing state between tools is a mechanical variable assignment in the planning loop. If the agent hallucinates a different item ID, the state logic is fundamentally broken, which shouldn't happen even once.

**4. Fit Card Variation: Given the exact same item and outfit suggestion (with caching disabled), the `create_fit_card` tool generates a fit card with a different opening sentence in at least 4 of 5 tries.**
*Why this target:* I picked 4 of 5 because `config.py` sets a temperature > 0 to encourage variation. However, there is a small chance the model naturally repeats a similar catchy opening hook by random chance, so demanding 5 of 5 could cause false failures.

**5. Empty Wardrobe Handling: When the agent is run against an empty wardrobe, the outfit suggestion explicitly provides standalone styling advice without hallucinating wardrobe pieces in 5 of 5 tries.**
*Why this target:* I picked 5 of 5 because an empty wardrobe is a strict data constraint. The model must consistently ground its response in the provided tools and data rather than making up items the user does not own.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
