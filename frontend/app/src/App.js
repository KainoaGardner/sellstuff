import { Route, Routes } from "react-router-dom";
import Nav from "./Nav";
import Home from "./Home";
import Alert from "./Alert";
import User from "./User";
import Data from "./Data";
import Login from "./Login";
import Register from "./Register";

function App() {
  return (
    <>
      <Nav />
      <Alert />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/user" element={<User />} />
        <Route path="/data" element={<Data />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </>
  );
}

export default App;
