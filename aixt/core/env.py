from __future__ import annotations

import datetime as _dt
import os
import random
from typing import Optional

DEFAULT_SEED = 1337


def get_seed() -> int:
    """Return the active seed, defaulting to DEFAULT_SEED."""
    return int(os.getenv("AIXT_SEED", str(DEFAULT_SEED)))


def init_determinism(seed: Optional[int] = None) -> int:
    """Initialize deterministic randomness for this process.

    Sets AIXT_SEED and seeds random (and numpy if available).
    """
    resolved = int(seed if seed is not None else get_seed())
    os.environ["AIXT_SEED"] = str(resolved)
    random.seed(resolved)

    try:
        import numpy as np  # type: ignore

        np.random.seed(resolved)
    except Exception:
        # Numpy is optional; determinism still holds for stdlib random.
        pass

    return resolved


def ensure_run_id(now: Optional[_dt.datetime] = None) -> str:
    """Ensure AIXT_RUN_ID is set and return it.

    Format: YYYYMMDDTHHMMSSZ (UTC).
    """
    run_id = os.getenv("AIXT_RUN_ID")
    if not run_id:
        ts = now or _dt.datetime.utcnow()
        run_id = ts.strftime("%Y%m%dT%H%M%SZ")
        os.environ["AIXT_RUN_ID"] = run_id
    return run_id
