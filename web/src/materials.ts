import { MATERIALS, type MaterialId, type MaterialSpec } from "./generated/materials";

export * from "./generated/materials";

const SUFFIX = /__(added|removed)$/;

function isMaterialId(name: string): name is MaterialId {
  return Object.prototype.hasOwnProperty.call(MATERIALS, name);
}

/** Map a glTF node name (e.g. "nitride__added") to its palette material, per CONVENTIONS.md. */
export function materialForNode(nodeName: string): MaterialSpec | null {
  const base = nodeName.replace(SUFFIX, "");
  return isMaterialId(base) ? MATERIALS[base] : null;
}
