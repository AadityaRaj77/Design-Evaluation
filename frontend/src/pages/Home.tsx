import UploadSection from "../components/UploadSection";

export default function Home() {
  return (
    <div
      className="
    min-h-screen
    bg-black
    text-white
    overflow-hidden
    relative
  "
    >
      {/* Background Glow */}

      <div
        className="
      absolute
      top-[-200px]
      left-1/2
      -translate-x-1/2
      w-[900px]
      h-[900px]
      rounded-full
      bg-fuchsia-500/10
      blur-[180px]
    "
      />

      <div
        className="
      absolute
      bottom-[-200px]
      right-[-100px]
      w-[500px]
      h-[500px]
      rounded-full
      bg-cyan-500/10
      blur-[180px]
    "
      />

      <div
        className="
      relative
      max-w-7xl
      mx-auto
      px-8
      py-14
    "
      >
        <div className="mb-20">
          <div
            className="
          inline-flex
          items-center
          gap-2
          px-4
          py-2
          rounded-full
          border
          border-zinc-800
          bg-zinc-900/70
          backdrop-blur
        "
          >
            <div
              className="
            w-2
            h-2
            rounded-full
            bg-emerald-400
          "
            />

            <span
              className="
            text-sm
            text-zinc-300
          "
            >
              Multimodal AI Design Intelligence
            </span>
          </div>

          <h1
            className="
          text-7xl
          font-black
          tracking-tight
          mt-8
          max-w-5xl
          leading-[0.95]
        "
          >
            AI-powered design critique with visual reasoning.
          </h1>

          <p
            className="
          text-zinc-400
          text-xl
          mt-8
          max-w-2xl
          leading-relaxed
        "
          >
            Analyze layouts, typography, colors, hierarchy, spacing, and UX
            clarity using multimodal AI agents.
          </p>
        </div>

        <UploadSection />
      </div>
    </div>
  );
}
