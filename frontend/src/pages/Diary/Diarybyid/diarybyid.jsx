import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { AddNewRecord } from "./components/addnewrecord";
import { GetDiaryDetail } from "./components/getDiaryDetails";
import axios from "../../../instance";
import "./diarybyid.css";
import { Navbar } from "../../../Navbar/navbar";


export const OpenedExer = () => {
    const [exerName, setExerName] = useState("")
    const { id } = useParams(); //Ezzel ki tudjuk szedni a linkből az id-t
    const [error, setError] = useState(false);
    const [loading, setLoading] = useState(true);
    const [isValid, setIsValid] = useState(null);
    const [refresh, setRefresh] = useState(0);

    useEffect(() => {
                const GetExerByID = async () => {
                    try {
                     


                    const Validate = await axios.get(
                        "/diary/is-authorized",
                        {
                        params: { exercise_id: id }, //a headbe kerül, az id, aamit szeretnénk lekérdezni hogy a felhasználó rendelkezik e vele
                       
                        }
                    );

                    const allowed = Validate.data.authorized; //Ha  benne van a felhasználónak a listájában a feladat akkor True-t kapunk vissza 
                    console.log("Authorization válasz:", Validate.data);

                    if (allowed) {
                        const response = await axios.get(`/exercise/exer/${id}`); //a linkből kiszedjük az id-t és betesszük ide a linkbe
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

    if(isValid === false){return <p style={{color:"white"}}>Nem naplózott feladatot próbálsz meg elérni</p>} 

    

    return(

        
    

        
        <>

        <Navbar/>
        <div className="diary-by-id-cont">
            <h1 style={{textAlign:'center', marginTop:"10%", fontSize:"3rem"}}>{exerName}</h1>
        <AddNewRecord exerName={exerName} exer_id={id} triggerRefresh = {()=> setRefresh(prev => prev + 1)}/>

            
        <GetDiaryDetail exer_id={id} refresh_key={refresh} /> 
        </div>
        
        </>
      

        
        
    )
   
    







}

