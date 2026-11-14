"use client";
import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { agentSlug } from "@/lib/api";

const AGENT_DOT_COLORS: Record<string, string> = {
  receptionist: "bg-[#2563EB]", // Blue dot
  verification: "bg-[#D97706]", // Orange/amber dot
  marketing: "bg-[#991B1B]",    // Maroon/red dot
  health_records: "bg-[#166534]", // Forest green dot
};

export default function Sidebar({ agents, user }: { agents: { key: string; label: string }[]; user: { email: string; role: string } | null }) {
  const path = usePathname();
  const qs = useSearchParams().toString();
  const keep = qs ? `?${qs}` : "";

  return (
    <nav className="border-b border-line bg-[#1E293B] text-white md:sticky md:top-0 md:h-screen md:w-56 md:shrink-0 md:border-b-0 md:border-r">
      <div className="flex items-center justify-between px-5 py-4 md:block">
        <Link href={`/${keep}`} className="block text-lg font-bold tracking-tight text-white hover:text-teal">
          Limra Dental AI
        </Link>
        <p className="hidden text-xs text-white/60 md:mt-0.5 md:block">Shifa Dental · Plano & Garland</p>
      </div>

      <div className="px-3 pb-3 md:pb-0">
        {/* Main Navigation Links */}
        <ul className="flex gap-1 overflow-x-auto md:block md:space-y-1">
          <li>
            <Link
              href={`/${keep}`}
              aria-current={path === "/" ? "page" : undefined}
              className={`block whitespace-nowrap rounded px-3 py-2 text-sm ${path === "/" ? "bg-[#334155] font-semibold text-white" : "text-slate-300 hover:bg-slate-700/50 hover:text-white"}`}
            >
              Overview
            </Link>
          </li>

          {agents.map((a) => {
            const href = `/${agentSlug(a.key)}`;
            const active = path.startsWith(href);
            const dotColor = AGENT_DOT_COLORS[a.key] ?? "bg-slate-400";
            return (
              <li key={a.key}>
                <Link
                  href={`${href}${keep}`}
                  aria-current={active ? "page" : undefined}
                  className={`flex items-center gap-2.5 whitespace-nowrap rounded px-3 py-2 text-sm ${active ? "bg-[#334155] font-semibold text-white" : "text-slate-300 hover:bg-slate-700/50 hover:text-white"}`}
                >
                  <span className={`h-2.5 w-2.5 rounded-full ${dotColor}`} aria-hidden />
                  <span>{a.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>

        {/* Static Auxiliary Links matching prototype image */}
        <div className="mt-6 hidden border-t border-slate-700/60 pt-4 md:block">
          <ul className="space-y-1">
            <li>
              <Link href={`/#alerts`} className="block rounded px-3 py-2 text-sm text-slate-300 hover:bg-slate-700/50 hover:text-white">
                Alerts
              </Link>
            </li>
            <li>
              <span className="block cursor-not-allowed rounded px-3 py-2 text-sm text-slate-400 opacity-60">
                Settings
              </span>
            </li>
            <li>
              <span className="block cursor-not-allowed rounded px-3 py-2 text-sm text-slate-400 opacity-60">
                Users
              </span>
            </li>
          </ul>
        </div>
      </div>

      {user && (
        <p className="hidden px-5 py-4 text-xs text-slate-400 md:absolute md:bottom-0 md:block">
          {user.email}<br />Role: {user.role}
        </p>
      )}
    </nav>
  );
}
