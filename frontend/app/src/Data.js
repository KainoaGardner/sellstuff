import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import api from "./Api";

function Data() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user"));
  const [data, setData] = useState({
    total_items: 0,
    total_sales: 0,
    profit: "0",
    average_sale_price: "0",
    biggest_profit_item: "",
  });

  useEffect(() => {
    if (!user) {
      navigate("/login");
    }
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await api.get(`/users/data`);
      console.log(response.data);
      setData(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  async function fetchGraphes() {
    const TOKEN = user.token;

    try {
      // const response = await fetch(
      //   BASEURL + `/items/toggle_sold?item_id=${item.id}`,
      //   {
      //     method: "PUT",
      //     headers: {
      //       Authorization: `Bearer ${TOKEN}`,
      //       "Content-Type": "application/json",
      //     },
      //   },
      // );
      console.log();
      // if (response.ok) {
      // }
    } catch (error) {
      console.log(error);
    }
  }

  const handleInputChange = (event) => {
    const value = event.target.value;
    // setGraph(value);
  };

  return (
    <>
      <h1>Data</h1>
      <div>
        <h2>Total Intems</h2>
        <h2>{data.total_items}</h2>
      </div>
      <div>
        <h2>Total Sales</h2>
        <h2>{data.total_sales}</h2>
      </div>
      <div>
        <h2>Total Profit</h2>
        <h2>{data.profit}</h2>
      </div>
      <div>
        <h2>Average Sale Price</h2>
        <h2>{data.average_sale_price}</h2>
      </div>
      <div>
        <h2>Biggest Profit Item</h2>
        <h2>{data.biggest_profit_item}</h2>
      </div>

      <div>
        <form>
          <label for="color">Color</label>
          <select name="color" id="color">
            <option value="red">Red</option>
            <option value="orange">Orange</option>
            <option value="yellow">Yellow</option>
            <option value="green">Green</option>
            <option value="blue" selected="selected">
              Blue
            </option>
            <option value="purple">Purple</option>
            <option value="black">Black</option>
          </select>
        </form>
      </div>
    </>
  );
}

export default Data;
