import { STATUS_LABEL } from "@/lib/format";
import type { Breakdown as B, Kpi, Status } from "@/lib/types";

const TONE: Record<string, string> = { neutral: "text-ink", done: "text-done", staff: "text-staff", failed: "text-failed" };
const PILL: Record<Status, string> = {
  done: "bg-done/10 text-done",
  needs_staff: "bg-staff/15 text-staff",
  failed: "bg-failed/10 text-failed",
  waiting: "bg-waiting/15 text-waiting",
  transferred: "bg-transferred/10 text-transferred",
};

export function StatusPill({ status }: { status: Status }) {
  return <span className={`inline-block whitespace-nowrap rounded px-2 py-0.5 text-xs font-semibold ${PILL[status] ?? PILL.waiting}`}>{STATUS_LABEL[status] ?? status}</span>;
}

export function KpiRow({ kpis }: { kpis: Kpi[] }) {
  return (
    <dl className="panel grid grid-cols-2 divide-line sm:grid-cols-3 lg:grid-cols-5 lg:divide-x">
      {kpis.map((k) => (
        <div key={k.label} className="px-4 py-3.5">
          <dt className="text-sm text-ink-soft">{k.label}</dt>
          <dd className={`mt-1 text-[28px] font-bold leading-none tracking-tight ${TONE[k.tone]}`}>{k.value}</dd>
          {k.sub && <dd className="mt-1.5 text-xs text-ink-faint">{k.sub}</dd>}
        </div>
      ))}
    </dl>
  );
}

export function Breakdown({ b }: { b: B }) {
  const max = Math.max(1, ...b.items.map((i) => i.value));
  return (
    <section className="panel p-4">
      <h2 className="panel-title">{b.title}</h2>
      {b.items.length === 0 ? (
        <p className="mt-3 text-sm text-ink-faint">Nothing in this period.</p>
      ) : (
        <ul className="mt-3 space-y-2.5">
          {b.items.map((i) => (
            <li key={i.label} className="text-sm">
              <div className="flex justify-between gap-3">
                <span className="min-w-0 text-ink-soft">{i.label}</span>
                <span className="shrink-0 font-semibold">{i.display}</span>
              </div>
              {i.value > 0 && !i.display.includes("★") && !i.display.startsWith("$") && (
                <div className="mt-1 h-1.5 rounded-full bg-mist">
                  <div className="h-1.5 rounded-full bg-teal" style={{ width: `${(i.value / max) * 100}%` }} />
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export function SampleBanner() {
  return (
    <p className="mb-4 rounded-panel border border-staff/40 bg-staff/10 px-4 py-2 text-sm text-staff">
      Sample data, not real patients. Run <code className="font-semibold">python -m app.seed --clear</code> before connecting live agents.
    </p>
  );
}

export function ErrorState({ message }: { message: string }) {
  return (
    <div className="panel max-w-xl p-6">
      <h1 className="text-lg font-semibold">The dashboard has no data to show</h1>
      <p className="mt-2 text-sm text-ink-soft">{message}</p>
    </div>
  );
}

export function PageHeader({ title, children }: { title: string; children?: React.ReactNode }) {
  return (
    <header className="mb-5 flex flex-wrap items-center justify-between gap-3">
      <h1 className="text-2xl font-bold tracking-tight">{title}</h1>
      <div className="flex flex-wrap items-center gap-3">{children}</div>
    </header>
  );
}
