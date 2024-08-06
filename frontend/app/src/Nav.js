import { Link } from "react-router-dom";

function Nav() {
  function logout() {
    localStorage.removeItem("user");
  }
  return (
    <>
      <Link to="/" className="site-title">
        Sell Stuff
      </Link>
      <ul>
        <li>
          <Link to="/user">User</Link>
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
