import { useEffect, useState } from "react";
import axios from '../../instance';
import { Navbar } from "../../Navbar/navbar";
import { useNavigate } from "react-router-dom";
import { ProfileHeader } from "./components/profile_header/profileHeader";
import { ProfileBody } from "./components/profile_body/profile_body";



export const Profile = () => {

  
    const [userName, setUserName] = useState('');
    const [age, setAge] = useState('');
    const [email, setEmail] = useState('');
    const [exerCount, setExerCount] = useState('');
    const navigate = useNavigate();

    
useEffect(()=>{

   const getUser = async () => {
    try {
      const response = await axios.get("/users/me", {
        
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
            <div className="profile-container" style={{ height:"100vh", background:"#0e0e11", overflow:"scroll"}}>
            <Navbar />
            <div className="profile-content">
                <ProfileHeader username = {userName}/>
                <ProfileBody age = {age} email = {email} exercount = {exerCount} />


            </div>


            
          </div>
        </>

    )

   
};