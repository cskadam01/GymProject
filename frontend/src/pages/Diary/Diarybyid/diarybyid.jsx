import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { AddNewRecord } from "./components/addnewrecord";
import { GetDiaryDetail } from "./components/getDiaryDetails";
import axios from "axios";

export const OpenedExer = () => {
    const [exerName, setExerName] = useState("")
    const { id } = useParams();
    const [error, setError] = useState(false);
    const [loading, setLoading] = useState(true);
    const [isValid, setIsValid] = useState(false);
    const [refresh, setRefresh] = useState(0);

    useEffect(() => {
        



        const GetExerByID = async () => {
            try{
            
            const Validate = await axios.get("http://localhost:8000/exercise/is-authorized", {params: {exercise_id: id}, withCredentials: true})
            
            setIsValid(Validate.data.authorized)
                
            if (Validate.data.authorized){
                const response = await axios.get(`http://localhost:8000/exercise/exer/${id}`);
                setExerName(response.data.exer_name);

            }
        }
            catch(err){
                console.error("hiba: ". err)

            }
            finally{
                setLoading(False)

            }

        };
        
        GetExerByID();
    }, [id]);


    if (loading) return    <p>Töltés</p>

    if(isValid === false){return <p>Nem naplózott feladatot próbálsz meg elérni</p>} 

    

    return(

        <>

j
    

        
        <>
        <AddNewRecord exerName={exerName} exer_id={id} triggerRefresh = {()=> setRefresh(prev => prev + 1)}/>
        <GetDiaryDetail exer_id={id} refresh_key={refresh} /> 
        </>
      
        

        </>
        
        
    )
   
    







}

