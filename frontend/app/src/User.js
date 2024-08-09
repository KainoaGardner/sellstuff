import React, { useState, useEffect, useContext } from "react";
import { baseurl, imageurl } from "./config";
import { useNavigate } from "react-router-dom";
import api from "./Api";
import AlertContext from "./AlertContext";

function User() {
  const user = JSON.parse(localStorage.getItem("user"));
  const [timestamp, setTimestamp] = useState(new Date().getTime());
  const navigate = useNavigate();

  const [, setAlert] = useContext(AlertContext);
  const showAlert = (text, type) => {
    setAlert({
      text,
      type,
    });
  };

  const [items, setItems] = useState([]);
  const [sort, setSort] = useState("id");
  const [reverse, setReverse] = useState(false);
  const [username, setUsername] = useState();
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    price: 0,
    sold: false,
  });

  const fetchItems = async () => {
    try {
      const response = await api.get(
        `/items/all?sort=${sort}&reverse_sort=${reverse}`,
      );
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
    }
  }, []);

  useEffect(() => {
    fetchItems();
  }, [sort, reverse]);

  const handleInputChange = (event) => {
    const value = event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleInputChange2 = (event) => {
    const value = event.target.value;
    setSort(value);
    fetchItems();
  };

  const handleReverseChange = (event) => {
    setReverse(event.target.checked);
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    let newForm = new FormData();
    newForm.append("title", formData.title);
    newForm.append("description", formData.description);
    newForm.append("price", formData.price);
    if (formData.sold) {
      newForm.append("sold", formData.sold);
    }

    await api.post("/items/create", newForm);
    fetchItems();
    setFormData({
      title: "",
      description: "",
      price: 0,
      sold: false,
    });
    showAlert(`${formData.title} Added`, "normal");
  };

  async function toggleSold(item) {
    const TOKEN = user.token;

    try {
      const response = await fetch(
        baseurl + `/items/toggle_sold?item_id=${item.id}`,
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

  async function uploadImage(image, item) {
    const TOKEN = user.token;
    let data = new FormData();
    data.append("file", image);

    try {
      const response = await fetch(
        baseurl + `/items/image/?item_id=${item.id}`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${TOKEN}`,
          },
          body: data,
        },
      );
      console.log(response);
      if (response.ok) {
        setTimestamp(new Date().getTime());
        fetchItems();
        showAlert(`${item.title} Image Updated`, "normal");
      }
    } catch (error) {
      console.log(error);
    }

    fetchItems();
  }

  const handleFileChange = (event, item) => {
    const image = event.target.files[0];
    uploadImage(image, item);
  };

  async function deleteItem(item) {
    await api.delete(`/items/delete?item_id=${item.id}`);
    showAlert(`${item.title} Deleted Updated`, "normal");
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
          type="date"
          id="sold"
          name="sold"
          onChange={handleInputChange}
          value={formData.sold}
        />

        <button type="submit">Submit</button>
      </form>

      <form>
        <label for="sort">Sort Type</label>
        <select name="sort" id="sort" onChange={handleInputChange2}>
          <option value="id">Added</option>
          <option value="title">Title</option>
          <option value="price">Price</option>
          <option value="sold_date">Sold Date</option>
        </select>
        <label for="reverse">Reverse</label>
        <input
          type="checkbox"
          name="reverse"
          id="reverse"
          onChange={handleReverseChange}
        />
      </form>

      <ul>
        {items.map((item) => (
          <div key={item.id}>
            <img src={`${imageurl}/${item.image}`} width="100" height="100" />
            <h2>{item.title}</h2>
            <p>{item.description}</p>
            <p>${item.price}</p>
            {item.sold ? (
              <div>
                <p>{item.sold}</p>
                <button onClick={() => toggleSold(item)}>Unsell</button>
              </div>
            ) : (
              <div>
                <p>Not Yet Sold</p>
                <button onClick={() => toggleSold(item)}>Sell</button>
              </div>
            )}

            <button onClick={() => deleteItem(item)}>Delete</button>
            <label for="image"></label>
            <input
              type="file"
              id="image"
              name="image"
              accept="image/png,image/jpeg"
              onChange={(e) => handleFileChange(e, item)}
            />
          </div>
        ))}
      </ul>
    </>
  );
}

export default User;
