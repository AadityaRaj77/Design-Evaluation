function UploadSection() {
  return (
    <section className="rounded-3xl border border-white/10 bg-white/5 p-10">
      <p className="text-zinc-300">
        Upload your design screenshot to get started.
      </p>
    </section>
  );
}

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-8 py-12">
        <div className="mb-12">
          <h1 className="text-6xl font-bold tracking-tight">
            AI Design Evaluator
          </h1>

          <p className="text-zinc-400 mt-4 text-lg max-w-2xl">
            Analyze UI screenshots using multimodal AI reasoning, layout
            intelligence, UX critique, and visual explainability.
          </p>
        </div>

        <UploadSection />
      </div>
    </div>
  );
}
