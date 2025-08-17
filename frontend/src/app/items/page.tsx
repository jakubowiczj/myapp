'use client';
import { useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE!;

export default function ItemsPage() {
  const [key, setKey] = useState('demo');
  const [json, setJson] = useState('{"hello":"world"}');
  const [result, setResult] = useState<string>('');

  async function putItem() {
    try {
      const body = JSON.parse(json);
      const res = await fetch(`${API_BASE}/items/${encodeURIComponent(key)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (e: unknown) {
      setResult(`PUT error: ${e.message ?? String(e)}`);
    }
  }

  async function getItem() {
    try {
      const res = await fetch(`${API_BASE}/items/${encodeURIComponent(key)}`, {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
      });
      const data = await res.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (e: unknown) {
      setResult(`GET error: ${e.message ?? String(e)}`);
    }
  }

  return (
    <main className="min-h-screen p-6 flex flex-col gap-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-semibold">Items (Postgres test)</h1>

      <label className="flex flex-col gap-1">
        <span className="text-sm text-gray-600">Key (pk)</span>
        <input
          className="border rounded px-3 py-2"
          value={key}
          onChange={(e) => setKey(e.target.value)}
        />
      </label>

      <label className="flex flex-col gap-1">
        <span className="text-sm text-gray-600">JSON body</span>
        <textarea
          className="border rounded px-3 py-2 font-mono"
          rows={6}
          value={json}
          onChange={(e) => setJson(e.target.value)}
        />
      </label>

      <div className="flex gap-3">
        <button onClick={putItem} className="rounded bg-black text-white px-4 py-2">PUT</button>
        <button onClick={getItem} className="rounded border px-4 py-2">GET</button>
      </div>

      <pre className="bg-gray-50 border rounded p-3 overflow-auto">{result}</pre>
    </main>
  );
}
