import { useState, useRef, useEffect } from "react";
import { UploadCloud, FileText, CheckCircle, Loader2, AlertTriangle, Info, Calendar, Settings, Tags } from "lucide-react";
import { api } from "../lib/api";

export function Documents() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState<string>("idle");
  const [metadata, setMetadata] = useState<any>(null);
  const [error, setError] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setStatus("idle");
      setMetadata(null);
      setError("");
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setStatus("uploading");
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/documents/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const { document_id } = response.data.data;
      pollStatus(document_id);
    } catch (err: any) {
      setError(err.message || "Failed to upload document");
      setUploading(false);
      setStatus("failed");
    }
  };

  const pollStatus = async (documentId: string) => {
    const interval = setInterval(async () => {
      try {
        const res = await api.get(`/documents/${documentId}/status`);
        const data = res.data.data;
        setStatus(data.status);
        
        if (data.status === "indexed") {
          clearInterval(interval);
          setUploading(false);
          setMetadata(data.metadata || {});
        } else if (data.status === "failed") {
          clearInterval(interval);
          setUploading(false);
          setError(data.message || "Processing failed");
        }
      } catch (err) {
        console.error("Failed to poll status", err);
      }
    }, 2000);
  };

  const getStatusMessage = () => {
    switch(status) {
      case "uploading": return "Uploading document...";
      case "processing": return "Initializing processing pipeline...";
      case "ocr": return "Extracting text and running OCR...";
      case "analyzing": return "AI is analyzing document contents...";
      case "embedding": return "Generating semantic embeddings...";
      case "indexed": return "Document ready!";
      case "failed": return "Processing failed.";
      default: return "";
    }
  };

  return (
    <div className="flex flex-col gap-8 max-w-5xl mx-auto py-8 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Document Intelligence</h1>
        <p className="text-muted-foreground mt-2">Upload PDFs or DOCX files for instant AI-powered analysis.</p>
      </div>

      {!metadata && (
        <div className="glass-panel rounded-2xl p-8 border-dashed border-2 border-border/50 hover:border-primary/50 transition-colors flex flex-col items-center justify-center text-center">
          <input 
            type="file" 
            className="hidden" 
            ref={fileInputRef} 
            onChange={handleFileChange}
            accept=".pdf,.docx"
          />
          
          <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
            <UploadCloud className="w-8 h-8 text-primary" />
          </div>
          
          {file ? (
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-foreground font-medium bg-background/50 px-4 py-2 rounded-lg border border-border">
                <FileText className="w-4 h-4 text-primary" />
                {file.name}
              </div>
              
              {!uploading && status !== "failed" && (
                <div className="flex gap-4 justify-center">
                  <button 
                    onClick={() => setFile(null)}
                    className="px-4 py-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                  >
                    Cancel
                  </button>
                  <button 
                    onClick={handleUpload}
                    className="px-6 py-2 bg-primary text-primary-foreground text-sm font-medium rounded-lg shadow-sm hover:bg-primary/90 transition-all"
                  >
                    Analyze Document
                  </button>
                </div>
              )}
            </div>
          ) : (
            <>
              <h3 className="text-lg font-medium text-foreground">Click to upload or drag and drop</h3>
              <p className="text-sm text-muted-foreground mt-1">PDF or DOCX (Max 10MB)</p>
              <button 
                onClick={() => fileInputRef.current?.click()}
                className="mt-6 px-6 py-2 bg-secondary text-secondary-foreground text-sm font-medium rounded-lg shadow-sm hover:bg-secondary/80 transition-all"
              >
                Select File
              </button>
            </>
          )}

          {uploading && (
            <div className="mt-8 flex flex-col items-center gap-3 w-full max-w-md">
              <Loader2 className="w-6 h-6 text-primary animate-spin" />
              <p className="text-sm font-medium text-foreground">{getStatusMessage()}</p>
              <div className="w-full bg-muted rounded-full h-1.5 overflow-hidden">
                <div className="bg-primary h-1.5 rounded-full animate-pulse w-full"></div>
              </div>
            </div>
          )}

          {error && (
            <div className="mt-6 flex items-center gap-2 text-destructive bg-destructive/10 px-4 py-3 rounded-lg text-sm">
              <AlertTriangle className="w-4 h-4" />
              {error}
            </div>
          )}
        </div>
      )}

      {metadata && (
        <div className="space-y-6 animate-fade-in">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold flex items-center gap-2 text-foreground">
              <CheckCircle className="w-5 h-5 text-green-500" />
              Document Analyzed
            </h2>
            <button 
              onClick={() => { setFile(null); setMetadata(null); setStatus("idle"); }}
              className="text-sm text-primary hover:underline"
            >
              Upload another
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-2 space-y-6">
              <div className="glass-panel p-6 rounded-xl border border-border">
                <h3 className="text-2xl font-bold text-foreground mb-2">
                  {metadata.DocumentTitle || file?.name}
                </h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  {metadata.Summary || "No summary available."}
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="glass-panel p-6 rounded-[1.25rem]">
                  <div className="flex items-center gap-2 text-white/50 mb-4">
                    <Settings className="w-4 h-4 text-white/50" />
                    <span className="text-xs font-medium tracking-wide">Equipment</span>
                  </div>
                  <p className="font-semibold text-white text-2xl tracking-tight mb-2">{metadata.EquipmentName || "N/A"}</p>
                  <p className="text-sm text-white/50 mt-1">ID <span className="text-white ml-2">{metadata.EquipmentID || "N/A"}</span></p>
                  <p className="text-sm text-white/50">Mfg <span className="text-white ml-2">{metadata.Manufacturer || "N/A"}</span></p>
                </div>

                <div className="glass-panel p-6 rounded-[1.25rem]">
                  <div className="flex items-center gap-2 text-white/50 mb-4">
                    <Info className="w-4 h-4 text-white/50" />
                    <span className="text-xs font-medium tracking-wide">Details</span>
                  </div>
                  <p className="font-semibold text-white text-2xl tracking-tight mb-2 capitalize">{metadata.DocumentType || "Document"}</p>
                  <p className="text-sm text-white/50 mt-1">Dept <span className="text-white ml-2">{metadata.Department || "N/A"}</span></p>
                  <p className="text-sm text-white/50">Rev <span className="text-white ml-2">{metadata.RevisionNumber || "1.0"}</span></p>
                </div>
              </div>

              {metadata.MaintenanceActions && metadata.MaintenanceActions.length > 0 && (
                <div className="glass-panel p-6 rounded-[1.25rem]">
                  <h4 className="text-sm font-semibold text-white mb-5 tracking-wide flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-primary" /> Maintenance Actions
                  </h4>
                  <ul className="space-y-4">
                    {metadata.MaintenanceActions.map((action: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-3 text-sm text-white/80">
                        <span className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5 flex-shrink-0" />
                        {action}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="space-y-6">
              {metadata.SafetyWarnings && metadata.SafetyWarnings.length > 0 && (
                <div className="bg-[#1a1a1c] border border-destructive/30 p-6 rounded-[1.25rem]">
                  <h4 className="text-sm font-semibold text-destructive mb-5 tracking-wide flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4" /> Critical Warnings
                  </h4>
                  <ul className="space-y-4">
                    {metadata.SafetyWarnings.map((warning: string, idx: number) => (
                      <li key={idx} className="text-sm text-white flex items-start gap-3">
                        <span className="w-1.5 h-1.5 rounded-full bg-destructive mt-1.5 flex-shrink-0" />
                        {warning}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {metadata.Keywords && metadata.Keywords.length > 0 && (
                <div className="glass-panel p-6 rounded-[1.25rem]">
                  <h4 className="text-sm font-semibold text-white mb-5 tracking-wide flex items-center gap-2">
                    <Tags className="w-4 h-4 text-white/50" /> Intelligence Tags
                  </h4>
                  <div className="flex flex-wrap gap-2.5">
                    {metadata.Keywords.map((kw: string, idx: number) => (
                      <span key={idx} className="px-4 py-2 rounded-full bg-[#2a2a2c] text-white/90 text-xs font-medium hover:bg-[#3a3a3c] transition-colors cursor-pointer border border-white/5">
                        {kw}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {metadata.ErrorCodes && metadata.ErrorCodes.length > 0 && (
                <div className="glass-panel p-6 rounded-[1.25rem]">
                  <h4 className="text-sm font-semibold text-white mb-5 tracking-wide">Diagnostics</h4>
                  <div className="flex flex-wrap gap-2.5">
                    {metadata.ErrorCodes.map((code: string, idx: number) => (
                      <span key={idx} className="px-4 py-2 rounded-xl font-mono bg-accent/10 text-accent font-semibold text-sm border border-accent/20">
                        {code}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
