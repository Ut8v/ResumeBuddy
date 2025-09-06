import React, { useEffect, useState } from "react";

const BASE_URL = import.meta.env.VITE_BASE_URL;

const HealthLine: React.FC = () => {
  const [line, setLine] = useState("Checking API…");

  useEffect(() => {
    (async () => {
      try {
        const [liveRes, readyRes] = await Promise.all([
          fetch(`${BASE_URL}/health`),
          fetch(`${BASE_URL}/health/ready`),
        ]);

        const live = liveRes.ok ? await liveRes.json() : null;
        const ready = readyRes.ok ? await readyRes.json() : null;

        if (live && ready) {
          const up = typeof live.uptime_seconds === "number" ? `${Math.round(live.uptime_seconds)}s` : "—";
          const r = ready.status || "degraded";
          const failing =
            ready.checks ? Object.keys(ready.checks).filter((k) => ready.checks[k] === false) : [];
          const suffix = r === "ok" ? "" : (failing.length ? ` – ${failing.join(", ")} failing` : "");
          setLine(`API: ${live.status || "unknown"} (uptime ${up}) · Ready: ${r}${suffix}`);
        } else if (live) {
          const up = typeof live.uptime_seconds === "number" ? `${Math.round(live.uptime_seconds)}s` : "—";
          setLine(`API: ${live.status || "unknown"} (uptime ${up}) · Ready: unknown`);
        } else if (ready) {
          setLine(`API: unknown · Ready: ${ready.status || "degraded"}`);
        } else {
          setLine("API: unreachable");
        }
      } catch {
        setLine("API: unreachable");
      }
    })();
  }, []);

  return <div className="text-body-secondary small">{line}</div>;
};

export default HealthLine;

