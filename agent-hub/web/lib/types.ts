export type Status = "done" | "needs_staff" | "failed" | "waiting" | "transferred";
export type Tone = "neutral" | "done" | "staff" | "failed";

export interface Kpi { label: string; value: string; sub: string; tone: Tone }
export interface Series { title: string; keys: string[]; points: Record<string, string | number>[] }
export interface BreakdownItem { label: string; value: number; display: string }
export interface Breakdown { title: string; items: BreakdownItem[]; agent?: string }
export interface Column { key: string; label: string; format?: "datetime"; wide?: boolean }
export interface Row {
  id: number; status: Status; actionable: boolean; resolved_by: string | null;
  location_id: string | null; when: string; recording_url?: string; [key: string]: unknown;
}

export interface AgentPage {
  agent: string; label: string; action_label: string; paused: boolean; sample_data: boolean;
  kpis: Kpi[]; series: Series | null; breakdowns: Breakdown[];
  table: { title: string; columns: Column[]; rows: Row[] }; cost: number;
}

export interface Meta {
  user: { email: string; role: string };
  locations: { id: string; name: string }[];
  agents: { key: string; label: string }[];
}

export interface Overview {
  tiles: { agent: string; label: string; kpi: Kpi; second: Kpi | null; paused: boolean; open_items: number; has_data: boolean }[];
  calls: Series | null;
  side_breakdowns: (Breakdown | null)[];
  needs_person: { id: number; agent: string; agent_label: string; when: string; summary: string; status: Status; location_id: string | null; action_label: string }[];
  alerts: { id: number; agent: string; summary: string; level: string; when: string }[];
  cost_month: number; budget: number; sample_data: boolean;
}
