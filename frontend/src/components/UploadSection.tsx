import { useState } from "react";

import { motion } from "framer-motion";

import API from "../services/api";

import type { AnalysisResponse } from "../types/analysis";

import { Layout, Type, Palette, MonitorSmartphone } from "lucide-react";

export default function UploadSection() {
  const [file, setFile] = useState<File | null>(null);

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState<AnalysisResponse | null>(null);

  const [preview, setPreview] = useState<string | null>(null);

  const [activeTab, setActiveTab] = useState("original");

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

  const getCurrentImage = () => {
    if (!result) return preview;

    const base = "http://127.0.0.1:8000/";

    if (activeTab === "ocr") {
      return base + result.visualizations.ocr_overlay;
    }

    if (activeTab === "layout") {
      return base + result.visualizations.layout_overlay;
    }

    if (activeTab === "issues") {
      return base + result.visualizations.issue_overlay;
    }

    return preview;
  };

  return (
    <div className="space-y-10">
      {/* Upload Area */}

      <div
        className="
        border
        border-dashed
        border-zinc-700
        rounded-3xl
        p-12
        bg-zinc-950/70
        backdrop-blur
      "
      >
        <input
          type="file"
          accept="image/*"
          onChange={(e) => {
            if (!e.target.files) return;

            const selected = e.target.files[0];

            setFile(selected);

            setPreview(URL.createObjectURL(selected));
          }}
        />

        <p className="text-zinc-400 mt-4 text-lg">
          Upload a UI screenshot for multimodal AI analysis.
        </p>

        <button
          onClick={handleAnalyze}
          className="
          mt-8
          px-7
          py-4
          rounded-2xl
          bg-white
          text-black
          font-semibold
          hover:scale-[1.02]
          transition-all
          duration-300
          "
        >
          Analyze Design
        </button>
      </div>

      {/* Loading */}

      {loading && (
        <div
          className="
          border
          border-zinc-800
          rounded-3xl
          p-8
          bg-zinc-950
        "
        >
          <div
            className="
            animate-pulse
            space-y-4
          "
          >
            <div
              className="
              h-6
              bg-zinc-800
              rounded
              w-1/3
            "
            />

            <div
              className="
              h-24
              bg-zinc-800
              rounded
            "
            />

            <div
              className="
              h-24
              bg-zinc-800
              rounded
            "
            />
          </div>
        </div>
      )}

      {/* Result Dashboard */}

      {result && (
        <motion.div
          initial={{
            opacity: 0,
            y: 30,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.5,
          }}
          className="
            grid
            grid-cols-1
            lg:grid-cols-2
            gap-8
          "
        >
          {/* LEFT SIDE */}

          <div
            className="
            border
            border-zinc-800
            rounded-3xl
            overflow-hidden
            bg-zinc-950
          "
          >
            <div
              className="
              p-6
              border-b
              border-zinc-800
            "
            >
              <h2 className="text-2xl font-bold">Visual Analysis</h2>

              <div
                className="
                flex
                gap-3
                mt-6
                flex-wrap
              "
              >
                {["original", "ocr", "layout", "issues"].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`
                      px-4
                      py-2
                      rounded-xl
                      text-sm
                      capitalize
                      transition-all

                      ${
                        activeTab === tab
                          ? "bg-white text-black"
                          : "bg-zinc-900 text-zinc-400"
                      }
                    `}
                  >
                    {tab}
                  </button>
                ))}
              </div>
            </div>

            <img
              src={getCurrentImage() || ""}
              alt="analysis"
              className="
                w-full
                object-cover
              "
            />
          </div>

          {/* RIGHT SIDE */}

          <div
            className="
            border
            border-zinc-800
            rounded-3xl
            p-8
            bg-zinc-950
          "
          >
            <h2
              className="
              text-3xl
              font-bold
              mb-8
            "
            >
              AI Analysis
            </h2>

            {/* Score */}

            <div
              className="
              flex
              items-center
              justify-between
              mb-10
            "
            >
              <div>
                <div
                  className="
                  text-zinc-500
                  text-sm
                  uppercase
                  tracking-widest
                "
                >
                  Overall Score
                </div>

                <div
                  className="
                  text-7xl
                  font-bold
                  mt-2
                "
                >
                  {result.aggregated_result.overall_score}
                </div>
              </div>

              <motion.div
                initial={{
                  scale: 0.7,
                  opacity: 0,
                }}
                animate={{
                  scale: 1,
                  opacity: 1,
                }}
                transition={{
                  duration: 0.5,
                }}
                className="
                  w-32
                  h-32
                  rounded-full
                  border-8
                  border-white
                  flex
                  items-center
                  justify-center
                  text-3xl
                  font-bold
                "
              >
                {result.aggregated_result.overall_score}
              </motion.div>
            </div>

            {/* Agent Cards */}

            <div
              className="
              grid
              grid-cols-2
              gap-4
              mb-10
            "
            >
              {[
                {
                  label: "Layout",
                  icon: Layout,
                  score: result.agent_outputs.layout.score,
                },

                {
                  label: "Typography",
                  icon: Type,
                  score: result.agent_outputs.typography.score,
                },

                {
                  label: "Colors",
                  icon: Palette,
                  score: result.agent_outputs.color.score,
                },

                {
                  label: "UX",
                  icon: MonitorSmartphone,
                  score: result.agent_outputs.ux.score,
                },
              ].map((item, index) => {
                const Icon = item.icon;

                return (
                  <motion.div
                    key={index}
                    initial={{
                      opacity: 0,
                      y: 20,
                    }}
                    animate={{
                      opacity: 1,
                      y: 0,
                    }}
                    transition={{
                      delay: index * 0.08,
                    }}
                    className="
                      border
                      border-zinc-800
                      rounded-2xl
                      p-5
                      bg-zinc-900/40
                      hover:scale-[1.015]
                      transition-all
                      duration-300
                    "
                  >
                    <div
                      className="
                      flex
                      items-center
                      justify-between
                    "
                    >
                      <Icon
                        className="
                        w-5
                        h-5
                        text-zinc-400
                      "
                      />

                      <div
                        className="
                        text-2xl
                        font-bold
                      "
                      >
                        {item.score}
                      </div>
                    </div>

                    <div
                      className="
                      mt-4
                      text-zinc-400
                    "
                    >
                      {item.label}
                    </div>
                  </motion.div>
                );
              })}
            </div>

            {/* Issues */}

            <div className="space-y-4">
              {result.aggregated_result.issues.map((issue, index) => (
                <motion.div
                  key={index}
                  initial={{
                    opacity: 0,
                    y: 20,
                  }}
                  animate={{
                    opacity: 1,
                    y: 0,
                  }}
                  transition={{
                    delay: index * 0.08,
                  }}
                  className="
                      border
                      border-zinc-800
                      rounded-2xl
                      p-5
                      bg-zinc-900/40
                      hover:scale-[1.015]
                      transition-all
                      duration-300
                    "
                >
                  <div
                    className="
                      flex
                      items-center
                      gap-3
                    "
                  >
                    <div
                      className="
                        text-red-400
                        uppercase
                        text-xs
                        tracking-widest
                      "
                    >
                      {issue.severity}
                    </div>

                    <div
                      className="
                        font-semibold
                        text-lg
                      "
                    >
                      {issue.title}
                    </div>
                  </div>

                  <p
                    className="
                      text-zinc-400
                      mt-3
                      leading-relaxed
                    "
                  >
                    {issue.reason}
                  </p>
                </motion.div>
              ))}
            </div>

            {/* Suggestions */}

            <div className="mt-12">
              <div
                className="
                text-2xl
                font-bold
                mb-6
              "
              >
                Suggested Improvements
              </div>

              <div className="space-y-4">
                {result.aggregated_result.suggestions.map(
                  (suggestion, index) => (
                    <motion.div
                      key={index}
                      initial={{
                        opacity: 0,
                        y: 20,
                      }}
                      animate={{
                        opacity: 1,
                        y: 0,
                      }}
                      transition={{
                        delay: index * 0.08,
                      }}
                      className="
                        border
                        border-zinc-800
                        rounded-2xl
                        p-5
                        bg-zinc-900/40
                        flex
                        gap-5
                        items-start
                        hover:scale-[1.015]
                        transition-all
                        duration-300
                      "
                    >
                      <div
                        className="
                        min-w-10
                        h-10
                        rounded-full
                        bg-white
                        text-black
                        flex
                        items-center
                        justify-center
                        font-bold
                      "
                      >
                        {suggestion.priority}
                      </div>

                      <div>
                        <div
                          className="
                          text-zinc-500
                          text-sm
                          uppercase
                          tracking-widest
                          mb-2
                        "
                        >
                          Priority Fix
                        </div>

                        <div
                          className="
                          text-lg
                          leading-relaxed
                        "
                        >
                          {suggestion.action}
                        </div>
                      </div>
                    </motion.div>
                  ),
                )}
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
}
