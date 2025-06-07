import { useState } from "react";
import api from "../api";

export const Navbar =() => {


   
        const HandleLogout = async () => {
        try{
        const response = await api.post("/users/logout", {});
        

        console.log("kijelentkezve:",response.data);
    
        }
    




    

    catch (err){
        console.error(err)


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