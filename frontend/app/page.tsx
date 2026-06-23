"use client";
import { useState, useEffect, useRef } from "react";
import { motion, useInView, AnimatePresence } from "framer-motion";
import FileUpload from "./components/FileUpload";
import Dashboard from "./components/Dashboard";
import ChatInterface from "./components/ChatInterface";
import { Brain, ChevronDown, Shield, Zap, BarChart3, MessageSquare, Upload, TrendingUp, ArrowRight, Sparkles } from "lucide-react";

function CountUp({ end, duration = 2, prefix = "", suffix = "" }: {
  end: number; duration?: number; prefix?: string; suffix?: string;
}) {
  const [count, setCount] = useState(0);
  const ref = useRef(null);
  const inView = useInView(ref, { once: true });
  useEffect(() => {
    if (!inView) return;
    let start = 0;
    const increment = end / (duration * 60);
    const timer = setInterval(() => {
      start += increment;
      if (start >= end) { setCount(end); clearInterval(timer); }
      else setCount(Math.floor(start));
    }, 1000 / 60);
    return () => clearInterval(timer);
  }, [inView, end, duration]);
  return <span ref={ref}>{prefix}{count.toLocaleString()}{suffix}</span>;
}

export default function Home() {
  const [documentData, setDocumentData] = useState<any>(null);
  const appRef = useRef<HTMLDivElement>(null);

  // Force scroll to top on load
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "instant" });
  }, []);

  const scrollToApp = () => appRef.current?.scrollIntoView({ behavior: "smooth" });

  const features = [
    { icon: <Upload size={18} />, title: "Upload any document", desc: "Bank statements, tax returns, pay stubs. PDF or scanned image — both work." },
    { icon: <Brain size={18} />, title: "AI extracts everything", desc: "Transactions, balances, and categories extracted automatically with high accuracy." },
    { icon: <MessageSquare size={18} />, title: "Ask anything", desc: "Chat naturally about your finances. Get specific answers with cited numbers." },
    { icon: <BarChart3 size={18} />, title: "50/30/20 Benchmark", desc: "See instantly how your spending compares against the gold standard budgeting rule." },
    { icon: <TrendingUp size={18} />, title: "Multi-document analysis", desc: "Upload multiple months. Ask questions that span across all your statements." },
    { icon: <Shield size={18} />, title: "Private by design", desc: "Processed in memory. Never stored. Your financial data stays yours." },
  ];

  return (
    <div style={{ background: "#050810", minHeight: "100vh", color: "#e2e8f0" }}>

      {/* Nav */}
      <nav style={{
        position: "fixed", top: 0, left: 0, right: 0, zIndex: 50,
        padding: "16px 40px", display: "flex", alignItems: "center",
        justifyContent: "space-between",
        background: "linear-gradient(to bottom, rgba(5,8,16,0.95), transparent)",
        backdropFilter: "blur(10px)"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 32, height: 32, borderRadius: 8,
            background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
            display: "flex", alignItems: "center", justifyContent: "center"
          }}>
            <Brain size={16} color="white" />
          </div>
          <span style={{ fontWeight: 700, fontSize: 16, color: "white", letterSpacing: "-0.3px" }}>FinSight</span>
        </div>
        <button onClick={scrollToApp} style={{
          display: "flex", alignItems: "center", gap: 6,
          padding: "8px 16px", borderRadius: 8, border: "1px solid rgba(99,102,241,0.4)",
          background: "rgba(99,102,241,0.1)", color: "#a5b4fc",
          fontSize: 13, fontWeight: 500, cursor: "pointer", transition: "all 0.2s"
        }}>
          Launch App <ArrowRight size={13} />
        </button>
      </nav>

      {/* Hero */}
      <section style={{
        minHeight: "100vh", display: "flex", flexDirection: "column",
        alignItems: "center", justifyContent: "center",
        textAlign: "center", padding: "0 24px", position: "relative", overflow: "hidden"
      }}>
        {/* Ambient orbs */}
        <div style={{
          position: "absolute", top: "20%", left: "50%", transform: "translateX(-50%)",
          width: 600, height: 600, borderRadius: "50%",
          background: "radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%)",
          pointerEvents: "none"
        }} />
        <div style={{
          position: "absolute", top: "40%", left: "20%",
          width: 300, height: 300, borderRadius: "50%",
          background: "radial-gradient(circle, rgba(139,92,246,0.08) 0%, transparent 70%)",
          pointerEvents: "none"
        }} />

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
        >
          {/* Badge */}
          <div style={{
            display: "inline-flex", alignItems: "center", gap: 6,
            padding: "6px 14px", borderRadius: 100,
            border: "1px solid rgba(99,102,241,0.3)",
            background: "rgba(99,102,241,0.08)",
            color: "#a5b4fc", fontSize: 12, fontWeight: 500, marginBottom: 28
          }}>
            <Sparkles size={11} /> AI-Powered Financial Intelligence
          </div>

          {/* Headline */}
          <h1 style={{
            fontSize: "clamp(42px, 7vw, 80px)", fontWeight: 900,
            lineHeight: 1.08, letterSpacing: "-2px", color: "white", marginBottom: 24,
            maxWidth: 800
          }}>
            Your finances,<br />
            <span style={{
              background: "linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%)",
              WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent"
            }}>finally clear.</span>
          </h1>

          {/* Subheading */}
          <p style={{
            color: "#64748b", fontSize: "clamp(15px, 2vw, 18px)",
            maxWidth: 520, lineHeight: 1.7, marginBottom: 36
          }}>
            Upload any bank statement or tax return. Ask questions in plain English.
            Get answers backed by your actual numbers — not guesses.
          </p>

          {/* CTA */}
          <div style={{ display: "flex", gap: 12, marginBottom: 64 }}>
            <button onClick={scrollToApp} style={{
              padding: "13px 28px", borderRadius: 12,
              background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
              color: "white", fontWeight: 600, fontSize: 15,
              border: "none", cursor: "pointer",
              boxShadow: "0 0 40px rgba(99,102,241,0.3)",
              display: "flex", alignItems: "center", gap: 8,
              transition: "all 0.2s"
            }}>
              Try it free <ArrowRight size={15} />
            </button>
          </div>

          {/* Stats */}
          <div style={{ display: "flex", gap: 48, marginBottom: 56 }}>
            {[
              { end: 99, suffix: "%", label: "Extraction accuracy" },
              { end: 50, suffix: "+", label: "Document formats" },
              { end: 3, suffix: "s", label: "Average response" },
            ].map((s, i) => (
              <div key={i} style={{ textAlign: "center" }}>
                <div style={{ fontSize: 32, fontWeight: 800, color: "white", fontVariantNumeric: "tabular-nums", letterSpacing: "-1px" }}>
                  <CountUp end={s.end} suffix={s.suffix} />
                </div>
                <div style={{ fontSize: 12, color: "#475569", marginTop: 4 }}>{s.label}</div>
              </div>
            ))}
          </div>

          {/* Scroll cue */}
          <motion.button
            onClick={scrollToApp}
            animate={{ y: [0, 6, 0] }}
            transition={{ repeat: Infinity, duration: 1.8 }}
            style={{ background: "none", border: "none", cursor: "pointer", color: "#334155" }}
          >
            <ChevronDown size={22} />
          </motion.button>
        </motion.div>
      </section>

      {/* Features */}
      <section style={{ padding: "80px 24px", maxWidth: 1100, margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: 56 }}>
          <motion.p
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            style={{ color: "#6366f1", fontSize: 12, fontWeight: 600, letterSpacing: "2px", marginBottom: 12 }}
          >
            HOW IT WORKS
          </motion.p>
          <motion.h2
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            style={{ fontSize: "clamp(28px, 4vw, 42px)", fontWeight: 800, color: "white", letterSpacing: "-1px", lineHeight: 1.2 }}
          >
            From document to insight<br />in seconds
          </motion.h2>
        </div>

        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
          gap: 16
        }}>
          {features.map((f, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08 }}
              whileHover={{ y: -4, borderColor: "rgba(99,102,241,0.4)" }}
              style={{
                background: "#0d1117", border: "1px solid #1e2738",
                borderRadius: 16, padding: 24, transition: "all 0.2s", cursor: "default"
              }}
            >
              <div style={{
                width: 40, height: 40, borderRadius: 10,
                background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.2)",
                display: "flex", alignItems: "center", justifyContent: "center",
                color: "#818cf8", marginBottom: 16
              }}>
                {f.icon}
              </div>
              <h3 style={{ fontWeight: 600, color: "white", fontSize: 15, marginBottom: 8 }}>{f.title}</h3>
              <p style={{ color: "#475569", fontSize: 13, lineHeight: 1.6 }}>{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Divider */}
      <div style={{ height: 1, background: "linear-gradient(to right, transparent, #1e2738, transparent)", margin: "0 40px" }} />

      {/* App Section */}
      <section ref={appRef} style={{ padding: "80px 24px", maxWidth: 1200, margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: 48 }}>
          <motion.h2
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            style={{ fontSize: "clamp(28px, 4vw, 42px)", fontWeight: 800, color: "white", letterSpacing: "-1px", marginBottom: 12 }}
          >
            Your financial advisor,{" "}
            <span style={{
              background: "linear-gradient(135deg, #818cf8, #c084fc)",
              WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent"
            }}>
              ready now.
            </span>
          </motion.h2>
          <p style={{ color: "#475569", fontSize: 14 }}>No account needed — upload and start asking.</p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          style={{
            display: "grid", gridTemplateColumns: "380px 1fr",
            gap: 20, height: 780
          }}
        >
          {/* Left */}
          <div style={{ display: "flex", flexDirection: "column", gap: 16, overflowY: "auto", paddingRight: 4 }}>
            <div style={{ background: "#0d1117", border: "1px solid #1e2738", borderRadius: 16, padding: 20 }}>
              <FileUpload onUploadSuccess={setDocumentData} />
            </div>
            {documentData && <Dashboard data={documentData} />}
          </div>

          {/* Right — Chat */}
          <div style={{
            background: "#0d1117", border: "1px solid #1e2738",
            borderRadius: 16, display: "flex", flexDirection: "column", overflow: "hidden",
            boxShadow: "0 0 60px rgba(99,102,241,0.08)"
          }}>
            <div style={{
              padding: "16px 20px", borderBottom: "1px solid #1e2738",
              display: "flex", alignItems: "center", gap: 10
            }}>
              <div style={{
                width: 8, height: 8, borderRadius: "50%", background: "#6366f1",
                boxShadow: "0 0 10px rgba(99,102,241,0.6)"
              }} />
              <div>
                <div style={{ fontWeight: 600, color: "white", fontSize: 13 }}>Financial Assistant</div>
                <div style={{ fontSize: 11, color: "#475569" }}>
                  {documentData ? "Document loaded — ask anything" : "Upload a document to begin"}
                </div>
              </div>
            </div>
            <ChatInterface hasDocument={!!documentData} />
          </div>
        </motion.div>
      </section>

      {/* Footer */}
      <footer style={{
        padding: "32px 24px", borderTop: "1px solid #0f172a",
        textAlign: "center"
      }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8, marginBottom: 8 }}>
          <div style={{
            width: 24, height: 24, borderRadius: 6,
            background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
            display: "flex", alignItems: "center", justifyContent: "center"
          }}>
            <Brain size={12} color="white" />
          </div>
          <span style={{ fontWeight: 700, color: "white", fontSize: 13 }}>FinSight</span>
        </div>
        <p style={{ fontSize: 12, color: "#1e293b" }}>
          Built with RAG + LLM pipeline. Documents are never stored.
        </p>
      </footer>
    </div>
  );
}