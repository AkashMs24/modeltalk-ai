import { useState, useEffect } from 'react'
import { getBiasReport } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, Cell } from 'recharts'
import { Shield, AlertTriangle, CheckCircle, Loader } from 'lucide-react'
import toast from 'react-hot-toast'

export default function BiasReport() {
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(false)

  const fetchReport = async () => {
    setLoading(true)
    try {
      const data = await getBiasReport()
      setReport(data)
    } catch (e) {
      toast.error('Failed to load bias report: ' + (e.response?.data?.detail || e.message))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchReport() }, [])

  return (
    <div className="p-8 max-w-6xl mx-auto animate-slide-up">
      <div className="mb-8 flex items-start justify-between">
        <div>
          <h1 className="font-display text-3xl font-700 text-white mb-2">Bias Detection</h1>
          <p className="text-muted">Disparate impact analysis across gender, ethnicity, and geography.</p>
        </div>
        <button
          onClick={fetchReport}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-panel border border-border rounded-xl text-sm text-white hover:border-accent/40 transition-all"
        >
          {loading ? <Loader size={14} className="animate-spin" /> : <Shield size={14} />}
          Refresh
        </button>
      </div>

      {loading && !report && (
        <div className="flex items-center justify-center h-64 text-muted">
          <Loader size={24} className="animate-spin mr-3" /> Running bias analysis...
        </div>
      )}

      {report && (
        <div className="space-y-6">
          <div className={`rounded-2xl p-6 border ${report.bias_detected ? 'bg-crimson/5 border-crimson/30' : 'bg-emerald/5 border-emerald/30'}`}>
            <div className="flex items-center gap-4">
              {report.bias_detected
                ? <AlertTriangle size={28} className="text-amber" />
                : <CheckCircle size={28} className="text-emerald" />}
              <div>
                <div className="font-display font-700 text-white text-xl">
                  {report.bias_detected ? 'Bias Detected' : 'No Significant Bias'}
                </div>
                <div className="text-sm text-muted mt-1">{report.recommendation}</div>
              </div>
              <div className="ml-auto text-right">
                <div className={`text-3xl font-display font-700 ${report.overall_bias_score > 0.1 ? 'text-amber' : 'text-emerald'}`}>
                  {(report.overall_bias_score * 100).toFixed(1)}%
                </div>
                <div className="text-xs text-muted">Bias Score</div>
              </div>
            </div>

            {report.flagged_attributes.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {report.flagged_attributes.map(flag => (
                  <span key={flag} className="text-xs font-mono px-2 py-1 bg-amber/10 border border-amber/30 text-amber rounded-lg">
                    ⚠ {flag}
                  </span>
                ))}
              </div>
            )}
          </div>

          {Object.entries(report.disparate_impact).map(([attr, groups]) => {
            const chartData = Object.entries(groups).map(([group, di]) => ({
              name: group,
              di: parseFloat((di * 100).toFixed(1))
            }))

            return (
              <div key={attr} className="bg-panel border border-border rounded-2xl p-6">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-display font-600 text-white capitalize">{attr.replace('_', ' ')} — Disparate Impact</h3>
                  <span className="text-xs font-mono text-muted">Threshold: 80% (legal standard)</span>
                </div>
                <p className="text-xs text-muted mb-4">Approval rate relative to the best-performing group. Below 80% is legally flagged.</p>
                <ResponsiveContainer width="100%" height={180}>
                  <BarChart data={chartData} margin={{ top: 10 }}>
                    <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#6B7080' }} />
                    <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: '#6B7080' }} unit="%" />
                    <Tooltip
                      formatter={(v) => [`${v}%`, 'Disparate Impact']}
                      contentStyle={{ background: '#1A1A25', border: '1px solid #2A2A3A', borderRadius: 8, fontSize: 12 }}
                    />
                    <ReferenceLine y={80} stroke="#FFB547" strokeDasharray="4 4" label={{ value: '80% threshold', fontSize: 10, fill: '#FFB547', position: 'insideTopRight' }} />
                    <Bar dataKey="di" radius={[4, 4, 0, 0]}>
                      {chartData.map((entry, i) => (
                        <Cell key={i} fill={entry.di < 80 ? '#FF4D6A' : '#00D48A'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>

                <div className="mt-4 grid grid-cols-3 gap-3">
                  {Object.entries(report.demographic_breakdown[attr] || {}).map(([group, rate]) => (
                    <div key={group} className="bg-ink rounded-xl p-3">
                      <div className="text-xs text-muted font-mono">{group}</div>
                      <div className="text-lg font-display font-700 text-white">{(rate * 100).toFixed(1)}%</div>
                      <div className="text-xs text-muted">approval rate</div>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
