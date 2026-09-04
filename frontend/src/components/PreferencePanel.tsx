import type { PreferenceSignal } from "../types";

interface Props {
  signals: PreferenceSignal[];
  onClose: () => void;
}

const FEATURE_LABELS: Record<string, string> = {
  role_family: "Role family",
  technology: "Technology",
  domain: "Domain",
  company_type: "Company type",
  seniority: "Seniority",
  location: "Location",
  work_model: "Work model",
};

export function PreferencePanel({ signals, onClose }: Props) {
  const grouped = new Map<string, PreferenceSignal[]>();
  for (const s of signals) {
    const list = grouped.get(s.feature_type) ?? [];
    list.push(s);
    grouped.set(s.feature_type, list);
  }
  for (const list of grouped.values()) {
    list.sort((a, b) => Math.abs(b.weight) - Math.abs(a.weight));
  }

  return (
    <div className="pref-panel-overlay" onClick={onClose}>
      <div className="pref-panel" onClick={(e) => e.stopPropagation()}>
        <div className="pref-panel-header">
          <h2>Learned preference signals</h2>
          <button type="button" className="link-btn" onClick={onClose}>
            close
          </button>
        </div>
        {signals.length === 0 && <p>No feedback recorded yet.</p>}
        {[...grouped.entries()].map(([featureType, list]) => (
          <div key={featureType} className="pref-group">
            <h3>{FEATURE_LABELS[featureType] ?? featureType}</h3>
            <table className="pref-table">
              <tbody>
                {list.map((s) => (
                  <tr key={`${s.feature_type}-${s.feature_value}`}>
                    <td>{s.feature_value}</td>
                    <td className={s.weight >= 0 ? "weight-pos" : "weight-neg"}>
                      {s.weight >= 0 ? "+" : ""}
                      {s.weight.toFixed(2)}
                    </td>
                    <td className="pref-evidence">
                      {s.evidence_count} evt · {s.confidence}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
}
