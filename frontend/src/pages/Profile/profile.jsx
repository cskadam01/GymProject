import { useEffect, useState, useTransition } from "react";
import axios from '../../instance';
import { Navbar } from "../../Navbar/navbar";
import { useNavigate } from "react-router-dom";
import { ProfileHeader } from "./components/profile_header/profileHeader";
import { ProfileCard } from "./components/profile_cards/profile_cards";
import style from "./profile.module.css"
import { FiSave } from "react-icons/fi";
import { AiOutlineFire } from "react-icons/ai";
import { WeeklyGoal } from "./components/weekly_goals/weeklyGoals";

export const Profile = ({}) => {

  
    const [userName, setUserName] = useState('');
    const [age, setAge] = useState('');
    const [email, setEmail] = useState('');
    const [streak, setStreak] = useState('');
    const [total, setTotal] = useState('');
    const [weekly, setWeekly] = useState('');
    const [exerCount, setExerCount] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [days, setDays] = useState("")
    const navigate = useNavigate();
    

    
useEffect(()=>{

   const getUser = async () => {
    setIsLoading(true);
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
      setDays(response.data.days)

    } catch (err) {
      
    } finally {
      setIsLoading(false);
    }
  };

  getUser()
}, [])
   

    
    return(
        <>
            <div className="profile-container" style={{ height:"100vh", background:"#050507", overflow:"scroll"}}>
            <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
            <Navbar />
            {isLoading ? (
              <div style={{ height: "calc(100vh - 60px)", display: "flex", alignItems: "center", justifyContent: "center", background: "#050507" }}>
                <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
                  <div style={{ width: 44, height: 44, borderRadius: "50%", border: "4px solid rgba(255,255,255,0.15)", borderTopColor: "rgba(255,255,255,0.9)", animation: "spin 0.9s linear infinite" }} />
                  <div style={{ color: "rgba(255,255,255,0.75)", fontSize: 14 }}>Betöltés...</div>
                </div>
              </div>
            ) : (
            <div className="profile-content">
                <ProfileHeader username = {userName}/>
                
                <div className={style.cardcont}>
                <ProfileCard name = "Edzések" number = {total} text = "Összesen"  icon={<FiSave />} borderColor="hsla(273, 74%, 43%, 0.52)" backGroundColor="#0B0D14" />
                <ProfileCard name = "Ez a hét" number = {streak} text = "edzések"  icon={<AiOutlineFire />} borderColor="hsla(189, 74%, 43%, 0.52)" backGroundColor="#0B0D14" />
                <ProfileCard name = "Feladatok" number = {exerCount} text = "összes naplózott"  icon={<AiOutlineFire />} borderColor="hsla(189, 74%, 43%, 0.52)" backGroundColor="#0B0D14" />
                <ProfileCard name = "PR-ok" number = {weekly} text = "heti"  icon={<AiOutlineFire />} borderColor="hsla(189, 74%, 43%, 0.52)" backGroundColor="#0B0D14" />
                </div>

                <WeeklyGoal current={streak} goal={5} days={days}/>


            </div>
            )}
          </div>
        </>

    )

   
};