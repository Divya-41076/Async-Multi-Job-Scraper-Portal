function StatusBanner({ scrapeTriggered }) {
  if (!scrapeTriggered) return null

  return (
    <div className="flex items-center gap-3 bg-yellow-400/10 border border-yellow-400/30 text-yellow-400 px-4 py-3 rounded-xl text-sm">
      {/* spinning indicator */}
      <svg
        className="animate-spin h-4 w-4 shrink-0"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          className="opacity-25"
          cx="12" cy="12" r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v8z"
        />
      </svg>
      <span>
        Refreshing jobs in background — results will update automatically
      </span>
    </div>
  )
}

export default StatusBanner