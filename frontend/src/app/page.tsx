// src/app/page.tsx
async function getHealth() {
  const base = process.env.NEXT_PUBLIC_API_BASE!;
  const res = await fetch(`${base}/health`, { cache: "no-store" });
  if (!res.ok) return { status: "down" };
  return res.json() as Promise<{ status: string }>;
}

export default async function Home() {
  const data = await getHealth();
  return (
    <main className="p-8 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold">MyApp</h1>
      <p className="mt-2 text-sm opacity-80">
        Status API: <b>{data.status}</b>
      </p>
      <p className="mt-6">Next.js → FastAPI (Lambda) działa 🎉</p>
    </main>
  );
}