export default function HomePage() {
  return (
    <div className="p-8">
      <div className="mx-auto max-w-7xl">
        <div>
          <p className="text-sm font-medium text-zinc-500">
            Enterprise AI Workspace
          </p>

          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-zinc-900">
            Dashboard
          </h1>

          <p className="mt-2 text-zinc-500">
            Monitor documents, conversations, retrieval, and
            Agentic RAG workflows from one workspace.
          </p>
        </div>

        <div className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard
            label="Documents"
            value="—"
            description="Indexed documents"
          />

          <MetricCard
            label="Conversations"
            value="—"
            description="Active conversations"
          />

          <MetricCard
            label="Queries"
            value="—"
            description="Questions processed"
          />

          <MetricCard
            label="Confidence"
            value="—"
            description="Average response confidence"
          />
        </div>

        <div className="mt-8 rounded-xl border border-zinc-200 bg-white p-6">
          <h2 className="text-lg font-semibold text-zinc-900">
            System Overview
          </h2>

          <p className="mt-2 text-sm text-zinc-500">
            Live platform metrics will appear here once the
            analytics API is connected.
          </p>
        </div>
      </div>
    </div>
  );
}

function MetricCard({
  label,
  value,
  description,
}: {
  label: string;
  value: string;
  description: string;
}) {
  return (
    <div className="rounded-xl border border-zinc-200 bg-white p-5">
      <p className="text-sm font-medium text-zinc-500">
        {label}
      </p>

      <p className="mt-3 text-3xl font-semibold text-zinc-900">
        {value}
      </p>

      <p className="mt-1 text-xs text-zinc-400">
        {description}
      </p>
    </div>
  );
}