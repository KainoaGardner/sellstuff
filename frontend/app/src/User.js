import React, { useState, useEffect } from "react";
import BASEURL from "./config";
import { useNavigate } from "react-router-dom";
import api from "./Api";

function User() {
  const user = JSON.parse(localStorage.getItem("user"));
  const navigate = useNavigate();

  const [username, setUsername] = useState();
  const [items, setItems] = useState([]);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    price: 0,
    sold: false,
  });

  const fetchItems = async () => {
    try {
      const response = await api.get("/items/all");
      setItems(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    if (!user) {
      navigate("/login");
    } else {
      setUsername(user.username);
      fetchItems();
    }
  }, []);

  const handleInputChange = (event) => {
    const value =
      event.target.type === "checkbox"
        ? event.target.checked
        : event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    await api.post("/items/create", formData);
    fetchItems();
    setFormData({
      title: "",
      description: "",
      price: 0,
      sold: false,
    });
  };

  async function toggleSold(item) {
    const TOKEN = user.token;

    try {
      const response = await fetch(
        BASEURL + `/items/toggle_sold?item_id=${item.id}`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${TOKEN}`,
            "Content-Type": "application/json",
          },
        },
      );
      if (response.ok) {
        fetchItems();
      }
    } catch (error) {
      console.log(error);
    }
  }

  async function deleteItem(item_id) {
    await api.delete(`/items/delete?item_id=${item_id}`);
    fetchItems();
  }

  return (
    <>
      <h1>{username}</h1>
      <form onSubmit={handleFormSubmit}>
        <label htmlFor="title">Title</label>
        <input
          type="text"
          id="title"
          name="title"
          onChange={handleInputChange}
          value={formData.title}
          required
        />
        <label htmlFor="description">Description</label>
        <input
          type="text"
          id="description"
          name="description"
          onChange={handleInputChange}
          value={formData.description}
        />
        <label htmlFor="price">Price</label>
        <input
          type="number"
          id="price"
          name="price"
          step="0.01"
          onChange={handleInputChange}
          value={formData.price}
        />

        <label htmlFor="sold">Sold</label>
        <input
          type="checkbox"
          id="sold"
          name="sold"
          onChange={handleInputChange}
          value={formData.sold}
        />

        <button type="submit">Submit</button>
      </form>

      <ul>
        {items.map((item) => (
          <div key={item.id}>
            <h2>{item.title}</h2>
            <p>{item.description}</p>
            <p>${item.price}</p>
            {item.sold ? (
              <button onClick={() => toggleSold(item)}>Sold</button>
            ) : (
              <button onClick={() => toggleSold(item)}>Not Sold</button>
            )}

            <button onClick={() => deleteItem(item.id)}>Delete</button>
          </div>
        ))}
      </ul>
    </>
  );
}

export default User;
