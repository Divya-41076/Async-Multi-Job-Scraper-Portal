function SearchBar({ keyword, location, source, onSearch }) {
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
      {/* keyword input */}
      <input
        type="text"
        placeholder="Search jobs... (e.g. python, react)"
        value={keyword}
        onChange={(e) => onSearch({ keyword: e.target.value })}
        className="flex-1 bg-gray-900 border border-gray-800 text-white placeholder-gray-500 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-emerald-500 transition-colors"
      />

      {/* location input */}
      <input
        type="text"
        placeholder="Location..."
        value={location}
        onChange={(e) => onSearch({ location: e.target.value })}
        className="bg-gray-900 border border-gray-800 text-white placeholder-gray-500 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-emerald-500 transition-colors sm:w-40"
      />

      {/* source filter */}
      <select
        value={source}
        onChange={(e) => onSearch({ source: e.target.value })}
        className="bg-gray-900 border border-gray-800 text-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-emerald-500 transition-colors sm:w-36"
      >
        <option value="">All Sources</option>
        <option value="Remotive">Remotive</option>
        <option value="Jobicy">Jobicy</option>
        <option value="Adzuna">Adzuna</option>
      </select>
    </div>
  );
}

export default SearchBar;
