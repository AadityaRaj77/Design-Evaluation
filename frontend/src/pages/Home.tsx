import UploadSection from "../components/UploadSection";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.08),transparent_40%)]" />

      <div className="relative max-w-7xl mx-auto px-8 py-14">
        <div className="mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-zinc-800 bg-zinc-900/70 backdrop-blur">
            <div className="w-2 h-2 rounded-full bg-emerald-400" />

            <span className="text-sm text-zinc-300">
              Multimodal AI Design Intelligence
            </span>
          </div>

          <h1 className="text-7xl font-bold tracking-tight mt-8 max-w-4xl leading-none">
            Analyze UI screenshots with AI-powered design reasoning.
          </h1>

          <p className="text-zinc-400 text-xl mt-8 max-w-2xl leading-relaxed">
            Evaluate layouts, typography, colors, UX clarity, spacing, and
            visual hierarchy using specialized multimodal agents.
          </p>
        </div>

        <UploadSection />
      </div>
    </div>
  );
}
