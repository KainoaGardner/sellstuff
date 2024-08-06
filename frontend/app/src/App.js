import { Route, Routes } from "react-router-dom";
import Nav from "./Nav";
import User from "./User";
import Login from "./Login";
import Register from "./Register";

function App() {
  return (
    <>
      <Nav />
      <Routes>
        <Route path="/user" element={<User />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </>
  );
}

export default App;
