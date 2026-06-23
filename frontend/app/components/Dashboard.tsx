"use client";
import { TrendingUp, TrendingDown, DollarSign, PieChart } from "lucide-react";

interface DashboardProps {
  data: any;
}

export default function Dashboard({ data }: DashboardProps) {
  if (!data) return null;

  const { calculated_summary, benchmark, metadata } = data;
  const spending = calculated_summary.spending_by_category;
  const maxSpend = Math.max(...Object.values(spending) as number[]);

  const categoryColors: Record<string, string> = {
    rent: "bg-red-400",
    shopping: "bg-orange-400",
    food: "bg-yellow-400",
    utilities: "bg-blue-400",
    health: "bg-green-400",
    subscription: "bg-purple-400",
    transport: "bg-pink-400",
    other: "bg-gray-400",
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="bg-white rounded-xl p-4 border border-gray-200">
        <p className="text-sm text-gray-500">Account Holder</p>
        <p className="font-semibold text-gray-800">
          {metadata.account_holder || "Unknown"} — {metadata.document_type?.replace("_", " ")}
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-3 gap-3">
        <div className="bg-green-50 rounded-xl p-4 border border-green-100">
          <div className="flex items-center gap-2 mb-1">
            <TrendingUp size={16} className="text-green-600" />
            <p className="text-xs text-green-600 font-medium">Income</p>
          </div>
          <p className="text-xl font-bold text-green-700">
            ${calculated_summary.total_credits.toLocaleString()}
          </p>
        </div>

        <div className="bg-red-50 rounded-xl p-4 border border-red-100">
          <div className="flex items-center gap-2 mb-1">
            <TrendingDown size={16} className="text-red-600" />
            <p className="text-xs text-red-600 font-medium">Expenses</p>
          </div>
          <p className="text-xl font-bold text-red-700">
            ${calculated_summary.total_debits.toLocaleString()}
          </p>
        </div>

        <div className="bg-blue-50 rounded-xl p-4 border border-blue-100">
          <div className="flex items-center gap-2 mb-1">
            <DollarSign size={16} className="text-blue-600" />
            <p className="text-xs text-blue-600 font-medium">Saved</p>
          </div>
          <p className="text-xl font-bold text-blue-700">
            ${calculated_summary.net_cashflow.toLocaleString()}
          </p>
        </div>
      </div>

      {/* 50/30/20 Benchmark */}
      <div className="bg-white rounded-xl p-4 border border-gray-200">
        <div className="flex items-center gap-2 mb-3">
          <PieChart size={16} className="text-gray-500" />
          <p className="font-semibold text-gray-700 text-sm">50/30/20 Benchmark</p>
        </div>
        <div className="space-y-2">
          {[
            { label: "Needs", pct: benchmark.needs_pct, target: 50, color: "bg-blue-400" },
            { label: "Wants", pct: benchmark.wants_pct, target: 30, color: "bg-orange-400" },
            { label: "Savings", pct: benchmark.savings_pct, target: 20, color: "bg-green-400" },
          ].map((item) => (
            <div key={item.label}>
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>{item.label}</span>
                <span>{item.pct}% <span className="text-gray-400">(target: {item.label === "Savings" ? ">" : "<"}{item.target}%)</span></span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-2">
                <div
                  className={`${item.color} h-2 rounded-full transition-all`}
                  style={{ width: `${Math.min(item.pct, 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
        <div className="mt-3 space-y-1">
          {benchmark.recommendations.map((r: string, i: number) => (
            <p key={i} className="text-xs text-gray-600 bg-gray-50 rounded-lg p-2">{r}</p>
          ))}
        </div>
      </div>

      {/* Spending by Category */}
      <div className="bg-white rounded-xl p-4 border border-gray-200">
        <p className="font-semibold text-gray-700 text-sm mb-3">Spending by Category</p>
        <div className="space-y-2">
          {Object.entries(spending).map(([cat, amount]) => (
            <div key={cat}>
              <div className="flex justify-between text-xs text-gray-600 mb-1">
                <span className="capitalize">{cat}</span>
                <span>${(amount as number).toLocaleString()}</span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-2">
                <div
                  className={`${categoryColors[cat] || "bg-gray-400"} h-2 rounded-full`}
                  style={{ width: `${((amount as number) / maxSpend) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}