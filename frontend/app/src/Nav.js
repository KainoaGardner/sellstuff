import { useContext } from "react";
import { Link } from "react-router-dom";
import AlertContext from "./AlertContext";
function Nav() {
  const [, setAlert] = useContext(AlertContext);
  const showAlert = (text, type) => {
    setAlert({
      text,
      type,
    });
  };
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
      <Link to="/" className="site-title">
        Sell Stuff
      </Link>
      <ul>
        <li>
          <Link to="/home">Home</Link>
          <Link to="/user">User</Link>
          <Link to="/data">Data</Link>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
          <Link to="/login" onClick={logout}>
            Logout
          </Link>
        </li>
      </ul>
    </>
  );
}

export default Nav;
