import { useEffect, useContext, useState } from "react";
import { Link } from "react-router-dom";
import AlertContext from "./AlertContext";
import "./static/Nav.css";
import "./static/NavLight.css";
import "./static/BaseLight.css";

function Nav() {
  const [path, setPath] = useState(window.location.pathname);
  const [, setAlert] = useContext(AlertContext);
  const showAlert = (text, type) => {
    setAlert({
      text,
      type,
    });
  };
  useEffect(() => {
    setPath(window.location.pathname);
  }, [path]);

  function logout() {
    const user = JSON.parse(localStorage.getItem("user"));
    if (user) {
      showAlert(`${user.username} Logged Out`, "normal");
    } else {
      showAlert(`Logged Out`, "normal");
    }
    localStorage.removeItem("user");
  }

  return (
    <>
      <div className="linkMain">
        <div className="linkLeft">
          <Link to="/" className="link linkTitle">
            Sell Stuff
          </Link>
        </div>
        <div className="linkRight">
          <Link className="link linkButton" to="/user">
            User
          </Link>
          <Link className="link linkButton" to="/data">
            Data
          </Link>
          <Link className="link linkButton" to="/login">
            Login
          </Link>
          <Link className="link linkButton" to="/register">
            Register
          </Link>
          <Link
            className="link linkButton"
            to="/login"
            onClick={() => {
              logout();
            }}
          >
            Logout
          </Link>
        </div>
      </div>
    </>
  );
}

export default Nav;
