// Server components call the API over the private network (API_URL);
// the browser uses NEXT_PUBLIC_API_URL for live updates and button actions.
const SERVER_API = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
export const PUBLIC_API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(public status: number, message: string) { super(message); }
}

export type Filters = { location?: string; days?: string };

export function filtersFrom(sp: Record<string, string | string[] | undefined>): Filters {
  const one = (v: string | string[] | undefined) => (Array.isArray(v) ? v[0] : v);
  return { location: one(sp.location) || undefined, days: one(sp.days) || "30" };
}

export async function apiGet<T>(path: string, filters: Filters = {}): Promise<T> {
  const qs = new URLSearchParams(Object.entries(filters).filter(([, v]) => v) as [string, string][]);
  let res: Response;
  try {
    // TODO(auth): forward the signed-in user's token once Cognito is wired up.
    res = await fetch(`${SERVER_API}${path}${qs.size ? `?${qs}` : ""}`, { cache: "no-store" });
  } catch {
    throw new ApiError(0, `The dashboard can't reach the API at ${SERVER_API}. Start it with: uvicorn app.main:app --reload`);
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, typeof body.detail === "string" ? body.detail : `API returned ${res.status}`);
  }
  return res.json();
}

export async function apiPost(path: string, body: unknown): Promise<void> {
  const res = await fetch(`${PUBLIC_API}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const b = await res.json().catch(() => ({}));
    throw new Error(typeof b.detail === "string" ? b.detail : `Request failed (${res.status})`);
  }
}

export const agentSlug = (key: string) => key.replace(/_/g, "-");
export const agentKey = (slug: string) => slug.replace(/-/g, "_");
