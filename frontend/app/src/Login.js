import React, { useState, useContext } from "react";
import { baseurl } from "./config";
import { useNavigate } from "react-router-dom";
import AlertContext from "./AlertContext";
import "./static/Login.css";

function Login() {
  const navigate = useNavigate();
  const [, setAlert] = useContext(AlertContext);
  const showAlert = (text, type) => {
    setAlert({
      text,
      type,
    });
  };

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const handleInputChange = (event) => {
    const value = event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch(baseurl + "/auth/token/", {
        method: "POST",
        body: new URLSearchParams({
          username: formData.username,
          password: formData.password,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        saveUser(formData.username, data.access_token, data.id);
        showAlert(`${formData.username} Logged in`, "normal");
        navigate("/user");
      } else {
        showAlert("Incorrect information", "danger");
      }
    } catch (error) {
      console.log(error);
    }
    setFormData({
      username: "",
      password: "",
    });
  };

  function saveUser(username, accessToken, id) {
    const user = { username: username, token: accessToken, id: id };
    localStorage.setItem("user", JSON.stringify(user));
  }

  return (
    <>
      <h1 className="title">Login</h1>
      <hr />
      <div className="loginMain">
        <form className="loginForm" onSubmit={handleFormSubmit}>
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            onChange={handleInputChange}
            value={formData.username}
            required
          />
          <label htmlFor="password">Password</label>
          <input
            className=""
            type="password"
            id="password"
            name="password"
            onChange={handleInputChange}
            value={formData.password}
            required
          />

          <button type="submit">Submit</button>
        </form>
      </div>
    </>
  );
}

export default Login;
