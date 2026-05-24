import { useState } from "react";

import API from "../services/api";

import type { AnalysisResponse } from "../types/analysis";

export default function UploadSection() {
  const [file, setFile] = useState<File | null>(null);

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState<AnalysisResponse | null>(null);

  const handleAnalyze = async () => {
    if (!file) return;

    try {
      setLoading(true);

      const formData = new FormData();

      formData.append("file", file);

      const response = await API.post("/analyze", formData);

      setResult(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="border border-zinc-800 rounded-3xl p-8 bg-zinc-950">
        <input
          type="file"
          accept="image/*"
          onChange={(e) => {
            if (!e.target.files) return;

            setFile(e.target.files[0]);
          }}
        />

        <button
          onClick={handleAnalyze}
          className="mt-6 px-6 py-3 rounded-xl bg-white text-black font-medium"
        >
          Analyze Design
        </button>
      </div>

      {loading && <div className="text-zinc-400">Analyzing screenshot...</div>}

      {result && (
        <div className="border border-zinc-800 rounded-3xl p-8 bg-zinc-950">
          <h2 className="text-3xl font-bold mb-6">Analysis Result</h2>

          <div className="text-5xl font-bold mb-8">
            {result.aggregated_result.overall_score}
          </div>

          <div className="space-y-4">
            {result.aggregated_result.issues.map((issue, index) => (
              <div
                key={index}
                className="border border-zinc-800 rounded-2xl p-5"
              >
                <div className="flex items-center gap-3">
                  <div className="text-red-400 uppercase text-xs">
                    {issue.severity}
                  </div>

                  <div className="font-semibold">{issue.title}</div>
                </div>

                <p className="text-zinc-400 mt-3">{issue.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
