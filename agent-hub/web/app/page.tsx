import Link from "next/link";
import { Suspense } from "react";
import { PauseToggle, ResolveButton } from "@/components/Actions";
import { Breakdown, ErrorState, PageHeader, StatusPill } from "@/components/Bits";
import Filters from "@/components/Filters";
import LiveRefresh from "@/components/LiveRefresh";
import SeriesChart from "@/components/SeriesChart";
import { agentSlug, apiGet, filtersFrom } from "@/lib/api";
import { fmtTime, fmtWhen, usd } from "@/lib/format";
import type { Meta, Overview } from "@/lib/types";

export const dynamic = "force-dynamic";

// Top accent border colors matching the prototype design
const TILE_ACCENT_COLORS: Record<string, string> = {
  receptionist: "border-t-[3px] border-t-[#1D6A73]",     // Deep teal/blue
  verification: "border-t-[3px] border-t-[#D97706]",     // Amber/gold
  marketing: "border-t-[3px] border-t-[#881337]",        // Deep maroon/wine
  health_records: "border-t-[3px] border-t-[#166534]",   // Deep green
};

const AGENT_DOT_COLORS: Record<string, string> = {
  receptionist: "bg-[#2563EB]",
  verification: "bg-[#D97706]",
  marketing: "bg-[#991B1B]",
  health_records: "bg-[#166534]",
};

export default async function OverviewPage({ searchParams }: { searchParams: Record<string, string | string[] | undefined> }) {
  const f = filtersFrom(searchParams);
  let data: Overview, meta: Meta;
  try {
    [data, meta] = await Promise.all([apiGet<Overview>("/v1/overview", f), apiGet<Meta>("/v1/meta")]);
  } catch (e) {
    return <ErrorState message={(e as Error).message} />;
  }

  const qs = new URLSearchParams(Object.entries(f).filter(([, v]) => v) as [string, string][]).toString();
  const budgetPct = Math.min(100, Math.round((100 * data.cost_month) / data.budget));
  const canPause = meta.user.role !== "staff";

  return (
    <>
      {/* Top Header with title, dropdown filters and sample banner pill on top right */}
      <header className="mb-5 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold tracking-tight text-slate-800">Home: Overview</h1>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <LiveRefresh />
          <Suspense><Filters locations={meta.locations} /></Suspense>
          {data.sample_data && (
            <span className="rounded border border-red-300 bg-red-50 px-3 py-1 text-xs font-bold uppercase tracking-wider text-red-600">
              Sample Data, Not Real
            </span>
          )}
        </div>
      </header>

      {/* Row 1: The 4 Distinct Agent KPI Cards with top color accents */}
      <div className="mb-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {data.tiles.map((t) => {
          const accent = TILE_ACCENT_COLORS[t.agent] ?? "border-t-[3px] border-t-slate-400";
          return (
            <Link
              key={t.agent}
              href={`/${agentSlug(t.agent)}${qs ? `?${qs}` : ""}`}
              className={`group rounded-lg border border-line bg-surface p-4 shadow-sm transition hover:shadow-md ${accent}`}
            >
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-500 group-hover:text-teal">{t.label}</p>
              <p className="mt-1.5 text-3xl font-extrabold tracking-tight text-slate-900">{t.kpi.value}</p>
              <p className="mt-1 text-xs text-slate-500">
                {t.kpi.label.toLowerCase()} {t.kpi.sub && `· ${t.kpi.sub}`}
              </p>
            </Link>
          );
        })}
      </div>

      {/* Row 2: Status & Pause Bar for every Agent */}
      <div className="mb-5 flex flex-wrap items-center justify-between gap-4 rounded-lg border border-line bg-surface px-5 py-2.5 shadow-sm">
        {data.tiles.map((t) => (
          <div key={t.agent} className="flex items-center gap-2 text-sm">
            <span className={`h-2.5 w-2.5 rounded-full ${t.paused ? "bg-amber-500" : !t.has_data ? "bg-slate-300" : t.open_items ? "bg-amber-600" : "bg-emerald-600"}`} aria-hidden />
            <span className="font-medium text-slate-700">
              {t.label}: {t.paused ? "Paused" : t.open_items ? "Waiting for approval" : "On"}
            </span>
            {canPause && (
              <div className="ml-1 scale-90">
                <PauseToggle agent={t.agent} paused={t.paused} label={t.label} />
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Row 3: 3-Column Chart & Breakdowns Row */}
      <div className="mb-5 grid gap-5 lg:grid-cols-3">
        {/* Calls per day Bar Chart */}
        <div className="rounded-lg border border-line bg-surface p-4 shadow-sm">
          <h2 className="text-sm font-bold text-slate-800">Calls per day</h2>
          <div className="mt-2">
            {data.calls ? (
              <SeriesChart series={data.calls} />
            ) : (
              <p className="py-12 text-center text-sm text-slate-400">No calls recorded in this period.</p>
            )}
          </div>
        </div>

        {/* Insurance checks Bar Breakdown */}
        <div className="rounded-lg border border-line bg-surface p-4 shadow-sm">
          {data.side_breakdowns[0] ? (
            <Breakdown b={data.side_breakdowns[0]} />
          ) : (
            <p className="py-12 text-center text-sm text-slate-400">No insurance data available.</p>
          )}
        </div>

        {/* Leads by source Bar Breakdown */}
        <div className="rounded-lg border border-line bg-surface p-4 shadow-sm">
          {data.side_breakdowns[1] ? (
            <Breakdown b={data.side_breakdowns[1]} />
          ) : (
            <p className="py-12 text-center text-sm text-slate-400">No marketing data available.</p>
          )}
        </div>
      </div>

      {/* Row 4: Bottom Row (Needs a Person on Left, Alerts & Cost on Right) */}
      <div className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_22rem]">
        {/* Needs a person (latest first) */}
        <section className="rounded-lg border border-line bg-surface p-5 shadow-sm">
          <div className="flex items-baseline justify-between border-b border-line pb-3">
            <div>
              <h2 className="text-base font-bold text-slate-800">Needs a person (latest first)</h2>
              <p className="text-xs text-slate-400">Items requiring human staff attention or live handoff</p>
            </div>
            <span className="text-xs font-semibold text-slate-400">{data.needs_person.length} open</span>
          </div>

          {data.needs_person.length === 0 ? (
            <p className="py-8 text-center text-sm text-emerald-600">✓ All clear. Every agent is operating smoothly.</p>
          ) : (
            <ul className="divide-y divide-slate-100">
              {data.needs_person.map((n) => {
                const dot = AGENT_DOT_COLORS[n.agent] ?? "bg-slate-400";
                return (
                  <li key={n.id} className="flex flex-wrap items-center justify-between gap-3 py-3">
                    <div className="flex items-center gap-3">
                      <time className="w-12 text-xs font-bold text-slate-500" dateTime={n.when} title={fmtWhen(n.when)}>
                        {fmtTime(n.when)}
                      </time>
                      <div className="flex items-center gap-2">
                        <span className={`h-2.5 w-2.5 rounded-full ${dot}`} />
                        <span className="text-xs font-semibold text-slate-700">{n.agent_label}</span>
                      </div>
                      <p className="text-sm font-medium text-slate-800">{n.summary}</p>
                    </div>

                    <div className="flex items-center gap-2">
                      <StatusPill status={n.status} />
                      {n.status === "needs_staff" && (
                        <ResolveButton id={n.id} label={n.action_label} />
                      )}
                    </div>
                  </li>
                );
              })}
            </ul>
          )}
        </section>

        {/* Alerts and cost */}
        <section id="alerts" className="rounded-lg border border-line bg-surface p-5 shadow-sm">
          <h2 className="text-base font-bold text-slate-800">Alerts and cost</h2>
          <div className="mt-3">
            {data.alerts.length === 0 ? (
              <p className="text-xs text-slate-400">No active alerts.</p>
            ) : (
              <ul className="space-y-3">
                {data.alerts.map((a) => {
                  const borderCol = a.level === "warning" ? "border-amber-600" : "border-red-600";
                  return (
                    <li key={a.id} className={`flex items-center justify-between gap-2 border-l-4 ${borderCol} pl-2.5 text-xs text-slate-700`}>
                      <span>{a.summary}</span>
                      <ResolveButton id={a.id} label="Clear" />
                    </li>
                  );
                })}
              </ul>
            )}
          </div>

          <div className="mt-6 border-t border-slate-100 pt-4">
            <div className="flex justify-between text-xs font-semibold">
              <span className="text-slate-600">Cost this month</span>
              <span className="text-slate-900">{usd(data.cost_month)} of {usd(data.budget)}</span>
            </div>
            <div className="mt-2 h-2.5 rounded-full bg-slate-100" role="progressbar">
              <div
                className={`h-2.5 rounded-full ${budgetPct >= 90 ? "bg-red-500" : budgetPct >= 75 ? "bg-amber-500" : "bg-slate-700"}`}
                style={{ width: `${budgetPct}%` }}
              />
            </div>
          </div>
        </section>
      </div>
    </>
  );
}
