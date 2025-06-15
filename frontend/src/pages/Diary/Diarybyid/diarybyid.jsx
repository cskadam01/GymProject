import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { AddNewRecord } from "./components/addnewrecord";
import { GetDiaryDetail } from "./components/getDiaryDetails";
import axios from "axios";
import "./diarybyid.css";
import { Navbar } from "../../../Navbar/navbar";


export const OpenedExer = () => {
    const [exerName, setExerName] = useState("")
    const { id } = useParams();
    const [error, setError] = useState(false);
    const [loading, setLoading] = useState(true);
    const [isValid, setIsValid] = useState(null);
    const [refresh, setRefresh] = useState(0);

    useEffect(() => {
                const GetExerByID = async () => {
                    try {
                    const Validate = await axios.get(
                        "http://localhost:8000/diary/is-authorized",
                        {
                        params: { exercise_id: id },
                        withCredentials: true,
                        }
                    );

                    const allowed = Validate.data.authorized;
                    console.log("Authorization válasz:", Validate.data);

                    if (allowed) {
                        const response = await axios.get(`http://localhost:8000/exercise/exer/${id}`);
                        setExerName(response.data.exer_name);
                        setIsValid(true); // ✅ csak akkor állítjuk true-ra, ha minden adat megvan
                    } else {
                        setIsValid(false); // ❌ nincs jogosultság
                    }
                    } catch (err) {
                    console.error("hiba:", err);
                    setIsValid(false); // biztonsági fallback
                    } finally {
                    setLoading(false);
                    }
                };

                GetExerByID();
}, [id]);

    if (loading || isValid === null) return <p>Töltés...</p>;

    if(isValid === false){return <p>Nem naplózott feladatot próbálsz meg elérni</p>} 

    

    return(

        
    

        
        <>

        <Navbar/>
        <div className="diary-by-id-cont">
            <h1 style={{textAlign:'center', marginTop:"10%", color:'white', fontSize:"3rem"}}>{exerName}</h1>
        <AddNewRecord exerName={exerName} exer_id={id} triggerRefresh = {()=> setRefresh(prev => prev + 1)}/>

            
        <GetDiaryDetail exer_id={id} refresh_key={refresh} /> 
        </div>
        
        </>
      

        
        
    )
   
    







}

