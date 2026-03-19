import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:5000'
const API_KEY = 'secret123'

const api = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
})

// Jobs
export const fetchJobs = (params) => {
    return api.get('/jobs', { params })
}

// Scrape
export const triggerScrape = (keyword) => {
    return api.post('/scrape', 
        { keyword },
        { headers: { 'X-API-KEY': API_KEY } }
    )
}

export const getScrapeStatus = (scrapeId) => {
    return api.get(`/scrape/status/${scrapeId}`)
}

// Stats
export const fetchStats = () => {
    return api.get('/stats')
}

// Health
export const fetchHealth = () => {
    return api.get('/health')
}