import { Route, Routes } from "react-router-dom";
import Nav from "./Nav";
import Home from "./Home";
import Alert from "./Alert";
import User from "./User";
import Data from "./Data";
import Login from "./Login";
import Register from "./Register";
import "./static/Base.css";
import "./static/Alert.css";

function App() {
  return (
    <>
      <Nav />
      <div className="mainBody">
        <Alert />
        <Routes className="mainBody">
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/user" element={<User />} />
          <Route path="/data" element={<Data />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
