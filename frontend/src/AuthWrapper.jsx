import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export const AuthWrapper = ({ children }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [authorized, setAuthorized] = useState(false);



  //Lekérjük a felhasználót és ha van találat akkor authorized-ot true-ra állítjuk ha pedig nincs találat visszakerülünk a login page-re
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await axios.get("http://localhost:8000/users/me", {
          withCredentials: true,
        });

        if (response.status === 200) {
          setAuthorized(true);
        }
      } catch (error) {
        navigate("/login");
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [navigate]);

  if (loading) {
    return <div>Betöltés...</div>;
  }

  if (!authorized) {
    
    return null;
  }

  return <>{children}</>;
};