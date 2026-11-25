import { Link } from "react-router-dom";
import { ResearchScene } from "./ResearchScene";

export default function App() {
  return (
    <main className="app-shell">
      <ResearchScene />
      <nav className="topbar">
        <Link className="brand" to="/">OMNI<span>-RAG</span></Link>
        <div className="nav-links">
          <a href="#how">How it works</a>
          <Link to="/login">Sign in</Link>
        </div>
      </nav>
      <section className="hero">
        <div className="eyebrow">MULTIMODAL SCIENTIFIC RESEARCH ASSISTANT</div>
        <h1>Answers grounded in <span>your papers.</span></h1>
        <p className="hero-copy">
          Upload research documents, ask natural-language questions, and trace every claim back to a real page, table, or figure region.
        </p>
        <div className="hero-actions">
          <Link className="primary-button" to="/guest">Explore as guest <span>→</span></Link>
          <Link className="secondary-button" to="/signup">Create an account</Link>
        </div>
        <div className="trust-row">
          <span><i /> Evidence-first answers</span>
          <span><i /> Private document scope</span>
          <span><i /> No invented citations</span>
        </div>
      </section>
      <section className="how" id="how">
        <div><span>01</span><strong>Upload</strong><p>Bring your own PDF or scientific image.</p></div>
        <div><span>02</span><strong>Retrieve</strong><p>Search text, tables, figures, and OCR evidence.</p></div>
        <div><span>03</span><strong>Cite</strong><p>Every supported claim links to its source region.</p></div>
        <div><span>04</span><strong>Verify</strong><p>Inspect retrieval scores and evidence quality.</p></div>
      </section>
    </main>
  );
}
