"use client";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

const RANGES = [["1", "Today"], ["7", "Last 7 days"], ["30", "Last 30 days"], ["90", "Last 90 days"]];

export default function Filters({ locations }: { locations: { id: string; name: string }[] }) {
  const router = useRouter();
  const path = usePathname();
  const sp = useSearchParams();
  const set = (k: string, v: string) => {
    const next = new URLSearchParams(sp);
    if (v) next.set(k, v); else next.delete(k);
    router.push(`${path}?${next}`);
  };
  const sel = "rounded border border-line bg-surface px-2.5 py-1.5 text-sm";
  return (
    <div className="flex flex-wrap gap-2">
      <label className="sr-only" htmlFor="loc">Office</label>
      <select id="loc" className={sel} value={sp.get("location") ?? ""} onChange={(e) => set("location", e.target.value)}>
        <option value="">{locations.map((l) => l.name).join(" + ") || "All offices"}</option>
        {locations.map((l) => <option key={l.id} value={l.id}>{l.name}</option>)}
      </select>
      <label className="sr-only" htmlFor="days">Date range</label>
      <select id="days" className={sel} value={sp.get("days") ?? "30"} onChange={(e) => set("days", e.target.value)}>
        {RANGES.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
      </select>
    </div>
  );
}
