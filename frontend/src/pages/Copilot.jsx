import { useState, useRef, useEffect } from 'react'
import { sendChatMessage } from '../services/api'
import { Send, Loader, Bot, User } from 'lucide-react'
import toast from 'react-hot-toast'

const SUGGESTED = [
  'Why was my loan rejected?',
  'What does debt-to-income ratio mean?',
  'How can I improve my revolving utilization?',
  'Is my risk score normal for my income?',
  'What factors matter most for approval?',
  'Explain SHAP values in simple terms'
]

// Sample context using real Kaggle feature names
const sampleContext = {
  revolving_utilization: 0.35,
  age: 45,
  late_30_59_days: 0,
  debt_ratio: 0.28,
  monthly_income: 5400,
  open_credit_lines: 8,
  late_90_days: 0,
  real_estate_loans: 1,
  late_60_89_days: 0,
  num_dependents: 2,
  gender: 'Male',
  ethnicity: 'White',
  zip_region: 'Urban'
}

export default function Copilot() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hello! I'm your Explainable AI Copilot. I can help you understand loan decisions, explain AI concepts, or walk you through what factors affect credit risk. What would you like to know?"
    }
  ])
  const [input, setInput]   = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (text) => {
    const msg = text || input.trim()
    if (!msg || loading) return

    const userMsg = { role: 'user', content: msg }
    setMessages(m => [...m, userMsg])
    setInput('')
    setLoading(true)

    try {
      const history = messages.map(m => ({ role: m.role, content: m.content }))
      const res = await sendChatMessage({
        message: msg,
        application_context: sampleContext,
        conversation_history: history
      })
      setMessages(m => [...m, { role: 'assistant', content: res.response }])
    } catch (e) {
      toast.error('Chat error: ' + (e.response?.data?.detail || e.message))
      setMessages(m => [...m, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="flex flex-col h-screen max-h-screen p-6 max-w-4xl mx-auto">
      <div className="mb-4">
        <h1 className="font-display text-3xl font-700 text-white mb-1">AI Copilot Chat</h1>
        <p className="text-muted text-sm">Ask anything about loan decisions in plain English. Powered by LLaMA 3.3 70B.</p>
      </div>

      <div className="flex flex-wrap gap-2 mb-4">
        {SUGGESTED.map(s => (
          <button key={s} onClick={() => sendMessage(s)} disabled={loading}
            className="text-xs px-3 py-1.5 bg-panel border border-border rounded-full text-muted hover:text-white hover:border-accent/40 transition-all disabled:opacity-50"
          >
            {s}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pr-1 mb-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''} animate-slide-up`}>
            <div className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 ${
              msg.role === 'assistant' ? 'bg-accent/20' : 'bg-panel border border-border'
            }`}>
              {msg.role === 'assistant'
                ? <Bot size={14} className="text-accent" />
                : <User size={14} className="text-muted" />}
            </div>
            <div className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
              msg.role === 'assistant'
                ? 'bg-panel border border-border text-white/85'
                : 'bg-accent text-white'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 animate-slide-up">
            <div className="w-8 h-8 rounded-xl bg-accent/20 flex items-center justify-center flex-shrink-0">
              <Bot size={14} className="text-accent" />
            </div>
            <div className="bg-panel border border-border rounded-2xl px-4 py-3">
              <div className="flex gap-1">
                {[0,1,2].map(i => (
                  <div key={i} className="w-2 h-2 bg-accent rounded-full animate-bounce"
                    style={{ animationDelay: `${i * 0.15}s` }} />
                ))}
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="flex gap-3 bg-panel border border-border rounded-2xl p-3">
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          rows={1}
          placeholder="Ask about your loan decision..."
          className="flex-1 bg-transparent text-white text-sm placeholder:text-muted focus:outline-none resize-none"
        />
        <button
          onClick={() => sendMessage()}
          disabled={loading || !input.trim()}
          className="w-9 h-9 bg-accent hover:bg-accent/80 disabled:opacity-40 rounded-xl flex items-center justify-center transition-all flex-shrink-0"
        >
          {loading ? <Loader size={14} className="animate-spin text-white" /> : <Send size={14} className="text-white" />}
        </button>
      </div>
    </div>
  )
}
