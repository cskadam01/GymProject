import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";
import axios from "./instance";

export const AuthWrapper = ({ children }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [authorized, setAuthorized] = useState(false);



  //Lekérjük a felhasználót és ha van találat akkor authorized-ot true-ra állítjuk ha pedig nincs találat visszakerülünk a login page-re
  useEffect(() => {
    const checkAuth = async () => {
      const token =localStorage.getItem("access_token")//lekérjük a local storagbementett tokent
      if(!token){
        navigate("/login")
        return


      }


      try {
        const response = await axios.get("/users/me", {
          headers:{
            Authorization: `Bearer ${token}`,


          },
        });

        if (response.status === 200) {
          setAuthorized(true);
        }
      } catch (error) {
        console.error("Auth error:", error);
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