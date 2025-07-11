// ConfirmDeleteModal.jsx
import React from "react";
import "./confirm.css";

export const ConfirmDeleteModal = ({ selectedLog, onCancel, onConfirm }) => {
  if (!selectedLog) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>Biztosan törlöd ezt a bejegyzést?</h3>
        <p>
          {selectedLog.exer_name} – {selectedLog.rep} ismétlés –{" "}
          {new Date(selectedLog.date).toLocaleString()}
        </p>
        <div className="modal-buttons">
          <button onClick={onCancel}>Mégse</button>
          <button onClick={onConfirm} className="danger">
            Törlés
          </button>
        </div>
      </div>
    </div>
  );
};
