import React from "react";
import "./DriversList.css";
import Header from "../../Components/Header/Header";
import { getNotVerifiedUsers, verifyUser } from "../../APIFunctions/adminCalls";
import { useState, useEffect } from "react";

const DriversList = () => {
  const [users, setUsers] = useState([]);
  const [errors, setErrors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getNotVerifiedUsers()
      .then((response) => {
        if (response.status === 200) {
          setUsers(response.data);
          setLoading(false);
        }
      })
      .catch((error) => {
        if (error.response) {
          setErrors([...errors, error.response.data.error]);
          setTimeout(() => {
            setErrors(
              errors.filter((error) => error !== error.response.data.error)
            );
          }, 3000);
        }
      });
  }, []);

  const handleVerify = (userId, verify) => {
    verifyUser(verify)
      .then((response) => {
        if (response.status === 200) {
          setUsers(
            users.map((user) => {
              if (user.user_id === userId) {
                return { ...user, verified: verify };
              } else {
                return user;
              }
            })
          );
        }
      })
      .catch((error) => {
        if (error.response) {
          setErrors([...errors, error.response.data.error]);
          setTimeout(() => {
            setErrors(
              errors.filter((error) => error !== error.response.data.error)
            );
          }, 3000);
        }
      });
  };

  return (
    <div>
      <Header />
      {loading ? (
        <div className="loading">
          <h1>Loading...</h1>
        </div>
      ) : (
        <div className="drivers-list">
          <div className="drivers-list-title">
            <h2>Drivers List</h2>
          </div>
          {errors &&
            errors.map((error, i) => (
              <div key={i} className="error">
                {error}
              </div>
            ))}
          <div className="drivers-list-container">
            <div className="drivers-list-header">
              <div className="header-card">
                <div className="header-item">ID</div>
                <div className="header-item">Name</div>
                <div className="header-item">Email</div>
                <div className="header-item">License Number</div>
                <div className="header-item">Verified</div>
              </div>
            </div>
            <div className="drivers-list-content">
              {users.map((user) => {
                return (
                  <div className="content-card" key={user.user_id}>
                    <div className="content-item">{user.user_id}</div>
                    <div className="content-item">
                      {user.first_name} {user.last_name}
                    </div>
                    <div className="content-item">{user.email}</div>
                    <div className="content-item">{user.license_number}</div>
                    <div className="content-item">
                      {user.verified ? (
                        <img
                          src="/verified.png"
                          alt="verified"
                          width={"30px"}
                        />
                      ) : (
                        <img
                          src="/unverified.png"
                          alt="not-verified"
                          width={"30px"}
                        />
                      )}
                    </div>
                    <div
                      onClick={() => handleVerify(user.user_id, !user.verified)}
                      className={
                        user.verified ? "deactivate-button" : "activate-button"
                      }
                    >
                      {user.verified ? "Deactivate" : "Activate"}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DriversList;
