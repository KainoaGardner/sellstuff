import React, { useState } from "react";
import BASEURL from "./config";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();
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
      const response = await fetch(BASEURL + "/auth/token/", {
        method: "POST",
        body: new URLSearchParams({
          username: formData.username,
          password: formData.password,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        saveUser(formData.username, data.access_token);
        navigate("/user");
      }
    } catch (error) {
      console.log(error);
    }
    setFormData({
      username: "",
      password: "",
    });
  };

  function saveUser(username, accessToken) {
    const user = { username: username, token: accessToken };
    localStorage.setItem("user", JSON.stringify(user));
  }

  return (
    <>
      <h1>Login</h1>
      <form onSubmit={handleFormSubmit}>
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
          type="password"
          id="password"
          name="password"
          onChange={handleInputChange}
          value={formData.password}
          required
        />

        <button type="submit">Submit</button>
      </form>
    </>
  );
}

export default Login;
