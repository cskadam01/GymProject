import { useState } from "react";
import axios from "axios";

export const Navbar =() => {


   
        const HandleLogout = async () => {
        try{
        const response = await axios.post("http://localhost:8000/users/logout", {}, {withCredentials: true});
        

        console.log("kijelentkezve:",response.data);
    
        }
    




    

    catch (err){
        console.error(error)


    }};

    return(

        <>
            <a href=""></a>
            <a href=""></a>
            <a href=""></a>
            <button onClick={HandleLogout}>Logout</button>
        </>
    )



}