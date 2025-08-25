const base = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export async function healthCheck() {
  console.log("API DEBUG base:", base); // 👈 dodajmy jeszcze test
  const res = await fetch(`${base}/health`, { cache: "no-store" });
  return res.json();
}

export { base };