"use client";
import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { agentSlug } from "@/lib/api";

export default function Sidebar({ agents, user }: { agents: { key: string; label: string }[]; user: { email: string; role: string } | null }) {
  const path = usePathname();
  const qs = useSearchParams().toString();
  const keep = qs ? `?${qs}` : "";
  const links = [{ href: "/", label: "Overview" }, ...agents.map((a) => ({ href: `/${agentSlug(a.key)}`, label: a.label }))];
  return (
    <nav className="border-b border-line bg-ink text-white md:sticky md:top-0 md:h-screen md:w-56 md:shrink-0 md:border-b-0 md:border-r">
      <div className="flex items-center justify-between px-5 py-4 md:block">
        <Link href={`/${keep}`} className="block text-lg font-bold tracking-tight">Agent Hub</Link>
        <p className="hidden text-xs text-white/60 md:mt-0.5 md:block">Shifa Dental</p>
      </div>
      <ul className="flex gap-1 overflow-x-auto px-3 pb-3 md:block md:space-y-0.5 md:pb-0">
        {links.map((l) => {
          const active = l.href === "/" ? path === "/" : path.startsWith(l.href);
          return (
            <li key={l.href}>
              <Link
                href={`${l.href}${keep}`}
                aria-current={active ? "page" : undefined}
                className={`block whitespace-nowrap rounded px-3 py-2 text-sm ${active ? "bg-white/15 font-semibold" : "text-white/75 hover:bg-white/10 hover:text-white"}`}
              >
                {l.label}
              </Link>
            </li>
          );
        })}
      </ul>
      {user && (
        <p className="hidden px-5 py-4 text-xs text-white/55 md:absolute md:bottom-0 md:block">
          {user.email}<br />Role: {user.role}
        </p>
      )}
    </nav>
  );
}
