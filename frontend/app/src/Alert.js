import React, { useContext } from "react";
import AlertContext from "./AlertContext";
import "./static/Alert.css";

function Alert() {
  const [alert] = useContext(AlertContext);
  if (!alert) {
    return null;
  }
  return (
    <div className="alertMain">
      <div className="alertIn">
        <div className="alert">{alert.text}</div>
      </div>
    </div>
  );
}
export default Alert;
