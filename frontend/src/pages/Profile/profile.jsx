import { useState } from "react";
import axios from 'axios';

export const Profile = () => {
    const [r, setR] = useState('');


      const getUser = async () => {
    try {
      const response = await axios.get("http://localhost:8000/users/me", {
        withCredentials: true
      });
      setR(response.data.user.name);



    } catch (err) {
      setR("Nem vagy bejelentkezve.");
    }
  };

    
    return(
        <>

            <p>{r}</p>
            <button onClick={getUser}>Get User</button>
        
        </>

    )

   
};