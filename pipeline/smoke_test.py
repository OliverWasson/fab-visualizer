"""Smoke test: build a Si slab with an oxide-filled trench, export as glTF.

Conventions: units are nanometers, +z points up out of the wafer.
glTF/three.js use +y up, so we rotate once at export.
"""
from pathlib import Path

import numpy as np
import trimesh
from manifold3d import Manifold

# Dimensions in nm (illustrative only, not real process geometry yet)
W, D, H = 280.0, 120.0, 80.0          # slab width (x), depth (y), thickness (z)
TRENCH_W, TRENCH_DEPTH = 40.0, 40.0   # trench width and depth

OUT = Path(__file__).resolve().parents[1] / "web/public/models/smoke_test.glb"


def box(x0, y0, z0, x1, y1, z1) -> Manifold:
    """Axis-aligned box from min corner to max corner."""
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def to_trimesh(m: Manifold, rgba) -> trimesh.Trimesh:
    """Convert a manifold3d solid into a colored trimesh mesh."""
    mesh = m.to_mesh()
    tm = trimesh.Trimesh(
        vertices=np.asarray(mesh.vert_properties)[:, :3],
        faces=np.asarray(mesh.tri_verts),
    )
    material = trimesh.visual.material.PBRMaterial(
        baseColorFactor=rgba, metallicFactor=0.0, roughnessFactor=0.6
    )
    tm.visual = trimesh.visual.TextureVisuals(material=material)
    return tm


# Silicon slab, top surface at z = 0
substrate = box(-W / 2, -D / 2, -H, W / 2, D / 2, 0)

# Trench cutter: slightly oversized in y and z so the boolean cuts cleanly
cutter = box(-TRENCH_W / 2, -D / 2 - 1, -TRENCH_DEPTH, TRENCH_W / 2, D / 2 + 1, 1)
silicon = substrate - cutter

# Oxide fill exactly occupying the trench
oxide = box(-TRENCH_W / 2, -D / 2, -TRENCH_DEPTH, TRENCH_W / 2, D / 2, 0)

scene = trimesh.Scene()
scene.add_geometry(to_trimesh(silicon, [150, 150, 165, 255]), node_name="silicon")
scene.add_geometry(to_trimesh(oxide, [90, 140, 220, 255]), node_name="sti_oxide")

# Convert z-up (our convention) to y-up (glTF convention)
scene.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]))

OUT.parent.mkdir(parents=True, exist_ok=True)
scene.export(OUT)
print(f"wrote {OUT}")