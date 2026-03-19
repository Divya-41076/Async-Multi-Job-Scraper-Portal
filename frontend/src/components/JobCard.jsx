function JobCard({ job }) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:scale-[1.01] hover:shadow-lg hover:shadow-emerald-500/10 transition-all duration-200">
      {/* header — title + source */}
      <div className="flex items-start justify-between gap-4 mb-3">
        <h2 className="text-white font-semibold text-base leading-snug">
          {job.title}
        </h2>
        <span className="text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-1 rounded-full shrink-0">
          {job.source}
        </span>
      </div>

      {/* company + location */}
      <div className="flex items-center gap-2 text-gray-300 text-sm mb-3">
        <span>{job.company}</span>
        {job.location && (
          <>
            <span className="text-gray-600">•</span>
            <span className="text-gray-400">{job.location}</span>
          </>
        )}
      </div>

      {/* skills */}
      {job.skills && (
        <p className="text-gray-500 text-xs mb-4 line-clamp-2">{job.skills}</p>
      )}

      {/* footer — salary + experience + link */}
      <div className="flex items-center justify-between mt-auto">
        <div className="flex gap-3">
          {job.salary && job.salary !== "Not disclosed" && (
            <span className="text-green-500 text-xs font-medium">
              {job.salary}
            </span>
          )}
          {job.experience && job.experience !== "Not specified" && (
            <span className="text-gray-500 text-xs">{job.experience}</span>
          )}
        </div>

        {job.job_url && (
          <a
            href={job.job_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-emerald-500 hover:text-emerald-400 font-medium transition-colors"
          >
            View Job →
          </a>
        )}
      </div>
    </div>
  );
}

export default JobCard;
