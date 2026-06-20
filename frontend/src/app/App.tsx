import { useState } from "react";
import { NavBar } from "./components/NavBar";
import { Dashboard } from "./components/Dashboard";
import { NewJob } from "./components/NewJob";
import { JobDetail } from "./components/JobDetail";
import { Validate } from "./components/Validate";

export type Page =
  | { name: "dashboard" }
  | { name: "new-job" }
  | { name: "job-detail"; id: string }
  | { name: "validate" };

export default function App() {
  const [page, setPage] = useState<Page>({ name: "dashboard" });

  function navigate(target: Page) {
    setPage(target);
  }

  return (
    <div className="min-h-screen" style={{ background: "#F9FAFB" }}>
      <NavBar page={page} navigate={navigate} />
      {page.name === "dashboard" && <Dashboard navigate={navigate} />}
      {page.name === "new-job" && <NewJob navigate={navigate} />}
      {page.name === "job-detail" && <JobDetail id={page.id} navigate={navigate} />}
      {page.name === "validate" && <Validate />}
    </div>
  );
}
