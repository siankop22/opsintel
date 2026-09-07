"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";

type DocumentResult = {
  id: number;
  title: string;
  score: number;
};

type MetricResult = {
  site: string;
  timestamp: string;
  throughput: number;
  staffing: number;
  downtime_minutes: number;
};

type ToolCall = {
  tool: string;
  arguments: Record<string, string>;
  results: DocumentResult[] | MetricResult[];
};

type InvestigationResult = {
  answer: string;
  tool_calls: ToolCall[];
  session_id: string;
  latency_ms: number;
  tool_call_count: number;
};

export default function Home() {
  const [question, setQuestion] = useState(
    "Investigate why NYC-02 throughput dropped on September 4."
  );

  function getSessionId() {
    let storedSession = localStorage.getItem("opsintel_session_id");

    if (!storedSession) {
      storedSession = crypto.randomUUID();
      localStorage.setItem("opsintel_session_id", storedSession);
    }

    return storedSession;
  }

  const [result, setResult] = useState<InvestigationResult | null>(null);
  const [loading, setLoading] = useState(false);

  async function runInvestigation() {
    const sessionId = getSessionId();

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000"}/api/investigate`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question,
            session_id: sessionId,
          }),
        }
      );

      const data = await response.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  }

  function renderToolResults(call: ToolCall) {
    if (call.tool === "search_documents") {
      const documents = call.results as DocumentResult[];

      return (
        <div className="mt-3 space-y-2">
          {documents.map((item) => (
            <div
              key={item.id}
              className="flex justify-between gap-4 text-sm"
            >
              <span className="text-zinc-300">
                {item.title}
              </span>

              <span className="text-zinc-500">
                {item.score.toFixed(2)}
              </span>
            </div>
          ))}
        </div>
      );
    }

    if (call.tool === "query_operations") {
      const metrics = call.results as MetricResult[];

      return (
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-zinc-500">
              <tr>
                <th className="pb-2 pr-4">Time</th>
                <th className="pb-2 pr-4">Throughput</th>
                <th className="pb-2 pr-4">Staffing</th>
                <th className="pb-2">Downtime</th>
              </tr>
            </thead>

            <tbody>
              {metrics.map((row, index) => (
                <tr
                  key={index}
                  className="border-t border-zinc-800"
                >
                  <td className="py-2 pr-4 text-zinc-300">
                    {new Date(row.timestamp).toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </td>

                  <td className="py-2 pr-4 text-zinc-300">
                    {row.throughput.toLocaleString()}
                  </td>

                  <td className="py-2 pr-4 text-zinc-300">
                    {row.staffing}
                  </td>

                  <td className="py-2 text-zinc-300">
                    {row.downtime_minutes} min
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }

    return null;
  }

  return (
    <main className="min-h-screen bg-black text-white">
      <div className="mx-auto max-w-5xl px-6 py-20">
        <p className="text-sm uppercase tracking-widest text-zinc-500">
          Enterprise AI Investigation Platform
        </p>

        <h1 className="mt-4 text-5xl font-bold">
          OpsIntel
        </h1>

        <p className="mt-5 max-w-2xl text-lg text-zinc-400">
          Investigate operational problems using AI agents,
          hybrid search, reranking, structured data, and memory.
        </p>

        <div className="mt-10 rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
          <label className="text-sm text-zinc-400">
            Investigation question
          </label>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="mt-3 min-h-32 w-full rounded-xl border border-zinc-700 bg-black p-4 text-white outline-none"
          />

          <button
            onClick={runInvestigation}
            disabled={loading}
            className="mt-4 rounded-xl bg-white px-5 py-3 font-medium text-black disabled:opacity-50"
          >
            {loading ? "Investigating..." : "Run Investigation"}
          </button>
        </div>

        {result && (
          <div className="mt-8 space-y-6">
            <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
              <h2 className="text-xl font-semibold">
                Investigation Result
              </h2>

              <div className="mt-4 flex gap-4 text-sm text-zinc-500">
                <span>
                  Latency: {(result.latency_ms / 1000).toFixed(2)}s
                </span>

                <span>
                  Tool calls: {result.tool_call_count}
                </span>
              </div>

              <div className="mt-4 space-y-4 leading-7 text-zinc-300">
                <ReactMarkdown>
                  {result.answer}
                </ReactMarkdown>
              </div>
            </div>

            <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
              <h2 className="text-xl font-semibold">
                Agent Activity
              </h2>

              <div className="mt-4 space-y-4">
                {result.tool_calls.map((call, index) => (
                  <div
                    key={index}
                    className="rounded-xl border border-zinc-800 bg-black p-4"
                  >
                    <p className="font-mono text-sm text-white">
                      {call.tool}
                    </p>

                    <p className="mt-2 text-sm text-zinc-500">
                      {JSON.stringify(call.arguments)}
                    </p>

                    {renderToolResults(call)}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
