import React from "react";
import "./Home.css";
import Header from "../../Components/Header/Header";

const Home = () => {
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("Login");
    // Implement your log-in logic here.
  };

  return (
    <div className="home-container">
      <Header />
      <div className="login-container">
        <h2>Login</h2>
        <form>
          <input type="text" placeholder="Username" />
          <input type="password" placeholder="Password" />
          <button type="submit" onClick={handleSubmit}>
            Login
          </button>
        </form>
        {/* Don't have an account ? signup */}
        <div className="signup-link">
          Don't have an account ? <a href="/signup">Sign Up</a>
        </div>
      </div>
    </div>
  );
};

export default Home;
