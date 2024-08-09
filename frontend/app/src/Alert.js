import React, { useContext } from "react";
import AlertContext from "./AlertContext";

function Alert() {
  const [alert] = useContext(AlertContext);
  if (!alert) {
    return null;
  }
  return <div>{alert.text}</div>;
}
export default Alert;
