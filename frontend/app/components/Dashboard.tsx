"use client";
import { TrendingUp, TrendingDown, DollarSign, PieChart } from "lucide-react";
import { motion } from "framer-motion";

interface DashboardProps {
  data: any;
}

export default function Dashboard({ data }: DashboardProps) {
  if (!data) return null;

  const { calculated_summary, benchmark, metadata } = data;
  const spending = calculated_summary.spending_by_category;
  const maxSpend = Math.max(...Object.values(spending) as number[]);

  const categoryColors: Record<string, string> = {
    rent: "bg-red-500",
    shopping: "bg-orange-500",
    food: "bg-yellow-500",
    utilities: "bg-blue-500",
    health: "bg-green-500",
    subscription: "bg-purple-500",
    transport: "bg-pink-500",
    other: "bg-slate-500",
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-3"
    >
      {/* Account */}
      <div className="card p-4">
        <p className="text-xs text-slate-500 mb-1">Account</p>
        <p className="font-semibold text-white text-sm">
          {metadata.account_holder || "Unknown"}
        </p>
        <p className="text-xs text-slate-500 capitalize">
          {metadata.document_type?.replace("_", " ")}
        </p>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-3 gap-2">
        {[
          { icon: <TrendingUp size={14} />, label: "Income", value: calculated_summary.total_credits, color: "text-green-400", bg: "bg-green-500/10" },
          { icon: <TrendingDown size={14} />, label: "Spent", value: calculated_summary.total_debits, color: "text-red-400", bg: "bg-red-500/10" },
          { icon: <DollarSign size={14} />, label: "Saved", value: calculated_summary.net_cashflow, color: "text-cyan-400", bg: "bg-cyan-500/10" },
        ].map((m, i) => (
          <div key={i} className={`card p-3 ${m.bg}`}>
            <div className={`${m.color} mb-1`}>{m.icon}</div>
            <p className={`text-base font-bold font-mono ${m.color}`}>
              ${m.value.toLocaleString()}
            </p>
            <p className="text-xs text-slate-500">{m.label}</p>
          </div>
        ))}
      </div>

      {/* Benchmark */}
      <div className="card p-4">
        <div className="flex items-center gap-2 mb-3">
          <PieChart size={14} className="text-cyan-400" />
          <p className="text-sm font-semibold text-white">50/30/20 Rule</p>
        </div>
        <div className="space-y-3">
          {[
            { label: "Needs", pct: benchmark.needs_pct, target: "<50%", color: "bg-blue-500" },
            { label: "Wants", pct: benchmark.wants_pct, target: "<30%", color: "bg-orange-500" },
            { label: "Savings", pct: benchmark.savings_pct, target: ">20%", color: "bg-green-500" },
          ].map((item) => (
            <div key={item.label}>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-400">{item.label}</span>
                <span className="text-slate-500 font-mono">{item.pct}% <span className="text-slate-600">/ {item.target}</span></span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.min(item.pct, 100)}%` }}
                  transition={{ duration: 1, ease: "easeOut" }}
                  className={`${item.color} h-1.5 rounded-full`}
                />
              </div>
            </div>
          ))}
        </div>
        <div className="mt-3 space-y-1">
          {benchmark.recommendations.map((r: string, i: number) => (
            <p key={i} className="text-xs text-slate-400 bg-slate-800/50 rounded-lg p-2 leading-relaxed">{r}</p>
          ))}
        </div>
      </div>

      {/* Spending */}
      <div className="card p-4">
        <p className="text-sm font-semibold text-white mb-3">Spending Breakdown</p>
        <div className="space-y-2.5">
          {Object.entries(spending).map(([cat, amount]) => (
            <div key={cat}>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-400 capitalize">{cat}</span>
                <span className="text-slate-300 font-mono">${(amount as number).toLocaleString()}</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${((amount as number) / maxSpend) * 100}%` }}
                  transition={{ duration: 0.8, ease: "easeOut" }}
                  className={`${categoryColors[cat] || "bg-slate-500"} h-1.5 rounded-full`}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}