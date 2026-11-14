"use client";
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { fmtDay } from "@/lib/format";
import type { Series } from "@/lib/types";

const COLORS: Record<string, string> = {
  Booked: "#2E7D5B", Verified: "#2E7D5B", Completed: "#2E7D5B", Done: "#2E7D5B",
  Info: "#8DB9BD", Transferred: "#3B5AA6", "Needs staff": "#A9670C",
  Failed: "#B3261E", Waiting: "#9AA8B0",
};
const FALLBACK = ["#1D6A73", "#6FA7AD", "#B9D4D6", "#3B5AA6"];

export default function SeriesChart({ series }: { series: Series }) {
  const total = series.points.reduce((n, p) => n + series.keys.reduce((m, k) => m + Number(p[k] || 0), 0), 0);
  return (
    <section className="panel p-4">
      <h2 className="panel-title">{series.title}</h2>
      {total === 0 ? (
        <p className="mt-3 text-sm text-ink-faint">No activity in this period. Pick a longer date range, or check that the agent is sending events.</p>
      ) : (
        <div className="mt-3 h-64" role="img" aria-label={`${series.title}, stacked by ${series.keys.join(", ")}`}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={series.points} margin={{ top: 4, right: 4, left: -18, bottom: 0 }}>
              <CartesianGrid vertical={false} stroke="#E4EDEA" />
              <XAxis dataKey="date" tickFormatter={fmtDay} tick={{ fontSize: 11, fill: "#7C8D91" }} tickLine={false} axisLine={false} minTickGap={24} />
              <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: "#7C8D91" }} tickLine={false} axisLine={false} />
              <Tooltip labelFormatter={(d) => fmtDay(String(d))} cursor={{ fill: "#E4EDEA" }} contentStyle={{ borderRadius: 6, borderColor: "#D3DEDA", fontSize: 13 }} />
              <Legend iconType="square" iconSize={10} wrapperStyle={{ fontSize: 12 }} />
              {series.keys.map((k, i) => (
                <Bar key={k} dataKey={k} stackId="a" fill={COLORS[k] ?? FALLBACK[i % FALLBACK.length]} maxBarSize={22} />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  );
}
