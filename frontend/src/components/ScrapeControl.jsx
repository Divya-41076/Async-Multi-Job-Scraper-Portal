import { useState } from "react";

export default function ScrapeControl({scrapeId, setScrapeId, loading, setLoading}){
    
    const [keyword,setKeyword] = useState("");
    const[selectedSources, setSelectedSources] = useState([]);
    // const [scrapeId, setScrapeId] = useState(null);
    // const[loading, setLoading] = useState(false);

    const sources = ["internshala", "TimesJobs"];

    const toggleSource = (source) => {
        if (selectedSources.includes(source)) {
            setSelectedSources(selectedSources.filter((s) => s !== source));
        }
        else {
            setSelectedSources([...selectedSources, source]);

        }
        
        }

    const handleStart = async() =>{
        if (!keyword || selectedSources.length === 0) return; 
        // validation to ensure keyword and at least one source is selected before starting the scrape

        
        console.log("Starting scrape with keyword:", keyword);
        // placeholder behaviour (real api)
        try {
            setLoading(true);

            const response = await fetch("http://127.0.0.1:5000/scrape",{
                method:"POST",
                headers: {
                    "Content-Type": "application/json",      
                },//this is header to specify we will be sending the json format data to the backend
                body: JSON.stringify({
                    keyword,
                    sources: selectedSources,//this body is what we will send it to the backend in json string format, we will include the keyword and the selected sources for scraping
                }),
                //body is the payload in the form of { "keyword": "python", "sources":[indeed,linkedin]}
            });

            if (!response.ok){
                throw new Error("Failed to start scrape");
            }

            const data = await response.json();

            setScrapeId(data.scrape_id);

        }

        catch (error){
            console.error("Error:", error);
            alert("Failed to start scrape.Please try again.");

        }

        finally{
            setLoading(false);
        }

        // setTimeout(() => {
        //     console.log("Scrape started for sources:", selectedSources);
        //     setScrapeId("ec78beec-895e-462e-bbd0-c016cee75f85");
        //     setLoading(false);
        
        // },1000);this was just to simulate the api call, now we will replace it with realapi call


    };

    return(
        <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
          <h2 className="text-lg font-medium mb-5">
            Trigger Scrape</h2>

          {/*keyword input*/}
          <div className="mb-4">
            <label className="block text-sm text-slate-600 mb-2">
                Keyword
            </label>
            <input type="text" 
                value ={keyword}
                onChange ={(e) => setKeyword(e.target.value)}
                placeholder = "e.g. Python developer"
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600"/>
                
          </div>

        {/* Source Selector */}
        <div className="mb-5">
            <label className="block text-sm text-slate-600 mb-2">
            Select Sources
            </label>

            <div className="flex flex-wrap gap-4">
            {sources.map((source) => (
                <label
                key={source}
                className="flex items-center gap-2 text-sm cursor-pointer"
                >
                <input
                    type="checkbox"
                    checked={selectedSources.includes(source)}
                    onChange={() => toggleSource(source)}
                    className="accent-teal-600"
                />
                {source}
                </label>
            ))}
            </div>
        </div>
        {/* Start Button */}
        <button
            onClick={handleStart}
            disabled={!keyword || selectedSources.length === 0 || loading}
            className={`w-full py-2 rounded-lg text-white transition ${
            loading
                ? "bg-slate-400 cursor-not-allowed"
                : "bg-teal-600 hover:bg-teal-700"
            }`}
        >
            {loading ? "Starting..." : "Start Scrape"}
        </button>

        {/* Scrape ID Display */}
        {scrapeId && (
            <div className="mt-5">
            <div className="text-sm text-slate-500 mb-1">
                Scrape ID
            </div>
            <div className="bg-slate-100 rounded-lg px-3 py-2 font-mono text-sm break-all">
                {scrapeId}
            </div>
            </div>
        )}
    
    </div>
    );



}
