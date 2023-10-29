import React from "react";
interface ProductGroupProps {
  type: "full" | "standard" | "small" | "carousel" | "multicolour";
}

export function ProductGroup({ type }: ProductGroupProps) {
  return <>{type}</>;
}
