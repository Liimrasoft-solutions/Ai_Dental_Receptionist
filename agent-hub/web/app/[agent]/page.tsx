import { notFound } from "next/navigation";
import { Suspense } from "react";
import { PauseToggle } from "@/components/Actions";
import { Breakdown, ErrorState, KpiRow, PageHeader, SampleBanner } from "@/components/Bits";
import EventTable from "@/components/EventTable";
import Filters from "@/components/Filters";
import LiveRefresh from "@/components/LiveRefresh";
import SeriesChart from "@/components/SeriesChart";
import { ApiError, agentKey, apiGet, filtersFrom } from "@/lib/api";
import type { AgentPage, Meta } from "@/lib/types";

export const dynamic = "force-dynamic";

/** One page for every agent, including ones added later: the API decides what it shows. */
export default async function AgentDetail({ params, searchParams }: {
  params: { agent: string };
  searchParams: Record<string, string | string[] | undefined>;
}) {
  const f = filtersFrom(searchParams);
  let page: AgentPage, meta: Meta;
  try {
    [page, meta] = await Promise.all([apiGet<AgentPage>(`/v1/agents/${agentKey(params.agent)}`, f), apiGet<Meta>("/v1/meta")]);
  } catch (e) {
    if (e instanceof ApiError && e.status === 404) notFound();
    return <ErrorState message={(e as Error).message} />;
  }
  return (
    <>
      <PageHeader title={page.label}>
        <LiveRefresh />
        {page.paused && <span className="rounded bg-waiting/15 px-2 py-1 text-xs font-semibold text-waiting">Paused</span>}
        {meta.user.role !== "staff" && <PauseToggle agent={page.agent} paused={page.paused} label={page.label} />}
        <Suspense><Filters locations={meta.locations} /></Suspense>
      </PageHeader>
      {page.sample_data && <SampleBanner />}
      <div className="space-y-5">
        <KpiRow kpis={page.kpis} />
        <div className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_22rem]">
          <div className="self-start">{page.series && <SeriesChart series={page.series} />}</div>
          <div className="space-y-5">{page.breakdowns.map((b) => <Breakdown key={b.title} b={b} />)}</div>
        </div>
        <EventTable table={page.table} actionLabel={page.action_label} />
      </div>
    </>
  );
}
