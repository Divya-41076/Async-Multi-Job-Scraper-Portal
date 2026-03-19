import { useState, useEffect } from "react";
import { triggerScrape, getScrapeStatus, fetchStats } from "../services/api";
import StatsPanel from "../components/StatsPanel";
import { Link } from "react-router-dom";

function Admin() {
  const [keyword, setKeyword] = useState("");
  const [scrapeId, setScrapeId] = useState(null);
  const [scrapeStatus, setScrapeStatus] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // load stats on mount
  useEffect(() => {
    loadStats();
  }, []);

  // poll scrape status when scrape is running
  useEffect(() => {
    if (!scrapeId) return;
    if (scrapeStatus?.state === "COMPLETED" || scrapeStatus?.state === "FAILED")
      return;

    const interval = setInterval(async () => {
      try {
        const res = await getScrapeStatus(scrapeId);
        setScrapeStatus(res.data);

        // refresh stats when completed
        if (res.data.state === "COMPLETED") {
          loadStats();
        }
      } catch (err) {
        clearInterval(interval);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [scrapeId, scrapeStatus]);

  const loadStats = async () => {
    try {
      const res = await fetchStats();
      setStats(res.data);
    } catch (err) {
      console.error("Failed to load stats");
    }
  };

  const handleTriggerScrape = async () => {
    if (!keyword.trim()) return;

    try {
      setLoading(true);
      setError(null);
      setScrapeStatus(null);

      const res = await triggerScrape(keyword);
      setScrapeId(res.data.scrape_id);
      setScrapeStatus({
        state: "PENDING",
        message: "Queued",
        matched: 0,
      });
    } catch (err) {
      setError("Failed to trigger scrape. Check your API key.");
    } finally {
      setLoading(false);
    }
  };

  const getStateColor = (state) => {
    if (state === "COMPLETED") return "text-green-500";
    if (state === "FAILED") return "text-red-500";
    if (state === "RUNNING") return "text-yellow-400";
    return "text-gray-400";
  };

  const getStateDot = (state) => {
    if (state === "COMPLETED") return "bg-green-500";
    if (state === "FAILED") return "bg-red-500";
    if (state === "RUNNING") return "bg-yellow-400 animate-pulse";
    return "bg-gray-500";
  };

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      {/* page title */}
      <div className="mb-6">
        <h1 className="text-white text-2xl font-bold mb-1">Admin Panel</h1>
        <p className="text-gray-500 text-sm">
          Monitor and trigger the job aggregation pipeline
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {/* scrape control */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h2 className="text-white font-semibold text-sm mb-4">
            Trigger Scrape
          </h2>

          {/* keyword input */}
          <input
            type="text"
            placeholder="Enter keyword (e.g. python)"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleTriggerScrape()}
            className="w-full bg-gray-800 border border-gray-700 text-white placeholder-gray-500 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-emerald-500 transition-colors mb-3"
          />

          {/* trigger button */}
          <button
            onClick={handleTriggerScrape}
            disabled={loading || !keyword.trim()}
            className="w-full bg-emerald-500 hover:bg-blue-600 disabled:opacity-30 text-white text-sm font-medium px-4 py-2.5 rounded-xl shadow-lg shadow-emerald-500/20 transition-all duration-200"
          >
            {loading ? "Starting..." : "Run Scrape"}
          </button>

          {/* error */}
          {error && <p className="text-red-400 text-xs mt-3">{error}</p>}

          {/* scrape status */}
          {scrapeStatus && (
            <div className="mt-4 p-3 bg-gray-800 border border-gray-700 rounded-xl">
              <div className="flex items-center gap-2 mb-2">
                <div
                  className={`w-2 h-2 rounded-full ${getStateDot(scrapeStatus.state)}`}
                />
                <span
                  className={`text-sm font-medium ${getStateColor(scrapeStatus.state)}`}
                >
                  {scrapeStatus.state}
                </span>
              </div>
              <p className="text-gray-400 text-xs mb-1">
                {scrapeStatus.message}
              </p>
              <p className="text-gray-500 text-xs">
                Matched:{" "}
                <span className="text-white">{scrapeStatus.matched}</span>
              </p>
              {scrapeId && (
                <p className="text-gray-600 text-xs mt-1 truncate">
                  ID: {scrapeId}
                </p>
              )}
              {/* ← ADD THIS */}
              {scrapeStatus.state === "COMPLETED" && (
                <Link
                  to="/"
                  className="inline-block mt-3 text-xs text-emerald-400 hover:text-emerald-300 transition-colors"
                >
                  View new jobs →
                </Link>
              )}
            </div>
          )}
        </div>

        {/* stats panel */}
        <StatsPanel stats={stats} />
      </div>
    </div>
  );
}

export default Admin;
