const TZ = process.env.NEXT_PUBLIC_CLINIC_TZ ?? "America/Chicago";

export function fmtWhen(iso: unknown): string {
  if (typeof iso !== "string" || !iso || iso === "–") return "–";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  const days = Math.abs(Date.now() - d.getTime()) / 864e5;
  const opts: Intl.DateTimeFormatOptions =
    days < 6
      ? { weekday: "short", hour: "numeric", minute: "2-digit", timeZone: TZ }
      : { month: "short", day: "numeric", hour: "numeric", minute: "2-digit", timeZone: TZ };
  return new Intl.DateTimeFormat("en-US", opts).format(d);
}

export function fmtTime(iso: string): string {
  return new Intl.DateTimeFormat("en-US", { hour: "numeric", minute: "2-digit", timeZone: TZ }).format(new Date(iso));
}

export function fmtDay(iso: string): string {
  return new Intl.DateTimeFormat("en-US", { month: "short", day: "numeric", timeZone: "UTC" }).format(new Date(iso));
}

export const usd = (n: number) => n.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });

export const STATUS_LABEL: Record<string, string> = {
  done: "Done", needs_staff: "Needs staff", failed: "Failed", waiting: "Waiting", transferred: "Sent to staff",
};
