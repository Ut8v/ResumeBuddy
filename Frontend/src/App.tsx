import React, { useState, type ChangeEvent, type FormEvent } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import HealthLine from "./components/display";
import { ContentService } from "./services";

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [responseText, setResponseText] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] ?? null;
    setFile(f);
  };

  const handleJobDescriptionChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setJobDescription(e.target.value);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!file || !jobDescription.trim()) return;
    setErrorMsg("");
    setResponseText("");
    setLoading(true);
    try {
      const form = new FormData();
      form.append("file", file);
      form.append("job_description", jobDescription);
      const data = await ContentService.sendContent(form);  
      setResponseText(data.summery ?? "");      
    } catch (err: unknown) {
      if (err instanceof Error) setErrorMsg(err.message);
      else setErrorMsg("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setFile(null);
    setJobDescription("");
    setResponseText("");
    setErrorMsg("");
  };

  return (
    <div className="container py-4">
      <h1 className="h4 mb-4">Resume Buddy</h1>
      <HealthLine />
      <form onSubmit={handleSubmit}>
        <div className="row g-4">
          <div className="col-12 col-lg-6">
            <div className="card h-100">
              <div className="card-header">File Upload</div>
              <div className="card-body">
                <div className="mb-3">
                  <label htmlFor="resumeFile" className="form-label">
                    Upload Resume (PDF/DOCX/TXT)
                  </label>
                  <input
                    id="resumeFile"
                    type="file"
                    className="form-control"
                    accept=".pdf,.doc,.docx,.txt"
                    onChange={handleFileChange}
                    required
                  />
                  {file && <div className="form-text">Selected: {file.name}</div>}
                </div>
              </div>
            </div>
          </div>

          <div className="col-12 col-lg-6">
            <div className="card h-100">
              <div className="card-header">Job Description</div>
              <div className="card-body">
                <div className="mb-3">
                  <label htmlFor="jobDesc" className="form-label">
                    Paste Job Description
                  </label>
                  <textarea
                    id="jobDesc"
                    className="form-control"
                    rows={10}
                    value={jobDescription}
                    onChange={handleJobDescriptionChange}
                    placeholder="Paste the job description here..."
                    required
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="col-12">
            <div className="d-flex gap-2">
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true" />
                    Sending…
                  </>
                ) : (
                  "Send"
                )}
              </button>
              <button type="button" className="btn btn-outline-secondary" onClick={handleClear} disabled={loading}>
                Clear
              </button>
            </div>
          </div>

        <div className="col-12">
            <div className="card">
                <div className="card-header">Response</div>
                <div className="card-body">
                {errorMsg && (
                    <div className="alert alert-danger" role="alert">{errorMsg}</div>
                )}

                {responseText ? (
                    <div className="border rounded p-3 bg-light">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {responseText}
                    </ReactMarkdown>
                    </div>
                ) : (
                    <p className="text-body-secondary mb-0">
                    Your API response will appear here…
                    </p>
                )}
                </div>
            </div>
            </div>

        </div>
      </form>
    </div>
  );
};

export default App;
