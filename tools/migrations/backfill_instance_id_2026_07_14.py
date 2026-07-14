"""Instance-id backfill migration — MC-E2 α condition (Owner ruling 2026-07-14).

Owner ruling verbatim:
    'legacy backfill: existing rows carry no instance_id; the same
     commit backfills all existing data to the instance-#1 identity and
     attests the backfill count, or every live call site breaks on the
     accessor's refusal.'

Run: `python3 -m tools.migrations.backfill_instance_id_2026_07_14`
Post-condition: db.<coll>.count_documents({"instance_id": {"$exists": false}}) == 0
                for every persistent collection.
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

from motor.motor_asyncio import AsyncIOMotorClient

DEFAULT_INSTANCE_ID = "instance_1"


async def run() -> int:
    from dotenv import load_dotenv
    load_dotenv("/app/backend/.env")
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = client[os.environ["DB_NAME"]]
    collections = await db.list_collection_names()
    total_backfilled = 0
    per_collection = {}
    for c in sorted(collections):
        # Skip internal Mongo collections
        if c.startswith("system.") or c.startswith("_"):
            continue
        # Missing-instance-id rows
        missing = await db[c].count_documents({"instance_id": {"$exists": False}})
        if missing > 0:
            result = await db[c].update_many(
                {"instance_id": {"$exists": False}},
                {"$set": {"instance_id": DEFAULT_INSTANCE_ID}},
            )
            per_collection[c] = result.modified_count
            total_backfilled += result.modified_count
        else:
            per_collection[c] = 0

    print("=== Backfill per collection ===")
    for c, n in per_collection.items():
        marker = "backfilled" if n > 0 else "already-scoped"
        print(f"  {c}: {n} ({marker})")
    print(f"Total rows backfilled: {total_backfilled}")

    # Attestation: post-backfill, every collection must have 0 unscoped rows
    print("\n=== Post-backfill attestation ===")
    any_leak = False
    for c in per_collection:
        residual = await db[c].count_documents({"instance_id": {"$exists": False}})
        status = "OK" if residual == 0 else "LEAK"
        if residual > 0:
            any_leak = True
        print(f"  {c}: {residual} unscoped rows ({status})")

    # Create compound indexes on the primary key collections
    print("\n=== Compound-index creation ===")
    index_targets = {
        "northena_ledger": ["run_id"],
        "northena_ledger_rows": ["run_id"],
        "objectives_async_state": ["objective_id"],
        "targeta_mining_plans": ["plan_id"],
        "mtafiti_registry_records": ["source_ref"],
        "engineer_key_grants": ["email"],
        "wizard_sessions": ["session_id"],
        "wizard_session_bindings": ["session_id"],
        "users": ["email"],
        "checker_requests": ["request_id"],
        "engineer_invites": ["invite_code"],
    }
    for coll_name, extra_keys in index_targets.items():
        if coll_name in collections:
            keys = [("instance_id", 1)] + [(k, 1) for k in extra_keys]
            await db[coll_name].create_index(keys, name="instance_id_compound", background=True)
            print(f"  {coll_name}: compound index ({', '.join(k[0] for k in keys)}) ensured")
    client.close()
    return 1 if any_leak else 0


if __name__ == "__main__":
    exit_code = asyncio.run(run())
    sys.exit(exit_code)
