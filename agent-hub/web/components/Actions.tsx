"use client";
import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import { apiPost } from "@/lib/api";

export function ResolveButton({ id, label }: { id: number; label: string }) {
  const router = useRouter();
  const [busy, start] = useTransition();
  const [err, setErr] = useState("");
  return (
    <span className="inline-flex flex-col items-end">
      <button
        className="btn btn-primary"
        disabled={busy}
        onClick={() => start(async () => {
          try { await apiPost(`/v1/events/${id}/resolve`, {}); router.refresh(); }
          catch (e) { setErr((e as Error).message); }
        })}
      >
        {busy ? "Saving…" : label}
      </button>
      {err && <span className="mt-1 text-xs text-failed">{err}</span>}
    </span>
  );
}

export function PauseToggle({ agent, paused, label }: { agent: string; paused: boolean; label: string }) {
  const router = useRouter();
  const [busy, start] = useTransition();
  const [err, setErr] = useState("");
  return (
    <span className="inline-flex items-center gap-2">
      <button
        className="btn"
        disabled={busy}
        aria-pressed={paused}
        aria-label={`${paused ? "Resume" : "Pause"} ${label}`}
        onClick={() => start(async () => {
          try { await apiPost(`/v1/agents/${agent}/pause`, { paused: !paused }); router.refresh(); }
          catch (e) { setErr((e as Error).message); }
        })}
      >
        {paused ? "Resume" : "Pause"}
      </button>
      {err && <span className="text-xs text-failed">{err}</span>}
    </span>
  );
}
