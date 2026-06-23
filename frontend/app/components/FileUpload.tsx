"use client";
import { useState } from "react";
import { Upload, FileText, CheckCircle, AlertCircle } from "lucide-react";

interface FileUploadProps {
  onUploadSuccess: (data: any) => void;
}

export default function FileUpload({ onUploadSuccess }: FileUploadProps) {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  const handleUpload = async (file: File) => {
    setUploading(true);
    setStatus("idle");
    setMessage("Processing document...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");
      const data = await res.json();
      setStatus("success");
      setMessage(`Successfully processed: ${data.file_name}`);
      onUploadSuccess(data);
    } catch (err) {
      setStatus("error");
      setMessage("Failed to process document. Make sure the backend is running.");
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleUpload(file);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleUpload(file);
  };

  return (
    <div className="w-full">
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-xl p-10 text-center transition-all cursor-pointer
          ${dragging ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-blue-400 hover:bg-gray-50"}
          ${uploading ? "opacity-50 pointer-events-none" : ""}`}
        onClick={() => document.getElementById("fileInput")?.click()}
      >
        <input
          id="fileInput"
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          className="hidden"
          onChange={handleFileInput}
        />
        <Upload className="mx-auto mb-3 text-gray-400" size={36} />
        <p className="text-gray-600 font-medium">
          {uploading ? "Processing..." : "Drop your financial document here"}
        </p>
        <p className="text-gray-400 text-sm mt-1">
          Supports PDF, PNG, JPG — bank statements, tax returns, pay stubs
        </p>
      </div>

      {message && (
        <div className={`mt-3 flex items-center gap-2 text-sm p-3 rounded-lg
          ${status === "success" ? "bg-green-50 text-green-700" : ""}
          ${status === "error" ? "bg-red-50 text-red-700" : ""}
          ${status === "idle" ? "bg-blue-50 text-blue-700" : ""}`}>
          {status === "success" && <CheckCircle size={16} />}
          {status === "error" && <AlertCircle size={16} />}
          {status === "idle" && <FileText size={16} />}
          {message}
        </div>
      )}
    </div>
  );
}