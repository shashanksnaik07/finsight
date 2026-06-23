"use client";
import { useState } from "react";
import FileUpload from "./components/FileUpload";
import Dashboard from "./components/Dashboard";
import ChatInterface from "./components/ChatInterface";
import { Brain } from "lucide-react";

export default function Home() {
  const [documentData, setDocumentData] = useState<any>(null);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <Brain size={18} className="text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900">FinSight</h1>
            <p className="text-xs text-gray-500">Personal Financial Document Intelligence</p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-6">
        <div className="grid grid-cols-12 gap-6 h-[calc(100vh-120px)]">

          {/* Left Panel — Upload + Dashboard */}
          <div className="col-span-4 flex flex-col gap-4 overflow-y-auto">
            <FileUpload onUploadSuccess={setDocumentData} />
            {documentData && <Dashboard data={documentData} />}
          </div>

          {/* Right Panel — Chat */}
          <div className="col-span-8 bg-white rounded-xl border border-gray-200 flex flex-col overflow-hidden">
            <div className="px-4 py-3 border-b border-gray-200">
              <h2 className="font-semibold text-gray-700 text-sm">Financial Assistant</h2>
              <p className="text-xs text-gray-400">Ask anything about your uploaded documents</p>
            </div>
            <ChatInterface hasDocument={!!documentData} />
          </div>

        </div>
      </main>
    </div>
  );
}