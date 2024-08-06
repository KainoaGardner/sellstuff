import React, { useState } from "react";
import BASEURL from "./config";
import { useNavigate } from "react-router-dom";

function Register() {
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
      console.log(formData.username, formData.password);
      const response = await fetch(BASEURL + "/users/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
        },

        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
        }),
      });
      if (response.ok) {
        const data = await response.json();
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

  return (
    <>
      <h1>Register</h1>
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

export default Register;
