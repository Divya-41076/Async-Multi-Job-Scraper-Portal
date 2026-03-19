import { useState, useEffect, useCallback } from "react";
import { fetchJobs } from "../services/api";
import JobCard from "../components/JobCard";
import SearchBar from "../components/SearchBar";
import StatusBanner from "../components/StatusBanner";
import { Link } from "react-router-dom";

const POLL_INTERVAL = 8000; // 8 seconds

function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [scrapeTriggered, setScrapeTriggered] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const [filters, setFilters] = useState({
    keyword: "",
    location: "",
    source: "",
  });

  const LIMIT = 20;

  const loadJobs = useCallback(
    async (currentPage = 1, currentFilters = filters) => {
      try {
        setLoading(true);
        setError(null);

        const params = {
          page: currentPage,
          limit: LIMIT,
          sort: "latest",
          ...(currentFilters.keyword && { keyword: currentFilters.keyword }),
          ...(currentFilters.location && { location: currentFilters.location }),
          ...(currentFilters.source && { source: currentFilters.source }),
        };

        const res = await fetchJobs(params);
        setJobs(res.data.results);
        setTotal(res.data.total);
        setScrapeTriggered(res.data.scrape_triggered);
        setLastUpdated(new Date()); // ← track last fetch time
      } catch (err) {
        setError("Failed to load jobs. Please try again.");
      } finally {
        setLoading(false);
      }
    },
    [filters],
  );

  // initial load
  useEffect(() => {
    loadJobs(1, filters);
  }, [filters, loadJobs]);

  // polling — only when scrape is running
  useEffect(() => {
    if (!scrapeTriggered) return;

    const interval = setInterval(() => {
      loadJobs(page, filters);
    }, POLL_INTERVAL);

    return () => clearInterval(interval);
  }, [scrapeTriggered, page, filters]);

  const handleSearch = (updated) => {
    setFilters((prev) => ({ ...prev, ...updated }));
    setPage(1);
  };

  const totalPages = Math.ceil(total / LIMIT);

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      {/* page title */}
      <div className="mb-6">
        <h1 className="text-white text-2xl font-bold mb-1">Browse Jobs</h1>
        <p className="text-gray-500 text-sm">
          Aggregated from Remotive, Jobicy and Adzuna
        </p>
        {/* ← ADD THIS */}
        <p className="text-gray-600 text-xs mt-1">
          Data refreshes automatically when stale.{" "}
          <Link
            to="/admin"
            className="text-emerald-500 hover:text-emerald-400 transition-colors"
          >
            Trigger a manual scrape →
          </Link>
        </p>
      </div>

      {/* search bar */}
      <div className="mb-4">
        <SearchBar
          keyword={filters.keyword}
          location={filters.location}
          source={filters.source}
          onSearch={handleSearch}
        />
      </div>

      {/* status banner */}
      <div className="mb-2">
        <StatusBanner scrapeTriggered={scrapeTriggered} />
      </div>

      {/* refresh indicator */}
      {lastUpdated && (
        <div className="flex items-center justify-between mb-4">
          <span className="text-gray-600 text-xs">{total} jobs found</span>
          <span className="text-gray-600 text-xs flex items-center gap-1">
            {scrapeTriggered && (
              <span className="w-1.5 h-1.5 bg-yellow-400 rounded-full animate-pulse inline-block mr-1" />
            )}
            Last updated: {lastUpdated.toLocaleTimeString()}
          </span>
        </div>
      )}

      {/* error state */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-3 rounded-xl text-sm mb-4">
          {error}
        </div>
      )}

      {/* loading state */}
      {loading && jobs.length === 0 && (
        <div className="text-gray-500 text-sm text-center py-12">
          Loading jobs...
        </div>
      )}

      {/* empty state */}
      {!loading && jobs.length === 0 && !error && (
        <div className="text-center py-12">
          {scrapeTriggered ? (
            <div>
              <p className="text-yellow-400 text-sm mb-1">
                ⟳ Fetching jobs for "{filters.keyword}"...
              </p>
              <p className="text-gray-500 text-xs">
                This may take up to a minute. Page will update automatically.
              </p>
            </div>
          ) : (
            <p className="text-gray-500 text-sm">
              No jobs found. Try a different keyword or filter.
            </p>
          )}
        </div>
      )}

      {/* jobs grid */}
      {jobs.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      )}

      {/* pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-6">
          <button
            onClick={() => {
              const prev = page - 1;
              setPage(prev);
              loadJobs(prev, filters);
            }}
            disabled={page === 1}
            className="px-4 py-2 text-sm bg-gray-900 border border-gray-800 text-gray-300 rounded-xl disabled:opacity-30 hover:border-emerald-500 transition-colors"
          >
            ← Prev
          </button>

          <span className="text-gray-500 text-sm">
            Page {page} of {totalPages}
          </span>

          <button
            onClick={() => {
              const next = page + 1;
              setPage(next);
              loadJobs(next, filters);
            }}
            disabled={page === totalPages}
            className="px-4 py-2 text-sm bg-gray-900 border border-gray-800 text-gray-300 rounded-xl disabled:opacity-30 hover:border-emerald-500 transition-colors"
          >
            Next →
          </button>
        </div>
      )}
    </div>
  );
}

export default Jobs;
