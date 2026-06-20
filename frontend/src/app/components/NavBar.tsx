import { Route, ExternalLink } from "lucide-react";
import type { Page } from "../App";

interface NavBarProps {
  page: Page;
  navigate: (p: Page) => void;
}

export function NavBar({ page, navigate }: NavBarProps) {
  const navLinks: { label: string; target: Page }[] = [
    { label: "Dashboard", target: { name: "dashboard" } },
    { label: "New Job", target: { name: "new-job" } },
    { label: "Validate", target: { name: "validate" } },
  ];

  function isActive(target: Page) {
    return target.name === page.name;
  }

  return (
    <header
      style={{
        height: 56,
        background: "#fff",
        borderBottom: "1px solid #E5E7EB",
        boxShadow: "0 1px 3px rgba(0,0,0,0.06)",
      }}
      className="flex items-center px-6 gap-8 sticky top-0 z-50"
    >
      {/* Logo */}
      <button
        onClick={() => navigate({ name: "dashboard" })}
        className="flex items-center gap-2 shrink-0"
        style={{ background: "none", border: "none", cursor: "pointer", padding: 0 }}
      >
        <div
          style={{ background: "#2563EB", borderRadius: 8, width: 32, height: 32 }}
          className="flex items-center justify-center"
        >
          <Route size={18} color="#fff" />
        </div>
        <span style={{ color: "#111827", fontWeight: 600, fontSize: 15 }}>Route Optimizer</span>
      </button>

      {/* Nav links */}
      <nav className="flex items-center gap-1 flex-1">
        {navLinks.map((link) => {
          const active = isActive(link.target);
          return (
            <button
              key={link.label}
              onClick={() => navigate(link.target)}
              style={{
                padding: "6px 12px",
                borderRadius: 6,
                fontSize: 14,
                fontWeight: active ? 600 : 400,
                color: active ? "#2563EB" : "#6B7280",
                background: active ? "#EFF6FF" : "transparent",
                border: "none",
                cursor: "pointer",
                transition: "all 0.15s",
              }}
            >
              {link.label}
            </button>
          );
        })}
      </nav>

      {/* API Docs */}
      <a
        href="#api-docs"
        style={{ textDecoration: "none", color: "#6B7280", fontSize: 14 }}
        className="flex items-center gap-1 hover:text-gray-900 transition-colors"
      >
        API Docs <ExternalLink size={13} />
      </a>
    </header>
  );
}
