import { useState, useEffect } from 'react'
import { Upload, CheckCircle, Activity, Globe, Sparkles, RefreshCw, TikTok, Youtube, Instagram, Facebook, MessageSquare } from 'lucide-react'

const API_BASE = 'http://localhost:8000/api'

function App() {
  const [syncing, setSyncing] = useState(false)
  const [suggestions, setSuggestions] = useState([])
  const [syncHistory, setSyncHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [sugRes, syncRes] = await Promise.all([
          fetch(`${API_BASE}/suggestions/daily`),
          fetch(`${API_BASE}/activity/sync-status`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
          })
        ])
        
        if (sugRes.ok) setSuggestions(await sugRes.json())
        if (syncRes.ok) setSyncHistory(await syncRes.json())
      } catch (err) {
        console.error("Failed to fetch dashboard data", err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const handleManualSync = () => {
    setSyncing(true)
    setTimeout(() => setSyncing(false), 2000)
  }

  return (
    <div className="min-h-screen bg-[#050505] text-white font-['Inter'] selection:bg-purple-500/30">
      {/* Navbar */}
      <nav className="border-b border-white/5 bg-black/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-tr from-purple-600 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-purple-500/20">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold tracking-tight">Dead Air</span>
          </div>
          <div className="flex items-center gap-6">
            <button className="text-sm font-medium text-zinc-400 hover:text-white transition-colors">Integrations</button>
            <button className="text-sm font-medium text-zinc-400 hover:text-white transition-colors">Settings</button>
            <div className="w-8 h-8 rounded-full bg-zinc-800 border border-white/10" />
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-12 grid lg:grid-cols-[1fr,380px] gap-12">
        {/* Left Column: Sync & Suggestions */}
        <div className="space-y-12">
          {/* Header */}
          <div className="flex items-end justify-between">
            <div>
              <h1 className="text-4xl font-bold tracking-tight mb-2">Sync Dashboard</h1>
              <p className="text-zinc-400">Post to TikTok, and we'll handle the rest automatically.</p>
            </div>
            <button 
              onClick={handleManualSync}
              className="flex items-center gap-2 px-6 py-3 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 transition-all font-semibold active:scale-[0.98]"
            >
              <RefreshCw className={`w-4 h-4 ${syncing ? 'animate-spin text-purple-400' : ''}`} />
              {syncing ? 'Checking TikTok...' : 'Sync Now'}
            </button>
          </div>

          {/* Sync Cards */}
          <div className="grid sm:grid-cols-2 gap-4">
            <div className="group bg-zinc-900/40 border border-white/5 rounded-3xl p-8 hover:border-purple-500/30 transition-all cursor-pointer overflow-hidden relative">
              <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
                <Globe className="w-24 h-24" />
              </div>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-12 h-12 bg-white/10 rounded-2xl flex items-center justify-center font-bold">TT</div>
                <div>
                  <h3 className="font-bold">TikTok Source</h3>
                  <p className="text-xs text-green-400">Connected</p>
                </div>
              </div>
              <p className="text-sm text-zinc-500 leading-relaxed mb-6">Watching @yourhandle for new uploads. No watermark fetch enabled.</p>
              <div className="flex -space-x-2">
                {[1, 2, 3].map(i => (
                  <div key={i} className="w-8 h-8 rounded-full border-2 border-zinc-900 bg-zinc-800" />
                ))}
              </div>
            </div>

            <div className="bg-gradient-to-br from-purple-500/10 to-blue-500/10 border border-purple-500/20 rounded-3xl p-8">
              <h3 className="font-bold mb-4">Distribution Rules</h3>
              <div className="space-y-3">
                {[
                  { label: 'YouTube Shorts', active: true },
                  { label: 'Instagram Reels', active: true },
                  { label: 'Facebook Reels', active: false },
                  { label: 'Threads', active: true },
                ].map(p => (
                  <div key={p.label} className="flex items-center justify-between text-sm">
                    <span className={p.active ? 'text-zinc-300' : 'text-zinc-600'}>{p.label}</span>
                    <div className={`w-2 h-2 rounded-full ${p.active ? 'bg-purple-500' : 'bg-transparent border border-zinc-700'}`} />
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Daily Suggestions section */}
          <div>
            <div className="flex items-center gap-2 mb-6">
              <Sparkles className="w-5 h-5 text-yellow-400" />
              <h2 className="text-2xl font-bold tracking-tight">Daily Suggestions</h2>
            </div>
            <div className="grid gap-4">
              {loading ? (
                <div className="animate-pulse text-zinc-600">Loading your creative hooks...</div>
              ) : suggestions.map((s, i) => (
                <div key={i} className="group bg-zinc-900/50 border border-white/5 rounded-3xl p-6 hover:bg-zinc-800/50 transition-all cursor-pointer">
                  <div className="flex items-center justify-between mb-3">
                    <span className="px-3 py-1 bg-white/5 rounded-lg text-[10px] font-bold text-zinc-400 uppercase tracking-widest">{s.category}</span>
                    <button className="p-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <RefreshCw className="w-4 h-4 text-zinc-500" />
                    </button>
                  </div>
                  <h4 className="font-bold text-lg mb-2">{s.title}</h4>
                  <p className="text-sm text-zinc-500 leading-relaxed">{s.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Activity & Refund Status */}
        <div className="space-y-6">
          <div className="bg-black border border-white/5 rounded-3xl p-8 sticky top-32">
            <div className="flex items-center justify-between mb-8">
              <h2 className="font-bold flex items-center gap-2">
                <Globe className="w-4 h-4 text-blue-400" />
                Fleet Status
              </h2>
              <div className="px-3 py-1 bg-purple-500/10 text-purple-400 text-[10px] font-bold uppercase tracking-widest rounded-full border border-purple-500/20">
                Monitoring
              </div>
            </div>

            <div className="space-y-8">
              <div className="relative">
                <div className="absolute left-4 top-8 bottom-0 w-px bg-zinc-800" />
                {syncHistory.length > 0 ? syncHistory.map((item, i) => (
                  <div key={i} className="flex gap-4 mb-8 last:mb-0 relative">
                    <div className="w-8 h-8 rounded-full bg-zinc-900 border border-white/5 flex items-center justify-center shrink-0 z-10">
                      <CheckCircle className="w-3 h-3 text-green-400" />
                    </div>
                    <div>
                      <p className="text-sm font-semibold">Synced to {item.platform}</p>
                      <p className="text-[11px] text-zinc-500">{new Date(item.posted_at).toLocaleString()}</p>
                    </div>
                  </div>
                )) : (
                  <p className="text-sm text-zinc-500">No sync history yet.</p>
                )}
              </div>
            </div>

            <div className="mt-12 pt-8 border-t border-white/5">
              <div className="flex justify-between items-end mb-4">
                <div>
                  <p className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-1">Package Health</p>
                  <p className="text-2xl font-bold">100% Eligible</p>
                </div>
                <p className="text-xs text-green-400 pb-1">32 Day Streak</p>
              </div>
              <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-purple-500 to-blue-500 w-full animate-pulse-slow" />
              </div>
              <p className="text-[10px] text-zinc-500 mt-4 leading-relaxed">
                Posts are being distributed automatically. Maintain 1 post every 24h to keep refund eligibility active.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
