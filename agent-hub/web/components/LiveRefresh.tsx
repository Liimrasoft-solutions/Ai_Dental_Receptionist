"use client";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { PUBLIC_API } from "@/lib/api";

/** Re-renders the page when an agent reports something new. */
export default function LiveRefresh() {
  const router = useRouter();
  const [live, setLive] = useState(false);
  const timer = useRef<ReturnType<typeof setTimeout>>();
  useEffect(() => {
    const es = new EventSource(`${PUBLIC_API}/v1/stream`);
    es.onopen = () => setLive(true);
    es.onerror = () => setLive(false);
    es.onmessage = () => {
      clearTimeout(timer.current);
      timer.current = setTimeout(() => router.refresh(), 800);
    };
    return () => { es.close(); clearTimeout(timer.current); };
  }, [router]);
  return (
    <span className="inline-flex items-center gap-1.5 text-xs text-ink-soft" title={live ? "New activity appears on its own" : "Not receiving live updates"}>
      <span className={`h-2 w-2 rounded-full ${live ? "bg-done" : "bg-waiting"}`} />
      {live ? "Live" : "Offline"}
    </span>
  );
}
