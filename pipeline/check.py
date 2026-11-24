"""Run every project check. CI runs this; run it yourself before committing.

Usage (from the repo root):
    python -m pipeline.check            # errors fail, warnings print
    python -m pipeline.check --strict   # warnings fail too
"""

from __future__ import annotations

import argparse
import sys

from pipeline import gen_materials_ts, mask_check, materials, spec_check


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--strict", action="store_true", help="treat warnings as errors"
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    try:
        palette = materials.load()
    except materials.PaletteError as e:
        errors += [f"palette: {line}" for line in str(e).splitlines()]
    else:
        e, w = materials.check_contrast(palette)
        errors += [f"palette: {x}" for x in e]
        warnings += [f"palette: {x}" for x in w]
        out = gen_materials_ts.OUT_PATH
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != gen_materials_ts.render(palette):
            errors.append(
                "palette: web/src/generated/materials.ts is stale; "
                "run `python -m pipeline.gen_materials_ts`"
            )

    e, w = spec_check.check_steps()
    errors += [f"steps: {x}" for x in e]
    warnings += [f"steps: {x}" for x in w]

    e, w = mask_check.check_masks()
    errors += [f"masks: {x}" for x in e]
    warnings += [f"masks: {x}" for x in w]

    for w in warnings:
        print(f"warning  {w}")
    for e in errors:
        print(f"ERROR    {e}")
    failed = bool(errors) or (args.strict and bool(warnings))
    print(
        f"\n{len(errors)} error(s), {len(warnings)} warning(s): {'FAIL' if failed else 'OK'}"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
