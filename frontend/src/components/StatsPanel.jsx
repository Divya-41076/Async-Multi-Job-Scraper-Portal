function timeAgo(timestamp) {
  const now = new Date();
  const then = new Date(timestamp + "Z");
  const diff = Math.floor((now - then) / 1000); // seconds

  if (diff < 60) return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

function StatsPanel({ stats }) {
  if (!stats) return null;

  const sources = Object.entries(stats.jobs_per_source || {});
  const maxCount = Math.max(...sources.map(([, count]) => count), 1);

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
      {/* header */}
      <h2 className="text-white font-semibold text-sm mb-4">System Stats</h2>

      {/* total jobs */}
      <div className="mb-5">
        <p className="text-gray-500 text-xs mb-1">Total Jobs</p>
        <p className="text-white text-2xl font-bold">{stats.total_jobs}</p>
      </div>

      {/* jobs per source */}
      <div className="mb-5">
        <p className="text-gray-500 text-xs mb-3">Jobs by Source</p>

        {sources.length === 0 ? (
          <p className="text-gray-600 text-xs">No data yet</p>
        ) : (
          <div className="flex flex-col gap-3">
            {sources.map(([source, count]) => {
              const barWidth = Math.round((count / maxCount) * 100);
              return (
                <div key={source}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-gray-400 text-xs">{source}</span>
                    <span className="text-emerald-400 text-xs font-medium">
                      {count}
                    </span>
                  </div>
                  {/* mini bar */}
                  <div className="w-full bg-gray-800 rounded-full h-1.5">
                    <div
                      className="bg-emerald-500 h-1.5 rounded-full transition-all duration-500"
                      style={{ width: `${barWidth}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* latest timestamp */}
      {stats.latest_job_timestamp && (
        <div>
          <p className="text-gray-500 text-xs mb-1">Last Updated</p>
          <p className="text-gray-400 text-xs">
            {timeAgo(stats.latest_job_timestamp)}
          </p>
        </div>
      )}
    </div>
  );
}

export default StatsPanel;
