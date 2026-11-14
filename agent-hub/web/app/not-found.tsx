import Link from "next/link";

export default function NotFound() {
  return (
    <div className="panel max-w-xl p-6">
      <h1 className="text-lg font-semibold">No agent with that name has reported yet</h1>
      <p className="mt-2 text-sm text-ink-soft">An agent gets its own page as soon as it sends its first event.</p>
      <Link href="/" className="btn mt-4">Back to overview</Link>
    </div>
  );
}
