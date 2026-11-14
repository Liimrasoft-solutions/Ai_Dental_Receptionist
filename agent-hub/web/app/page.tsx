import Link from "next/link";
import { Suspense } from "react";
import { PauseToggle, ResolveButton } from "@/components/Actions";
import { Breakdown, ErrorState, PageHeader, SampleBanner, StatusPill } from "@/components/Bits";
import Filters from "@/components/Filters";
import LiveRefresh from "@/components/LiveRefresh";
import SeriesChart from "@/components/SeriesChart";
import { agentSlug, apiGet, filtersFrom } from "@/lib/api";
import { fmtTime, fmtWhen, usd } from "@/lib/format";
import type { Meta, Overview } from "@/lib/types";

export const dynamic = "force-dynamic";

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
      <PageHeader title="Overview">
        <LiveRefresh />
        <Suspense><Filters locations={meta.locations} /></Suspense>
      </PageHeader>
      {data.sample_data && <SampleBanner />}

      {/* Is everything working? */}
      <ul className="panel mb-5 grid divide-y divide-line sm:grid-cols-2 sm:divide-y-0 lg:grid-cols-4 lg:divide-x" aria-label="Agent status">
        {data.tiles.map((t) => (
          <li key={t.agent} className="flex items-center justify-between gap-2 px-4 py-2.5 text-sm">
            <span className="flex items-center gap-2">
              <span className={`h-2.5 w-2.5 rounded-full ${t.paused ? "bg-waiting" : !t.has_data ? "bg-line" : t.open_items ? "bg-staff" : "bg-done"}`} aria-hidden />
              <span className="font-medium">{t.label}</span>
              <span className="text-ink-faint">{t.paused ? "Paused" : !t.has_data ? "No reports yet" : "On"}</span>
            </span>
            {canPause && <PauseToggle agent={t.agent} paused={t.paused} label={t.label} />}
          </li>
        ))}
      </ul>

      <div className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_24rem]">
        <div className="space-y-5">
          {/* What did the agents do? */}
          <div className="grid gap-px overflow-hidden rounded-panel border border-line bg-line sm:grid-cols-2 lg:grid-cols-4">
            {data.tiles.map((t) => (
              <Link key={t.agent} href={`/${agentSlug(t.agent)}${qs ? `?${qs}` : ""}`} className="group bg-surface p-4 hover:bg-paper">
                <p className="text-sm font-medium text-ink-soft group-hover:text-teal">{t.label}</p>
                <p className="mt-2 text-[34px] font-bold leading-none tracking-tight">{t.kpi.value}</p>
                <p className="mt-1.5 text-sm text-ink-soft">{t.kpi.label.toLowerCase()}</p>
                {t.second && <p className="text-xs text-ink-faint">{t.second.label}: {t.second.value}</p>}
              </Link>
            ))}
          </div>
          {data.calls && <SeriesChart series={data.calls} />}
          <div className="grid gap-5 md:grid-cols-2">
            {data.side_breakdowns.filter(Boolean).map((b) => <Breakdown key={b!.title} b={b!} />)}
          </div>
        </div>

        {/* What needs a person? Styled as the front-desk sheet: time on the left, one line per item. */}
        <aside className="space-y-5">
          <section className="panel border-l-4 border-l-staff">
            <h2 className="panel-title px-4 pt-4">Needs a person</h2>
            <p className="px-4 text-xs text-ink-faint">Latest first. Clear an item once someone has handled it.</p>
            {data.needs_person.length === 0 ? (
              <p className="p-4 text-sm text-done">Nothing waiting. Every agent is handling its own work.</p>
            ) : (
              <ol className="mt-3 divide-y divide-mist">
                {data.needs_person.map((n) => (
                  <li key={n.id} className="grid grid-cols-[4.25rem_1fr] gap-x-3 px-4 py-3">
                    <time className="pt-0.5 text-sm font-semibold" dateTime={n.when} title={fmtWhen(n.when)}>{fmtTime(n.when)}</time>
                    <div className="min-w-0">
                      <p className="text-sm">{n.summary}</p>
                      <div className="mt-1.5 flex flex-wrap items-center gap-2 text-xs text-ink-faint">
                        <span>{n.agent_label}</span>
                        {n.location_id && <span className="capitalize">{n.location_id}</span>}
                        <StatusPill status={n.status} />
                      </div>
                      {n.status === "needs_staff" && <div className="mt-2"><ResolveButton id={n.id} label={n.action_label} /></div>}
                    </div>
                  </li>
                ))}
              </ol>
            )}
          </section>

          <section className="panel p-4">
            <h2 className="panel-title">Alerts</h2>
            {data.alerts.length === 0 ? (
              <p className="mt-2 text-sm text-ink-faint">No open alerts.</p>
            ) : (
              <ul className="mt-2 space-y-2">
                {data.alerts.map((a) => (
                  <li key={a.id} className="flex items-start justify-between gap-3 text-sm">
                    <span className={a.level === "warning" ? "text-staff" : "text-ink-soft"}>{a.summary}</span>
                    <ResolveButton id={a.id} label="Clear" />
                  </li>
                ))}
              </ul>
            )}
            <div className="mt-4 border-t border-mist pt-3">
              <div className="flex justify-between text-sm">
                <span className="text-ink-soft">Cost this month</span>
                <span className="font-semibold">{usd(data.cost_month)} of {usd(data.budget)}</span>
              </div>
              <div className="mt-2 h-2 rounded-full bg-mist" role="progressbar" aria-valuenow={budgetPct} aria-valuemin={0} aria-valuemax={100} aria-label="Share of monthly budget used">
                <div className={`h-2 rounded-full ${budgetPct >= 90 ? "bg-failed" : budgetPct >= 75 ? "bg-staff" : "bg-teal"}`} style={{ width: `${budgetPct}%` }} />
              </div>
            </div>
          </section>
        </aside>
      </div>
    </>
  );
}
