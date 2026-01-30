import { useEffect, useState } from "react";
import axios from '../../instance';
import { Navbar } from "../../Navbar/navbar";
import { useNavigate } from "react-router-dom";
import { ProfileHeader } from "./components/profile_header/profileHeader";
import { ProfileBody } from "./components/profile_body/profile_body";
import { ProfileCard } from "./components/profile_cards/profile_cards";
import style from "./profile.module.css"
import { FiSave } from "react-icons/fi";
import { AiOutlineFire } from "react-icons/ai";


export const Profile = () => {

  
    const [userName, setUserName] = useState('');
    const [age, setAge] = useState('');
    const [email, setEmail] = useState('');
    const [streak, setStreak] = useState('');
    const [total, setTotal] = useState('');
    const [weekly, setWeekly] = useState('');
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
      setStreak(response.data.streak)
      setTotal(response.data.total_workouts)
      setWeekly(response.data.weekly_prs)
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
                <div className={style.cardcont}>
                <ProfileCard name = "Edzések" number = {total} text = "Összesen"  icon={<FiSave />} borderColor="hsla(273, 74%, 43%, 0.52)" backGroundColor="#0B0D14" />
                <ProfileCard name = "Ez a hét" number = {streak} text = "edzések"  icon={<AiOutlineFire />} borderColor="hsla(189, 74%, 43%, 0.52)" backGroundColor="#0B0D14" />
                
                </div>


            </div>


            
          </div>
        </>

    )

   
};