import { useEffect, useState } from "react";
import axios from 'axios';
import { Navbar } from "../../Navbar/navbar";
import { useNavigate } from "react-router-dom";



export const Profile = () => {

  
    const [userName, setUserName] = useState('');
    const [age, setAge] = useState('');
    const [email, setEmail] = useState('');
    const [exerCount, setExerCount] = useState('');
    const navigate = useNavigate();

const HandleLogout = async () => {
        try{
        const response = await axios.post("http://localhost:8000/users/logout", {}, {withCredentials: true});
        

        console.log("kijelentkezve:",response.data);
        navigate("/login")
    
        }


    catch (err){
        console.error(err)
    }};
    
useEffect(()=>{

   const getUser = async () => {
    try {
      const response = await axios.get("http://localhost:8000/users/me", {
        withCredentials: true
      });
      setUserName(response.data.user);
      setAge(response.data.age)
      setEmail(response.data.email)
      setExerCount(response.data.exers)





    } catch (err) {
      
    }
  };

  getUser()
}, [])
   

    
    return(
        <>
            <div className="profile-container">
            <Navbar />
            <h1 style={{marginTop:"20px"}}>Szia {userName}! </h1>


            
            <p>Email címed: {email}</p>
            <p>Korod: {age}  </p>
            <p>Naplózott feladataid száma: {exerCount} </p>
            <button onClick={HandleLogout}>Kijelentkezés</button>


            
          </div>
        </>

    )

   
};