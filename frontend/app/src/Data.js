import React, { useContext, useState, useEffect } from "react";
import { baseurl, imageurl } from "./config";
import { useNavigate } from "react-router-dom";
import AlertContext from "./AlertContext";

import api from "./Api";

function Data() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user"));
  const [, setAlert] = useContext(AlertContext);
  const showAlert = (text, type) => {
    setAlert({
      text,
      type,
    });
  };

  useEffect(() => {
    if (!user) {
      navigate("/login");
    }
    fetchData();
  }, []);

  const [color, setColor] = useState("blue");
  const [timeframe, setTimeframe] = useState("weekly");
  const [valueType, setValueType] = useState("sales");
  const [time, setTime] = useState(new Date().getTime());
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
      showAlert(`Must Be Logged In`, "danger");
    } else {
      fetchGraphes();
    }
  }, [color, timeframe, valueType]);

  const fetchData = async () => {
    try {
      const response = await api.get(`/users/data`);
      setData(response.data);
    } catch (error) {}
  };

  async function fetchGraphes() {
    const TOKEN = user.token;

    try {
      await fetch(
        baseurl +
          `/graphs/bar?value_type=${valueType}&graph_type=${timeframe}&color=${color}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${TOKEN}`,
            "Content-Type": "application/json",
          },
        },
      );
    } catch (error) {}
    setTime(new Date().getTime());
  }

  const handleColorInput = (event) => {
    const value = event.target.value;
    setColor(value);
  };

  const handleTimeFrameInput = (event) => {
    const value = event.target.value;
    setTimeframe(value);
  };

  const handleValueInput = (event) => {
    const value = event.target.value;
    setValueType(value);
  };

  return (
    <>
      <h1 className="title">Data</h1>
      <hr />
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
        <h3>{color}</h3>
        <h3>{timeframe}</h3>
        <h3>{valueType}</h3>
        <form>
          <label htmlFor="color">Color</label>
          <select name="color" id="color" onChange={handleColorInput}>
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

        <form>
          <label htmlFor="timeframe">Timeframe</label>
          <select
            name="timeframe"
            id="timeframe"
            onChange={handleTimeFrameInput}
          >
            <option value="weekly" selected="selected">
              Weekly
            </option>
            <option value="monthly">Monthly</option>
            <option value="yearly">Yearly</option>
          </select>
        </form>

        <form>
          <label htmlFor="value">Value</label>
          <select name="value" id="value" onChange={handleValueInput}>
            <option value="sales" selected="selected">
              Sales
            </option>
            <option value="profit">Profit</option>
          </select>
        </form>
        <img
          id="bargraph"
          src={user ? `${imageurl}/${user.id}/bar.png?${time}` : ""}
          width="500"
        />
      </div>
    </>
  );
}

export default Data;
