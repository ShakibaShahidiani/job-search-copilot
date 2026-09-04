import { REJECT_REASONS, type RejectReason } from "../types";

interface Props {
  onPick: (reason?: RejectReason) => void;
  onCancel: () => void;
}

export function RejectReasonPicker({ onPick, onCancel }: Props) {
  return (
    <div className="reject-picker">
      <div className="reject-picker-header">
        <span>Why reject? (optional)</span>
        <button type="button" className="link-btn" onClick={onCancel}>
          cancel
        </button>
      </div>
      <div className="reject-picker-chips">
        {REJECT_REASONS.map((r) => (
          <button
            key={r.value}
            type="button"
            className="chip chip-reason"
            onClick={() => onPick(r.value)}
          >
            {r.label}
          </button>
        ))}
        <button type="button" className="chip chip-reason chip-skip" onClick={() => onPick(undefined)}>
          Skip reason
        </button>
      </div>
    </div>
  );
}
