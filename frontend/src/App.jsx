import {useState , useEffect} from "react";
import ScrapeControl from "./components/ScrapeControl";
import StatusPanel from "./components/StatusPanel";


export default function App(){
  const [scrapeId, setScrapeId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [statusData, setStatusData] = useState(null);

  useEffect(() => {
    if (!scrapeId) return;

    const interval = setInterval(async() => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/scrape/status/${scrapeId}`);

        if (!response.ok) return;

        const data = await response.json();
        setStatusData(data);

        if (
          data.state === "COMPLETED" || data.state === "FAILED"
        )
        {
          clearInterval(interval);
        }
      }
      catch(error){
        console.error("Polling errror:", error);
      }
    },2000);

    return () => clearInterval(interval);
  }, [scrapeId]);

  
  return(
    <div className="min-h-screen px-6 py-8">
      <div className="max-w-7xl mx-auto">
        {/*Header*/}
        <header className="mb-10">
          <h1 className="text-3xl font-semibold">
            Job Aggregator Dashboard
          </h1>
          <p className="text-slate-500 mt-1">
            Async Mutli-Portal Scraper System
          </p>
        </header>

        {/*trigger +monitor section */}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <ScrapeControl 
              scrapeId = {scrapeId}
              setScrapeId = {setScrapeId}
              loading = {loading}
              setLoading = {setLoading}
            />

            
          </div>
        
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <StatusPanel
              scrapeId={scrapeId}
              statusData={statusData}
            />
          </div>

        </div>

        {/*stats section */}
        <div className="mb-10">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            
            {[1,2,3,4].map((i) =>(
              <div
              key={i}
              className ="bg-white rounded-xl shadow-sm p-6 border border-slate-200"
              >
                Stat Card {i}
              </div>
              
            ))}

          </div>
        </div>


        {/*jobs table */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
          Jobs Table(coming next)
        </div>


      </div>
    </div>
  );
}