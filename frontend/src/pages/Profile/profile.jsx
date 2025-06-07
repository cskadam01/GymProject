import { useState } from "react";
import api from '../api';
import { Navbar } from "../../navbar/navbar";


export const Profile = () => {
    const [r, setR] = useState('');


      const getUser = async () => {
    try {
      const response = await api.get("/users/me");
      setR(response.data.user.name);



    } catch (err) {
      setR("Nem vagy bejelentkezve.");
    }
  };

    
    return(
        <>

            <p>{r}</p>
            <button onClick={getUser}>Get User</button>

            <Navbar/>
        
        </>

    )

   
};