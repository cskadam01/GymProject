// ConfirmDeleteModal.jsx
import React from "react";
import "./confirm.css";

export const ConfirmDeleteModal = ({ selectedLog, onCancel, onConfirm }) => {
  if (!selectedLog) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>Napló:</h3>
        <p>
          <p>{selectedLog.exer_name}</p>  
          <p>{selectedLog.rep} ismétlés</p>
          
          {new Date(selectedLog.date).toLocaleString()}
        </p>
        <div className="modal-buttons">
          <button onClick={onCancel} className="go-back">Mégse</button>
          <button onClick={onConfirm} className="danger">
            Törlés
          </button>
        </div>
      </div>
    </div>
  );
};
