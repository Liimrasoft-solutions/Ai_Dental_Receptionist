"use client";

import { useState } from "react";
import { ResolveButton } from "@/components/Actions";
import { StatusPill } from "@/components/Bits";
import { fmtWhen } from "@/lib/format";
import type { AgentPage } from "@/lib/types";

const PAGE_SIZE = 10;

export default function EventTable({ table, actionLabel }: { table: AgentPage["table"]; actionLabel: string }) {
  const [page, setPage] = useState(1);
  const totalRows = table.rows.length;
  const totalPages = Math.max(1, Math.ceil(totalRows / PAGE_SIZE));

  // Current slice of 10 rows
  const startIndex = (page - 1) * PAGE_SIZE;
  const currentRows = table.rows.slice(startIndex, startIndex + PAGE_SIZE);

  const prevPage = () => setPage((p) => Math.max(1, p - 1));
  const nextPage = () => setPage((p) => Math.min(totalPages, p + 1));

  return (
    <section className="panel">
      <div className="flex flex-wrap items-center justify-between gap-3 px-4 pt-4 pb-2">
        <div>
          <h2 className="panel-title">{table.title}</h2>
          <span className="text-xs text-ink-faint">
            {totalRows === 0 ? "0 records" : `Showing ${startIndex + 1}–${Math.min(startIndex + PAGE_SIZE, totalRows)} of ${totalRows}`}
          </span>
        </div>

        {/* Swipe / Pagination Controls */}
        {totalRows > PAGE_SIZE && (
          <div className="flex items-center gap-2">
            <span className="text-xs font-medium text-ink-soft">
              List {page} of {totalPages}
            </span>
            <div className="inline-flex rounded-md border border-line bg-paper p-0.5 shadow-sm">
              <button
                type="button"
                onClick={prevPage}
                disabled={page === 1}
                className="inline-flex h-8 w-8 items-center justify-center rounded text-sm text-ink-soft hover:bg-surface disabled:opacity-30 disabled:hover:bg-transparent"
                aria-label="Previous list of 10"
                title="Previous list"
              >
                ←
              </button>
              <button
                type="button"
                onClick={nextPage}
                disabled={page === totalPages}
                className="inline-flex h-8 w-8 items-center justify-center rounded text-sm text-ink-soft hover:bg-surface disabled:opacity-30 disabled:hover:bg-transparent"
                aria-label="Next list of 10"
                title="Next list (Swipe right)"
              >
                →
              </button>
            </div>
          </div>
        )}
      </div>

      {totalRows === 0 ? (
        <p className="p-4 text-sm text-ink-faint">Nothing in this period.</p>
      ) : (
        <div className="mt-2 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-y border-line bg-paper text-ink-soft">
              <tr>
                {table.columns.map((c) => (
                  <th key={c.key} scope="col" className="whitespace-nowrap px-4 py-2 font-medium">
                    {c.label}
                  </th>
                ))}
                <th scope="col" className="px-4 py-2 font-medium">Status</th>
                <th scope="col" className="px-4 py-2"><span className="sr-only">Actions</span></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-mist">
              {currentRows.map((r) => (
                <tr key={r.id} className={r.actionable ? "bg-staff/[0.04]" : undefined}>
                  {table.columns.map((c) => (
                    <td key={c.key} className={`px-4 py-2.5 align-top ${c.wide ? "min-w-[16rem]" : "whitespace-nowrap"}`}>
                      {c.format === "datetime"
                        ? fmtWhen(r[c.key])
                        : c.key === "location_id"
                        ? capital(r.location_id)
                        : String(r[c.key] ?? "–")}
                    </td>
                  ))}
                  <td className="px-4 py-2.5 align-top">
                    <StatusPill status={r.status} />
                  </td>
                  <td className="whitespace-nowrap px-4 py-2.5 text-right align-top">
                    {r.recording_url && r.recording_url !== "–" && (
                      <a
                        className="mr-3 text-teal underline-offset-2 hover:underline"
                        href={String(r.recording_url)}
                        target="_blank"
                        rel="noreferrer"
                      >
                        Recording
                      </a>
                    )}
                    {r.actionable && <ResolveButton id={r.id} label={actionLabel} />}
                    {r.resolved_by && <span className="text-xs text-ink-faint">by {r.resolved_by}</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Bottom Pagination Footnote */}
          {totalRows > PAGE_SIZE && (
            <div className="flex items-center justify-between border-t border-line px-4 py-3 bg-paper/50 text-xs text-ink-faint">
              <span>Showing 10 per list</span>
              <div className="flex items-center gap-3">
                <span>
                  Page <strong>{page}</strong> of <strong>{totalPages}</strong>
                </span>
                <div className="inline-flex gap-1">
                  <button
                    type="button"
                    onClick={prevPage}
                    disabled={page === 1}
                    className="rounded border border-line px-2.5 py-1 text-ink-soft hover:bg-surface disabled:opacity-30"
                  >
                    ← Previous
                  </button>
                  <button
                    type="button"
                    onClick={nextPage}
                    disabled={page === totalPages}
                    className="rounded border border-line px-2.5 py-1 text-ink-soft hover:bg-surface disabled:opacity-30"
                  >
                    Next →
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
}

const capital = (s: string | null) => (s ? s[0].toUpperCase() + s.slice(1) : "–");
