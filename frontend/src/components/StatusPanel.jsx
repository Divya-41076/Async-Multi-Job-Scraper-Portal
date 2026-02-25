export default function StatusPanel({ scrapeId, statusData}) {
    if (!scrapeId) {
        return (
            <div className = "bg-white rounded-2xl shadow-sm p-8 border border-slate-200">
                <h2 className = "text-xl font-semibold mb-6">Live Status</h2>
                <div className="text-slate-500 text-sm">
                    No active scrape.
                </div>
                </div>
        );
    }

    if (!statusData){
        return (
            <div className="bg-white rounded-2xl shadow-sm p-8 border border-slate-200">
                <h2 className="text-xl font-semibold mb-6">Live Status</h2>
                <div className="text-slate-500 text-sm">
                Fetching status...
                </div>
            </div>
        );
        
    }

    const badgeColor = statusData.state === "RUNNING" ? "bg-teal-600"
    : statusData.state === "COMPLETED" ? "bg-green-500"
    :statusData.state === "FAILED" ? "bg-red-500"
    : "bg-amber-500";


    return (
    <div className="bg-white rounded-2xl shadow-sm p-8 border border-slate-200">
      <h2 className="text-xl font-semibold mb-6">Live Status</h2>

      <span className={`px-3 py-1 text-xs rounded-full text-white ${badgeColor}`}>
        {statusData.state}
      </span>

      <div className="mt-4 text-sm text-slate-600">
        Message: {statusData.message}
      </div>

      <div className="mt-2 text-sm text-slate-600">
        Matched: {statusData.matched}
      </div>
    </div>
  );


}
    //     const renderBadge=() => {
//         if (loading) {

//             return (
//                 <span className = "px-3 py-1 text-xs font-medium rounded-full bg-teal-600 text-white">
//                     RUNNING
//                 </span>
//             );
//         }

//         if (scrapeId)
//         {
//             return (
//                 <span className="px-3 py-1 text-xs font-medium rounded-full bg-green-500 text-white">
//                     COMPLETED
//                 </span>
//             );
//         }
//         return null;
//     };


//     return(
//         <div className = "bg-white rounded-2xl shadow-sm p-8 border border-slate-200">
//             <h2 className="text-xl font-semibold mb-6">
//                 LIVE STATUS
//             </h2>
//             {!scrapeId && !loading && (
//                 <div className="text-slate-500 text-sm">
//                     No active scrape.
//                     <div className="mt-2 text-xs">
//                         Start a scrape to monitor execution progress.
//                     </div>
//                 </div>
//             )}

//             {(loading || scrapeId) && (
//                 <div>
//                     <div className="mb-4">
//                         {renderBadge()}
//                     </div>

//                     {scrapeId && (
//                         <div className="text-sm text-slate-600">
//                             Scrape ID:
//                             <div className="mt-1 bg-slate-100 rounded-lg px-3 py-2 font-mono text-xs break-all">
//                                 {scrapeId}
//                             </div>
//                         </div>
//                     )}

//                     {loading && (
//                         <div className = "mt-4 text-sm text-slate-600">
//                             Scraping in progress...
//                         </div>
//                     )}
//                 </div>
//             )}  
//         </div>
//     );
// }